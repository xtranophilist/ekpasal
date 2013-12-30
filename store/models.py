from django.db import models
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey
from jsonfield import JSONField


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
        self.slug = slugify(self.name)
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
        self.slug = slugify(self.name)
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
        self.slug = slugify(self.name)
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
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class Image(models.Model):
    image = models.ImageField(upload_to='images/products/', null=True)


class Product(models.Model):
    name = models.CharField(max_length=50)
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
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)


class ProductInfo(models.Model):
    product = models.ForeignKey(Product)
    code = models.CharField(max_length=100, null=True)
    store = models.ForeignKey(Store)
    availability = models.IntegerField()
    original_price = models.FloatField(null=True)
    price = models.FloatField()
    currency = models.ForeignKey(Currency)
    vendor = models.ForeignKey(Vendor, null=True)
    purchase_url = models.CharField(max_length=254)

    def __str__(self):
        return self.product.name + ' on ' + self.store.name