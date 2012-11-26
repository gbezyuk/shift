# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Price', fields ['product', 'specific_value', 'size', 'color']
        db.delete_unique('catalog_price', ['product_id', 'specific_value', 'size_id', 'color_id'])

        # Deleting model 'Price'
        db.delete_table('catalog_price')

        # Deleting model 'Color'
        db.delete_table('catalog_color')

        # Adding model 'Shipment'
        db.create_table('catalog_shipment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(related_name='prices', to=orm['catalog.Product'])),
            ('size', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='prices', null=True, to=orm['catalog.Size'])),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('remainder', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('special_price', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('catalog', ['Shipment'])

        # Adding unique constraint on 'Shipment', fields ['product', 'special_price', 'size']
        db.create_unique('catalog_shipment', ['product_id', 'special_price', 'size_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Shipment', fields ['product', 'special_price', 'size']
        db.delete_unique('catalog_shipment', ['product_id', 'special_price', 'size_id'])

        # Adding model 'Price'
        db.create_table('catalog_price', (
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(related_name='prices', to=orm['catalog.Product'])),
            ('color', self.gf('django.db.models.fields.related.ForeignKey')(related_name='prices', null=True, to=orm['catalog.Color'], blank=True)),
            ('remainder', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('size', self.gf('django.db.models.fields.related.ForeignKey')(related_name='prices', null=True, to=orm['catalog.Size'], blank=True)),
            ('specific_value', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('added_to_cart_times', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('note', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('ordered_times', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal('catalog', ['Price'])

        # Adding unique constraint on 'Price', fields ['product', 'specific_value', 'size', 'color']
        db.create_unique('catalog_price', ['product_id', 'specific_value', 'size_id', 'color_id'])

        # Adding model 'Color'
        db.create_table('catalog_color', (
            ('code', self.gf('django.db.models.fields.CharField')(default='#000', max_length=100, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default='black', unique=True, max_length=100, null=True, blank=True)),
            ('title_en', self.gf('django.db.models.fields.CharField')(default='black', unique=True, max_length=100, null=True, blank=True)),
            ('title_ru', self.gf('django.db.models.fields.CharField')(default='black', unique=True, max_length=100, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('catalog', ['Color'])

        # Deleting model 'Shipment'
        db.delete_table('catalog_shipment')


    models = {
        'catalog.category': {
            'Meta': {'ordering': "['tree_id', 'lft']", 'object_name': 'Category'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_ru': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name_ru': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['catalog.Category']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'catalog.image': {
            'Meta': {'ordering': "['title']", 'object_name': 'Image'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'max_length': '500'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'priority': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'})
        },
        'catalog.product': {
            'Meta': {'ordering': "['name']", 'object_name': 'Product'},
            'also_they_buy_with_this_product': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'also_they_buy_with_this_product_rel_+'", 'null': 'True', 'to': "orm['catalog.Product']"}),
            'base_price': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'products'", 'null': 'True', 'to': "orm['catalog.Category']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_ru': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name_ru': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'you_might_be_interested': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'you_might_be_interested_rel_+'", 'null': 'True', 'to': "orm['catalog.Product']"})
        },
        'catalog.shipment': {
            'Meta': {'ordering': "['product', 'enabled', 'special_price']", 'unique_together': "[('product', 'special_price', 'size')]", 'object_name': 'Shipment'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'prices'", 'to': "orm['catalog.Product']"}),
            'remainder': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'size': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'prices'", 'null': 'True', 'to': "orm['catalog.Size']"}),
            'special_price': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'catalog.size': {
            'Meta': {'ordering': "['title']", 'object_name': 'Size'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['catalog']