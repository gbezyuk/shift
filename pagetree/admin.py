from django.contrib import admin
from feincms.admin import tree_editor
from django.utils.translation import ugettext_lazy as _
from .models import Page

class PageAdmin(tree_editor.TreeEditor):
    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js',
        ]

    save_on_top = True
    save_as = False

    list_display = (
        'title',
        'url',
        'is_enabled',
        'created',
        'modified',
    )
    list_display_links = (
        'title',
        'url',
    )
    list_editable = (
        'is_enabled',
    )
    list_filter = (
        'is_enabled',
        'parent',
    )
    list_per_page = 500

    search_fields = (
        'title',
        'url',
        'content',
    )


    def enable(self, request, queryset):
        queryset.update(is_enabled=True)
    enable.short_description = _('enable')

    def disable(self, request, queryset):
        queryset.update(is_enabled=False)
    disable.short_description = _('disable')

admin.site.register(Page, PageAdmin)