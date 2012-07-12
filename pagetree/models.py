from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel

class Page(MPTTModel):
    """
    Page
    """
    class Meta:
        # The TreeEditor needs this ordering definition
        ordering = ['tree_id', 'lft']
        verbose_name = _('page')
        verbose_name_plural = _('pages')

    url = models.CharField(max_length=255, verbose_name=_('URL'), null=False, unique=True, blank=False, default=_('/'))
    title = models.CharField(max_length=1000, verbose_name=_('title'), null=False, blank=False, default=_('new page'))
    content = models.TextField(verbose_name=_('content'), null=False, blank=False, default=_('put some html here'))
    is_enabled = models.BooleanField(verbose_name=_('is enabled'), null=False, blank=False, default=True)

    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', verbose_name=_('parent page'))

    created = models.DateTimeField(verbose_name=_('created'), auto_now_add=True)
    modified = models.DateTimeField(verbose_name=_('modified'), auto_now=True)

    @property
    def topmost_parent(self):
        result = self
        while result.parent:
            result = result.parent
        return result

    @property
    def is_inside_disabled_parent(self):
        """
        checks if any parent of current category is disabled
        """
        return self.get_ancestors().filter(is_enabled=False).exists()

    def get_absolute_url(self):
        return self.url

    def __unicode__(self):
        return self.title

    @property
    def enabled_children(self):
        return self.children.filter(is_enabled=True)