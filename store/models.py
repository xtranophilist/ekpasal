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

    def __unicode__(self):
        return self.name


class Vendor(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(null=True)
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
        verbose_name_plural = u'Inventory Categories'


class Product(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=255)
    image = models.ImageField(upload_to='images/products/', null=True)
    description = models.CharField(max_length=254, null=True, blank=True)
    rating = models.FloatField(null=True)
    brand = models.ForeignKey(Brand, null=True)
    category = models.ForeignKey(Category)
    attributes = JSONField()

    def __unicode__(self):
        return self.name