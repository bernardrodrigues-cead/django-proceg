from django.contrib import admin

from Acesso_Restrito.models import *

# Register your models here.
admin.site.register(
    (
        CM_banco,
        CM_dados_bancarios,
        CM_pessoa,
        CM_pessoa_documentacao,
    )
)