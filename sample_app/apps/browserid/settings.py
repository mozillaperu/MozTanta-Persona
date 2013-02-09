from django.conf import settings
from browserid import constants

VERIFIER_URL = getattr(
    settings,
    'PERSONA_VERIFIER_URL',
    constants.PERSONA_VERIFIER_URL
)