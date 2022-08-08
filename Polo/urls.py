from django.urls import path

from Polo import views

urlpatterns = [
    path('', views.PoloView, name='polo'),
    
    path('polos/consulta', views.CM_poloListView.as_view(), name='cm_polo-list'),
    path('polos/cadastro', views.CM_poloCreate.as_view(), name='cm_polo-create'),
    path('polos/<int:pk>/editar', views.CM_poloUpdateView.as_view(), name='cm_polo-update'),
    path('polos/<int:pk>/excluir', views.CM_poloDeleteView.as_view(), name='cm_polo-delete'),
    path('polos/<int:pk>/associarPoloIes', views.SI_associa_polo_iesUpdate.as_view(), name='si_associa_polo_ies-update'),
    
    path('ies/consulta', views.SI_iesListView.as_view(), name='si_ies-list'),
    path('ies/cadastro', views.SI_iesCreate.as_view(), name='si_ies-create'),
    path('ies/<int:pk>/editar', views.SI_iesUpdateView.as_view(), name='si_ies-update'),
    path('ies/<int:pk>/excluir', views.SI_iesDeleteView.as_view(), name='si_ies-delete'),
    
    path('mantenedor/consulta', views.SI_mantenedorListView.as_view(), name='si_mantenedor-list'),
    path('mantenedor/cadastro', views.SI_mantenedorCreate.as_view(), name='si_mantenedor-create'),
    path('mantenedor/<int:pk>/editar', views.SI_mantenedorUpdateView.as_view(), name='si_mantenedor-update'),
    path('mantenedor/<int:pk>/excluir', views.SI_mantenedorDeleteView.as_view(), name='si_mantenedor-delete'),
]