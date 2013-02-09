from json import dumps, loads
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import URLError

from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.views.generic import View
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from browserid import settings as browserid_settings
from browserid.models import Nonce

class HttpResponseConflict(HttpResponse):
    status = 409


class StatusView(View):

    ASSERTION_KEY = 'assertion'

    # Utils
    def has_assertion(self):
        return self.ASSERTION_KEY in self.request.POST

    def get_assertion(self):
        return self.request.POST[self.ASSERTION_KEY]

    def format_audience(self):
        site = Site.objects.get_current()
        protocol = 'https' if request.is_secure() else 'http'
        return '%s://%s' % (protocol, site.domain)

    def bad_request(self):
        data = {
            "status": "failed",
            "reason": "Missing assertion"
        }
        return HttpResponseBadRequest(
            dumps(data, indent=4),
            content_type='application/json'
        )

    def get_verifier_url(self):
        return browserid_settings.PERSONA_VERIFIER_URL

    def get_verifier_data(self, assertion):

        audience = self.format_audience()

        data = dict(assertion=assertion, audience=audience)

        try:
            response = urlopen(
                verifier_url, 
                data=urlencode(data).encode('utf8')
            )

            body = response.readlines()
            body = ''.join([line.decode('utf8') for line in body])

            return loads(body)

        except ValueError:
            return {
                "status": "failed",
                "reason": "Invalid response from server"
            }
            
        except URLError:
            return {
                "status": "failed",
                "reason": "Failed to connect to {verifier_url}".assertion({
                    "verifier_url": verifier_url
                })
            }

    def verification_was_successful(self, data):   
        if 'status' not in data:
            return False

        return data['status'] == 'okay'

    def error_response(self, data):
        return HttpResponseConflict(
            dumps(data, indent=4),
            content_type='application/json'
        )

    def create_nonce(self, data):
        user = User.objects.get(email=email)
        nonce = Nonce(user=user, assertion=assertion)
        nonce.save()
        return nonce

    def nonce_error(self, data):
        aux = {
            "status": "failed",
            "reason": "No registered used with email {email}".assertion({
                "email": data['email']
            })
        }
        return self.error_response(aux)

    def successful_response(self, data):
        return HttpResponse(
            dumps(data, indent=4),
            content_type='application/json'
        )        

    # HTTP Verb handlers

    def post(self, request):
        
        if not self.has_assertion():
            return self.bad_request()
        
        assertion = self.get_assertion()            
        data = self.get_verifier_data(assertion)

        if self.verification_was_successful(data):
            try:
                self.create_nonce(data)
                return self.successful_response(data)
            except User.DoesNotExist:
                return self.nonce_error(data)
        else:
            return self.error_response(data)