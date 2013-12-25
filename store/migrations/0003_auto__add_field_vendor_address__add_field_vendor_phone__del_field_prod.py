# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Vendor.address'
        db.add_column(u'store_vendor', 'address',
                      self.gf('django.db.models.fields.TextField')(null=True),
                      keep_default=False)

        # Adding field 'Vendor.phone'
        db.add_column(u'store_vendor', 'phone',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True),
                      keep_default=False)

        # Deleting field 'Product.category'
        db.delete_column(u'store_product', 'category_id')

        # Adding M2M table for field categories on 'Product'
        m2m_table_name = db.shorten_name(u'store_product_categories')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('product', models.ForeignKey(orm[u'store.product'], null=False)),
            ('category', models.ForeignKey(orm[u'store.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['product_id', 'category_id'])


        # Changing field 'Product.description'
        db.alter_column(u'store_product', 'description', self.gf('django.db.models.fields.TextField')(null=True))
        # Adding field 'ProductInfo.code'
        db.add_column(u'store_productinfo', 'code',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=100),
                      keep_default=False)

        # Adding field 'ProductInfo.original_price'
        db.add_column(u'store_productinfo', 'original_price',
                      self.gf('django.db.models.fields.FloatField')(null=True),
                      keep_default=False)

        # Adding field 'ProductInfo.vendor'
        db.add_column(u'store_productinfo', 'vendor',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['store.Vendor']),
                      keep_default=False)

        # Adding field 'ProductInfo.purchase_url'
        db.add_column(u'store_productinfo', 'purchase_url',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=254),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Vendor.address'
        db.delete_column(u'store_vendor', 'address')

        # Deleting field 'Vendor.phone'
        db.delete_column(u'store_vendor', 'phone')

        # Adding field 'Product.category'
        db.add_column(u'store_product', 'category',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['store.Category']),
                      keep_default=False)

        # Removing M2M table for field categories on 'Product'
        db.delete_table(db.shorten_name(u'store_product_categories'))


        # Changing field 'Product.description'
        db.alter_column(u'store_product', 'description', self.gf('django.db.models.fields.CharField')(max_length=254, null=True))
        # Deleting field 'ProductInfo.code'
        db.delete_column(u'store_productinfo', 'code')

        # Deleting field 'ProductInfo.original_price'
        db.delete_column(u'store_productinfo', 'original_price')

        # Deleting field 'ProductInfo.vendor'
        db.delete_column(u'store_productinfo', 'vendor_id')

        # Deleting field 'ProductInfo.purchase_url'
        db.delete_column(u'store_productinfo', 'purchase_url')


    models = {
        u'store.brand': {
            'Meta': {'object_name': 'Brand'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'foreign': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'rating': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'})
        },
        u'store.category': {
            'Meta': {'object_name': 'Category'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['store.Category']"}),
            'plural_name': ('django.db.models.fields.CharField', [], {'max_length': '154', 'null': 'True'}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'store.currency': {
            'Meta': {'object_name': 'Currency'},
            'exchange_rate': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        u'store.product': {
            'Meta': {'object_name': 'Product'},
            'attributes': ('jsonfield.fields.JSONField', [], {}),
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['store.Brand']", 'null': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['store.Category']", 'symmetrical': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'rating': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'stores': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'products'", 'symmetrical': 'False', 'through': u"orm['store.ProductInfo']", 'to': u"orm['store.Store']"})
        },
        u'store.productinfo': {
            'Meta': {'object_name': 'ProductInfo'},
            'availability': ('django.db.models.fields.IntegerField', [], {}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['store.Currency']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original_price': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['store.Product']"}),
            'purchase_url': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'store': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['store.Store']"}),
            'vendor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['store.Vendor']"})
        },
        u'store.store': {
            'Meta': {'object_name': 'Store'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'rating': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
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
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['store']