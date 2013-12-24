from django.db import models


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
    foreign = models.BooleanField(null=True)

    def __unicode__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(null=True)
    image = models.ImageField(upload_to='images/stores/', null=True)
    rating = models.FloatField(null=True)
    foreign = models.BooleanField(null=True)

    def __unicode__(self):
        return self.name


class Currency(models.Model):
    name = models.CharField(max_length=50)
    short_name = models.CharField(max_length=5)
    exchange_rate = models.FloatField()

    def __unicode__(self):
        return self.name