from json import dumps, loads
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import URLError

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseBadRequest
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.template import loader
from django.views.generic import View
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.backends import ModelBackend
from django.conf import settings

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

    def get_domain(self):
        domain = getattr(settings, 'SITE_DOMAIN', None)
        if domain is None:
            try:
                domain = Site.objects.get_current()
            except Site.DoesNotExist:
                domain = self.request.META['SERVER_NAME']
        return domain

    def format_audience(self):
        #site = Site.objects.get_current()
        protocol = 'https' if self.request.is_secure() else 'http'
        result = '{protocol}://{domain}'.format(
            protocol=protocol, 
            domain=self.get_domain()
        )
        if self.request.META['SERVER_PORT'] != '80':
            result = '{result}:{port}'.format(
                result=result,
                port=self.request.META['SERVER_PORT']
            )

        print(result)
        return result

    def bad_request(self):
        data = {
            "status": "failed",
            "reason": "Missing assertion"
        }
        t = loader.get_template('status.html')
        c = RequestContext(self.request, data)
        return HttpResponseBadRequest(t.render(c))

    def get_verifier_url(self):
        return browserid_settings.PERSONA_VERIFIER_URL

    def get_verifier_data(self, assertion):

        audience = self.format_audience()

        data = dict(assertion=assertion, audience=audience)

        try:
            response = urlopen(
                self.get_verifier_url(), 
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
        t = loader.get_template('status.html')
        c = RequestContext(self.request, data)
        return HttpResponseConflict(t.render(c))

    def create_nonce(self, assertion, data):
        user = User.objects.get(email=data['email'])
        nonce = Nonce(user=user, assertion=assertion)
        nonce.save()
        return nonce

    def nonce_error(self, data):
        aux = {
            "status": "failed",
            "reason": "No registered user with email {email}".format(
                email=data['email']
            )
        }
        return self.error_response(aux)

    def redirect_home(self):
        homepage = reverse('homepage')
        return HttpResponseRedirect(homepage)

    def get_default_auth_backend(self):
        return 'django.contrib.auth.backends.ModelBackend'

    def start_session_from_nonce(self, nonce):
        nonce.user.backend = self.get_default_auth_backend()
        login(self.request, nonce.user)

    def start_session_from_email(self, email):
        user = User.objects.get(email=email)
        user.backend = self.get_default_auth_backend()
        login(self.request, user)

    # HTTP Verb handlers

    def post(self, request):
        
        if not self.has_assertion():
            return self.bad_request()
        
        assertion = self.get_assertion()            
        data = self.get_verifier_data(assertion)

        if self.verification_was_successful(data):
            try:
                if browserid_settings.CREATE_NONCE:
                    nonce = self.create_nonce(assertion, data)
                    self.start_session_from_nonce(nonce)
                else:
                    self.start_session_from_email(data['email'])
                return self.redirect_home()
            except User.DoesNotExist:
                return self.nonce_error(data)
        else:
            return self.error_response(data)