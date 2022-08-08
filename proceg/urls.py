"""proceg URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
# from django.conf.urls import url
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
# from django.views.static import serve
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('procead/', include('procead.urls')),
    path('curso/', include('Curso.urls')),
    path('polo/', include('Polo.urls')),
    path('financeiro/', include('Financeiro.urls')),
    path('viagem/', include('Viagens.urls')),
    path('administracao/', include('Acesso_Restrito.urls')),
    path('curso/', include('Curso.urls')),
    path('almoxarifado/', include('Almoxarifado.urls')),
    path('ticket/', include('Ticket.urls')),
    path('', RedirectView.as_view(url='procead/', permanent=True)),
    path('accounts/', include('django.contrib.auth.urls')),
    ### Add Django site authentication urls (for login, logout, password management)
        # accounts/login/ [name='login']
        # accounts/logout/ [name='logout']
        # accounts/password_change/ [name='password_change']
        # accounts/password_change/done/ [name='password_change_done']
        # accounts/password_reset/ [name='password_reset']
        # accounts/password_reset/done/ [name='password_reset_done']
        # accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
        # accounts/reset/done/ [name='password_reset_complete']
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )