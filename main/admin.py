from rollyourown.seo.admin import register_seo_admin, auto_register_inlines
from django.contrib import admin
from .seo import MyMetadata

register_seo_admin(admin.site, MyMetadata)
auto_register_inlines(admin.site, MyMetadata)