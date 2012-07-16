from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.generic import TemplateView
from doppler.shift.catalog.models import Category

def home(request, template_name='home.haml'):
    return render_to_response(
        template_name,
        {},
        context_instance=RequestContext(request)
    )

def handler404(request, template_name='404.haml'):
    return render_to_response(
        template_name,
            {},
        context_instance=RequestContext(request)
    )

def handler500(request, template_name='500.haml'):
    return render_to_response(
        template_name,
            {},
        context_instance=RequestContext(request)
    )

def google_site_verification(request):
    return HttpResponse('google-site-verification: googleca70414f1dff2fd9.html')