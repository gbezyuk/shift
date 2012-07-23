from django.http import HttpResponse, HttpResponseServerError, HttpResponseNotFound
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.generic import TemplateView
from doppler.shift.catalog.models import Category
from django.template import loader

def home(request, template_name='home.haml'):
    return render_to_response(
        template_name,
        {},
        context_instance=RequestContext(request)
    )

def handler404(request, template_name = "404.haml"):
    """
    handles wrong path requests
    """
    return HttpResponseNotFound(loader.get_template(template_name).render(RequestContext(request)))

def handler500(request, template_name = "500.haml"):
    """
    Using custom HTTP 500 error page
    """
    return HttpResponseServerError(loader.get_template(template_name).render(RequestContext(request)))

def google_site_verification(request):
    return HttpResponse('google-site-verification: googleca70414f1dff2fd9.html')