from django.contrib import admin

from Acesso_Restrito.models import *

# Register your models here.
admin.site.register(
    (
        CM_associa_grupo_permissao,
        CM_banco,
        CM_dados_bancarios,
        CM_cidade,
        CM_pessoa,
        CM_pessoa_documentacao,
    )
)