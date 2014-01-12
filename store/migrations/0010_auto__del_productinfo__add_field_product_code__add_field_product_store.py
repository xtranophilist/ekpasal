# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'ProductInfo'
        db.delete_table(u'store_productinfo')

        # Adding field 'Product.code'
        db.add_column(u'store_product', 'code',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True),
                      keep_default=False)

        # Adding field 'Product.store'
        db.add_column(u'store_product', 'store',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['store.Store']),
                      keep_default=False)

        # Adding field 'Product.availability'
        db.add_column(u'store_product', 'availability',
                      self.gf('django.db.models.fields.IntegerField')(default=None),
                      keep_default=False)

        # Adding field 'Product.original_price'
        db.add_column(u'store_product', 'original_price',
                      self.gf('django.db.models.fields.FloatField')(null=True),
                      keep_default=False)

        # Adding field 'Product.price'
        db.add_column(u'store_product', 'price',
                      self.gf('django.db.models.fields.FloatField')(default=None),
                      keep_default=False)

        # Adding field 'Product.currency'
        db.add_column(u'store_product', 'currency',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['store.Currency']),
                      keep_default=False)

        # Adding field 'Product.vendor'
        db.add_column(u'store_product', 'vendor',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['store.Vendor'], null=True),
                      keep_default=False)

        # Adding field 'Product.purchase_url'
        db.add_column(u'store_product', 'purchase_url',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=254),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'ProductInfo'
        db.create_table(u'store_productinfo', (
            ('original_price', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['store.Product'])),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('vendor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['store.Vendor'], null=True)),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            ('purchase_url', self.gf('django.db.models.fields.CharField')(max_length=254)),
            ('currency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['store.Currency'])),
            ('availability', self.gf('django.db.models.fields.IntegerField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('store', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['store.Store'])),
        ))
        db.send_create_signal(u'store', ['ProductInfo'])

        # Deleting field 'Product.code'
        db.delete_column(u'store_product', 'code')

        # Deleting field 'Product.store'
        db.delete_column(u'store_product', 'store_id')

        # Deleting field 'Product.availability'
        db.delete_column(u'store_product', 'availability')

        # Deleting field 'Product.original_price'
        db.delete_column(u'store_product', 'original_price')

        # Deleting field 'Product.price'
        db.delete_column(u'store_product', 'price')

        # Deleting field 'Product.currency'
        db.delete_column(u'store_product', 'currency_id')

        # Deleting field 'Product.vendor'
        db.delete_column(u'store_product', 'vendor_id')

        # Deleting field 'Product.purchase_url'
        db.delete_column(u'store_product', 'purchase_url')


    models = {
        u'store.brand': {
            'Meta': {'object_name': 'Brand'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'foreign': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'rating': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'store.category': {
            'Meta': {'object_name': 'Category'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['store.Category']"}),
            'plural_name': ('django.db.models.fields.CharField', [], {'max_length': '154', 'null': 'True', 'blank': 'True'}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'blank': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'store.currency': {
            'Meta': {'object_name': 'Currency'},
            'exchange_rate': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        u'store.image': {
            'Meta': {'object_name': 'Image'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_file': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'image_url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'store.product': {
            'Meta': {'object_name': 'Product'},
            'attributes': ('jsonfield.fields.JSONField', [], {'null': 'True'}),
            'availability': ('django.db.models.fields.IntegerField', [], {}),
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['store.Brand']", 'null': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'products'", 'symmetrical': 'False', 'to': u"orm['store.Category']"}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['store.Currency']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'products'", 'symmetrical': 'False', 'to': u"orm['store.Image']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'original_price': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'purchase_url': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'rating': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'blank': 'True'}),
            'store': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['store.Store']"}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'vendor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['store.Vendor']", 'null': 'True'}),
            'views': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'store.store': {
            'Meta': {'object_name': 'Store'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'rating': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'blank': 'True'}),
            'status': ('django.db.models.fields.BooleanField', [], {})
        },
        u'store.vendor': {
            'Meta': {'object_name': 'Vendor'},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'foreign': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'rating': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'blank': 'True'})
        }
    }

    complete_apps = ['store']