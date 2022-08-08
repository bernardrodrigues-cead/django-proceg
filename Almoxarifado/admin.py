from django.contrib import admin
from Almoxarifado.models import * 


# Register your models here.
admin.site.register(
    (    
        Produto,
        Categoria,
        Estoque,
        Saida_Produto,
        Entrada_Produto,         
    )
)