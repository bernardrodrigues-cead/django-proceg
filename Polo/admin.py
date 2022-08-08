from django.contrib import admin

from Polo.models import CM_polo, SI_ies, SI_mantenedor

# Register your models here.
admin.site.register(
    (    
        SI_mantenedor,
        SI_ies,
        CM_polo,
    )
)