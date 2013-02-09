from json import dumps, loads
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import URLError

from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.views.generic import View
from django.contrib.sites.models import Site
from browserid import settings as browserid_settings


class HttpResponseConflict(HttpResponse):
    status = 409


class StatusView(View):

    def post(self, request):
        site = Site.objects.get_current()
        protocol = 'https' if request.is_secure() else 'http'
        audience = '%s://%s' % (protocol, site.domain)
        assertion = request.POST.get('assertion', None)

        if assertion is None:
            data = {
                "status": "failed",
                "reason": "Missing assertion"
            }
            return HttpResponseBadRequest(
                dumps(data, indent=4),
                content_type='application/json'
            )
        else:

            data = {
                "assertion": assertion,
                "audience": audience
            }

            verifier_url = browserid_settings.PERSONA_VERIFIER_URL

            try:
                response = urlopen(
                    verifier_url, 
                    data=urlencode(data).encode('utf8')
                )

                body = response.readlines()
                body = ''.join([line.decode('utf8') for line in body])

                data = loads(body)
                
                #FIXME: Store assertion associated to user
                return HttpResponseConflict(
                    data,
                    content_type='application/json'
                )

            except ValueError:
                data = {
                    "status": "failed",
                    "reason": "Invalid response from server"
                }
                return HttpResponseConflict()
            except URLError:
                data = {
                    "status": "failed",
                    "reason": "Failed to connect to %s" % verifier_url}

            return HttpResponseConflict(
                dumps(data, indent=4),
                content_type='application/json'
            )