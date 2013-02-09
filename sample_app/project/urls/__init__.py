from django.conf import settings
from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^', include('myapp.urls')),
    url(r'^', include('browserid.urls')),
)

from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
