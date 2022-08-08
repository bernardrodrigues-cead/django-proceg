from django.contrib import admin

from Viagens.models import VI_endereco, VI_os

# Register your models here.
admin.site.register(
    (    
        VI_os,
        VI_endereco
    )
)