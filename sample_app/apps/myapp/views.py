from django.views.generic.base import TemplateView
from django.core.urlresolvers import reverse

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_url'] = reverse('login')
        context['logout_url'] = reverse('logout')
        context['status_url'] = reverse('status')
        return context