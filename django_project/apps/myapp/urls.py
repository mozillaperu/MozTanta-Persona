from django.conf.urls import patterns, url

from myapp import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name="homepage")
)
