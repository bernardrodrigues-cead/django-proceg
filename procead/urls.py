from django.urls import path
from . import views

"""Nessa página cadastram-se as URLs da aplicação:
    path(string(URL), View(View associada à URL), Name(Nome breve pelo qual a URL será chamada))
"""
urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/403', views.DeniedView, name='denied'),
    path('alterar-senha', views.alterar_senha, name='alterar-senha'),
]