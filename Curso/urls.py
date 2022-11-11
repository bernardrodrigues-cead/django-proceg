from django.urls import path

from Curso import views

urlpatterns = [
    path('', views.CursoView, name='curso'),
    
    path('cursos/consulta', views.CM_cursoListView.as_view(), name='cm_curso-list'),
    path('cursos/consulta/<int:cm_curso_id>/curso_oferta', views.curso_ofertaView, name='curso_oferta'),
    path('cursos/cadastro', views.CM_cursoCreate.as_view(), name='cm_curso-create'),
    path('cursos/<int:pk>', views.CM_cursoDetailView.as_view(), name='cm_curso-detail'),
    path('cursos/<int:pk>/editar', views.CM_cursoUpdateView.as_view(), name='cm_curso-update'),
    path('cursos/<int:pk>/excluir', views.CM_cursoDeleteView.as_view(), name='cm_curso-delete'),
    
    path('ofertas/consulta', views.SI_curso_ofertaListView.as_view(), name='si_curso_oferta-list'),
    path('ofertas/cadastro', views.SI_curso_ofertaCreate, name='si_curso_oferta-create'),
    path('ofertas/<int:pk>', views.SI_curso_ofertaDetailView.as_view(), name='si_curso_oferta-detail'),
    path('ofertas/<int:si_curso_oferta_id>/editar', views.SI_curso_ofertaUpdateView, name='si_curso_oferta-update'),
    path('ofertas/<int:pk>/excluir', views.SI_curso_ofertaDeleteView.as_view(), name='si_curso_oferta-delete'),
]