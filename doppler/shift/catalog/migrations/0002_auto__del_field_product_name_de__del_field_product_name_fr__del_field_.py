# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Product.name_de'
        db.delete_column('catalog_product', 'name_de')

        # Deleting field 'Product.name_fr'
        db.delete_column('catalog_product', 'name_fr')

        # Deleting field 'Product.name_es'
        db.delete_column('catalog_product', 'name_es')

        # Deleting field 'Product.description_es'
        db.delete_column('catalog_product', 'description_es')

        # Deleting field 'Product.description_fr'
        db.delete_column('catalog_product', 'description_fr')

        # Deleting field 'Product.description_de'
        db.delete_column('catalog_product', 'description_de')

        # Adding field 'Product.category'
        db.add_column('catalog_product', 'category',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.Category'], null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Category.name_fr'
        db.delete_column('catalog_category', 'name_fr')

        # Deleting field 'Category.name_de'
        db.delete_column('catalog_category', 'name_de')

        # Deleting field 'Category.description_fr'
        db.delete_column('catalog_category', 'description_fr')

        # Deleting field 'Category.description_de'
        db.delete_column('catalog_category', 'description_de')

        # Deleting field 'Category.name_es'
        db.delete_column('catalog_category', 'name_es')

        # Deleting field 'Category.description_es'
        db.delete_column('catalog_category', 'description_es')

    def backwards(self, orm):
        # Adding field 'Product.name_de'
        db.add_column('catalog_product', 'name_de',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Product.name_fr'
        db.add_column('catalog_product', 'name_fr',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Product.name_es'
        db.add_column('catalog_product', 'name_es',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Product.description_es'
        db.add_column('catalog_product', 'description_es',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Product.description_fr'
        db.add_column('catalog_product', 'description_fr',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Product.description_de'
        db.add_column('catalog_product', 'description_de',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Product.category'
        db.delete_column('catalog_product', 'category_id')

        # Adding field 'Category.name_fr'
        db.add_column('catalog_category', 'name_fr',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_de'
        db.add_column('catalog_category', 'name_de',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_fr'
        db.add_column('catalog_category', 'description_fr',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_de'
        db.add_column('catalog_category', 'description_de',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.name_es'
        db.add_column('catalog_category', 'name_es',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.description_es'
        db.add_column('catalog_category', 'description_es',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

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
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'catalog.product': {
            'Meta': {'ordering': "['name']", 'object_name': 'Product'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.Category']", 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_ru': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name_ru': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['catalog']