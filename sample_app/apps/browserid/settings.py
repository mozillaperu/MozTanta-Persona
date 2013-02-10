from django.conf import settings
from browserid import constants

PERSONA_VERIFIER_URL = getattr(
    settings,
    'PERSONA_VERIFIER_URL',
    constants.PERSONA_VERIFIER_URL
)

CREATE_NONCE = getattr(
    settings,
    'CREATE_NONCE',
    constants.CREATE_NONCE
)