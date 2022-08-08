from django.urls import path

from Viagens import views

urlpatterns = [
    path('', views.ViagemView, name='viagem'),
    path('endereco/consulta', views.VI_enderecoListView.as_view(), name='vi_endereco-list'),
    path('endereco/cadastro', views.VI_enderecoCreate.as_view(), name='vi_endereco-create'),
    path('endereco/<int:pk>/editar', views.VI_enderecoUpdateView.as_view(), name='vi_endereco-update'),
    path('endereco/<int:pk>/excluir', views.VI_enderecoDeleteView.as_view(), name='vi_endereco-delete'),
    path('os/consulta', views.VI_osListView, name='vi_os-list'),
    path('os/cadastro', views.VI_osCreate, name='vi_os-create'),
    path('os/<int:os_id>/editar', views.VI_osUpdateView, name="vi_os-update"),
    path('os/<int:pk>/excluir', views.VI_osDeleteView.as_view(), name="vi_os-delete"),    
    path('os/pendentes', views.VI_osPendentesListView.as_view(), name='vi_os_pendentes-list'),
    path('os/aprovados', views.VI_osAprovadosListView.as_view(), name='vi_os_aprovados-list'),
    path('os/reprovados', views.VI_osReprovadosListView.as_view(), name='vi_os_reprovados-list'),
    path('os/<int:pk>/aprovacao', views.VI_osAprovacao.as_view(), name='vi_os-aprovacao'),
]