from django.contrib import admin

from Curso.models import *

# Register your models here.
admin.site.register(
    (    
        SI_tipo_curso,
        SI_curso_projeto,
        SI_curso_situacao,
        FI_orgao_fomento,
        FI_fonte_pagadora,
        FI_programa,
        CM_curso,
        SI_curso_oferta,
        SI_associa_curso_oferta_polo,
    )
)