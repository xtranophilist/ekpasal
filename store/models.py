from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from jsonfield import JSONField


class Store(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(null=True)
    image = models.ImageField(upload_to='images/stores/', null=True)
    status = models.BooleanField()
    rating = models.FloatField(null=True)
    last_updated = models.DateTimeField()
    # products = models.ManyToManyField(Product, through='ProductInfo')

    def __unicode__(self):
        return self.name


class Vendor(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(null=True)
    address = models.TextField(null=True)
    phone = models.CharField(null=True, max_length=50)
    image = models.ImageField(upload_to='images/stores/', null=True)
    rating = models.FloatField(null=True)
    foreign = models.NullBooleanField()

    def __unicode__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(null=True)
    image = models.ImageField(upload_to='images/brands/', null=True)
    rating = models.FloatField(null=True)
    foreign = models.NullBooleanField()

    def __unicode__(self):
        return self.name


class Currency(models.Model):
    name = models.CharField(max_length=50)
    short_name = models.CharField(max_length=5)
    exchange_rate = models.FloatField()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = u'Currencies'


class Category(MPTTModel):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=255)
    image = models.ImageField(upload_to='images/categories/', null=True)
    description = models.CharField(max_length=254, null=True, blank=True)
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children')
    plural_name = models.CharField(max_length=154, null=True)

    def get_plural_name(self):
        return self.plural_name or self.name + 's'

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = u'Categories'


class Product(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=255)
    image = models.ImageField(upload_to='images/products/', null=True)
    description = models.TextField(null=True, blank=True)
    rating = models.FloatField(null=True)
    brand = models.ForeignKey(Brand, null=True)
    categories = models.ManyToManyField(Category)
    attributes = JSONField()
    stores = models.ManyToManyField(Store, through='ProductInfo', related_name='products')

    def __unicode__(self):
        return self.name


class ProductInfo(models.Model):
    product = models.ForeignKey(Product)
    code = models.CharField(max_length=100)
    store = models.ForeignKey(Store)
    availability = models.IntegerField()
    original_price = models.FloatField(null=True)
    price = models.FloatField()
    currency = models.ForeignKey(Currency)
    vendor = models.ForeignKey(Vendor)
    purchase_url = models.CharField(max_length=254)

    def __unicode__(self):
        return self.product.name + ' on ' + self.store.name