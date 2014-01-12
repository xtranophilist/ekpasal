import urllib
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from jsonfield import JSONField
from app.libr import unique_slugify
from django.core.files import File
import os


class Store(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True)
    description = models.TextField(null=True)
    image = models.ImageField(upload_to='images/stores/', null=True)
    status = models.BooleanField()
    rating = models.FloatField(null=True)
    last_updated = models.DateTimeField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        unique_slugify(self, self.name)
        super(Store, self).save(*args, **kwargs)


class Vendor(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True)
    description = models.TextField(null=True)
    address = models.TextField(null=True)
    phone = models.CharField(null=True, max_length=50)
    image = models.ImageField(upload_to='images/stores/', null=True)
    rating = models.FloatField(null=True)
    foreign = models.NullBooleanField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        unique_slugify(self, self.name)
        super(Vendor, self).save(*args, **kwargs)


class Brand(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True)
    description = models.TextField(null=True)
    image = models.ImageField(upload_to='images/brands/', null=True)
    rating = models.FloatField(null=True)
    foreign = models.NullBooleanField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        unique_slugify(self, self.name)
        super(Brand, self).save(*args, **kwargs)


class Currency(models.Model):
    name = models.CharField(max_length=50)
    short_name = models.CharField(max_length=5)
    exchange_rate = models.FloatField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = u'Currencies'


class Category(MPTTModel):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=255, blank=True)
    image = models.ImageField(upload_to='images/categories/', null=True, blank=True)
    description = models.CharField(max_length=254, null=True, blank=True)
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children')
    plural_name = models.CharField(max_length=154, null=True, blank=True)

    def get_plural_name(self):
        return self.plural_name or self.name + 's'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = u'Categories'

    def save(self, *args, **kwargs):
        unique_slugify(self, self.name)
        super(Category, self).save(*args, **kwargs)

    def get_all_categories(self):
        return list(self.get_ancestors(include_self=True))

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'image': self.image,
            'categories': self.get_all_categories(),
        }


class Image(models.Model):
    image_file = models.ImageField(upload_to='images/products/', null=True)
    image_url = models.URLField()

    def get_remote_image(self):
        if self.image_url and not self.image_file:
            result = urllib.urlretrieve(self.image_url)
            self.image_file.save(
                os.path.basename(self.image_url),
                File(open(result[0]))
            )
            # self.save()

    def save(self, *args, **kwargs):
        self.get_remote_image()
        super(Image, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # You have to prepare what you need before delete the model
        storage, path = self.image_file.storage, self.image_file.path
        # Delete the model before the file
        super(Image, self).delete(*args, **kwargs)
        # Delete the file after the model
        storage.delete(path)


class Product(models.Model):
    name = models.CharField(max_length=254)
    slug = models.SlugField(max_length=255, blank=True)
    description = models.TextField(null=True, blank=True)
    rating = models.FloatField(null=True)
    brand = models.ForeignKey(Brand, null=True)
    images = models.ManyToManyField(Image, related_name='products')
    categories = models.ManyToManyField(Category, related_name='products')
    attributes = JSONField(null=True)
    stores = models.ManyToManyField(Store, through='ProductInfo', related_name='products')
    # new = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        unique_slugify(self, self.name)
        super(Product, self).save(*args, **kwargs)

    def get_all_categories(self):
        return list(self.categories.all()[0].get_ancestors(include_self=True))

    def serialize(self):
        dct = {
            'name': self.name,
            'description': self.description,
            'slug': self.slug,
            'info': [],
            'images': [],
            'categories': self.get_all_categories(),
        }
        for info in self.info.all():
            dct['info'].append(info.serialize())
        for image in self.images.all():
            dct['images'].append(image.image_file.url)
        return dct



class ProductInfo(models.Model):
    product = models.ForeignKey(Product, related_name='info')
    code = models.CharField(max_length=100, null=True)
    # rating
    # reviews
    store = models.ForeignKey(Store)
    availability = models.IntegerField()
    original_price = models.FloatField(null=True)
    price = models.FloatField()
    currency = models.ForeignKey(Currency)
    vendor = models.ForeignKey(Vendor, null=True)
    purchase_url = models.CharField(max_length=254)

    def get_availability(self):
        if self.availability == 0:
            return 'In Stock'
        elif self.availability == -1:
            return 'Out of Stock'
        return self.availability

    def __str__(self):
        return self.product.name + ' on ' + self.store.name

    def serialize(self):
        return {
            'price': self.price,
            'original_price': self.original_price,
            'availability': self.availability,
            'purchase_url': self.purchase_url,
            'store': self.store.name,
            'get_availability': self.get_availability(),
        }