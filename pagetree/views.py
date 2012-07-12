from django.template import loader, RequestContext
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponse, HttpResponsePermanentRedirect
from django.conf import settings
from django.core.xheaders import populate_xheaders
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_protect
from .models import Page

DEFAULT_TEMPLATE = 'page_default.haml'

def page(request, url):
    """
    Public interface to the page view.
    This view is called from PageFallbackMiddleware.process_response
    when a 404 is raised, which often means CsrfViewMiddleware.process_view
    has not been called even if CsrfViewMiddleware is installed. So we need
    to use @csrf_protect, in case the template needs {% csrf_token %}.
    However, we can't just wrap this view; if no matching flatpage exists,
    or a redirect is required for authentication, the 404 needs to be returned
    without any CSRF checks. Therefore, we only CSRF protect the internal implementation.
    """
    if not url.startswith('/'):
        url = '/' + url
    try:
        page = get_object_or_404(Page, url__exact=url, is_enabled=True)
    except Http404:
        if not url.endswith('/') and settings.APPEND_SLASH:
            url += '/'
            get_object_or_404(Page, url__exact=url, is_enabled=True)
            return HttpResponsePermanentRedirect('%s/' % request.path)
        else:
            raise
    if page.is_inside_disabled_parent:
        raise Http404
    return render_page(request, page)

@csrf_protect
def render_page(request, page):
    """
    Internal interface to the page view. CSRF protected explicitly.
    """
    t = loader.get_template(DEFAULT_TEMPLATE)

    # To avoid having to always use the "|safe" filter in flatpage templates,
    # mark the title and content as already safe (since they are raw HTML
    # content in the first place).
    page.title = mark_safe(page.title)
    page.content = mark_safe(page.content)

    c = RequestContext(request, {
        'page': page,
    })
    response = HttpResponse(t.render(c))
    populate_xheaders(request, response, Page, page.id) # dunno wat
    return response