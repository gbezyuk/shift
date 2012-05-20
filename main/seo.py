from rollyourown import seo
from django.utils.translation import ugettext as _

class MyMetadata(seo.Metadata):
    title       = seo.Tag(head=True, max_length=68)
    description = seo.MetaTag(max_length=155)
    keywords    = seo.KeywordTag()
    heading     = seo.Tag(name="h1")

    class Meta:
        use_sites = True
        use_cache = True
        use_i18n = True
        groups = {'optional': ('heading',)}
        verbose_name = _('metadata')
        verbose_name_plural = _('metadata')