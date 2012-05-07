"""
Studio: Doppler
Product: Shift e-commerce engine
Module: Base
Part: Admin implementation
"""
from django.contrib.admin import ModelAdmin

class TinyMCEAdmin(ModelAdmin):
    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js',
            ]
