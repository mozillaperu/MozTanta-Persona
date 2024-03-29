from django.conf.urls import patterns, url
from django.views.decorators.csrf import csrf_exempt
from browserid import views

urlpatterns = patterns('',
    url(r'^status/?$', csrf_exempt(views.StatusView.as_view()), name='status'),
    url(r'^logout/?$', 'django.contrib.auth.views.logout', name='logout')
)