from django.views.generic.base import TemplateView
from django.core.urlresolvers import reverse

class IndexView(TemplateView):
    template_name = 'index.html'