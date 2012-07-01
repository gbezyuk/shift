from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.generic import TemplateView
from doppler.shift.catalog.models import Category

class HomeView(TemplateView):
    template_name = "home.haml"

class ViewFor404(TemplateView):
    template_name = "404.haml"

class ViewFor500(TemplateView):
    template_name = "500.haml"

def mens(request, template_name='doppler/shift/catalog/mens.haml'):
    return render_to_response(
        template_name,
        {'category': Category.enabled_root.get(pk=1)},
        context_instance=RequestContext(request)
    )

def womens(request, template_name='doppler/shift/catalog/womens.haml'):
    return render_to_response(
        template_name,
        {'category': Category.enabled_root.get(pk=2)},
        context_instance=RequestContext(request)
    )

def children(request, template_name='doppler/shift/catalog/children.haml'):
    return render_to_response(
        template_name,
        {'category': Category.enabled_root.get(pk=3)},
        context_instance=RequestContext(request)
    )

def to_customer(request, template_name='to_customer.haml'):
    return render_to_response(
        template_name,
        {},
        context_instance=RequestContext(request)
    )

def contacts(request, template_name='contacts.haml'):
    return render_to_response(
        template_name,
        {},
        context_instance=RequestContext(request)
    )