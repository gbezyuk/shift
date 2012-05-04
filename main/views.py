from django.http import HttpResponse

from django.views.generic import TemplateView

class HomeView(TemplateView):
	template_name = "home.haml"

class ViewFor404(TemplateView):
	template_name = "404.haml"

class ViewFor500(TemplateView):
	template_name = "500.haml"