from django.contrib import admin

from Financeiro.models import *

# Register your models here.
admin.site.register(
    (    
        FI_bolsa,
        CM_pessoa_bolsa,
    )
)