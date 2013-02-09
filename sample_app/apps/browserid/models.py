from django.db import models
from django.contrib.auth.models import User
from browserid import strings

class Nonce(models.Model):

    user = models.ForeignKey(User,
        verbose_name=strings.NONCE_USER
    )

    assertion = models.CharField(
        verbose_name=strings.NONCE_ASSERTION,
        max_length=512,
        unique=True
    )

    created = models.DateTimeField(
        verbose_name=strings.NONCE_CREATED,
        auto_now_add=True
    )
       
    def __str__(self):
        return strings.NONCE_UNICODE.format(
            assertion=self.assertion, 
            email=self.user.email
        )

    class Meta:
        verbose_name = strings.NONCE_VERBOSE_NAME
        verbose_name_plural = strings.NONCE_VERBOSE_NAME_PLURAL

