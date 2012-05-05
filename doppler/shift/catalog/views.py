"""
Studio: Doppler
Product: Shift e-commerce engine
Module: Catalog
Part: Views implementation
"""
from django.http import HttpResponse

def index(request):
    return HttpResponse(content='catalog index')