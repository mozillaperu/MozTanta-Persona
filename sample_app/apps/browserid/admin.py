from django.contrib import admin
from browserid.models import Nonce

class NonceAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'assertion', 'created', )
    search_fields = ('assertion', )

admin.site.register(Nonce, NonceAdmin)