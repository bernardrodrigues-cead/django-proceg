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
    
    path('editais/cadastro', views.PR_editalCreate, name='pr_edital-create'),
    path('editais/consulta', views.PR_editalListView.as_view(), name='pr_edital-list'),
    path('editais/<int:pr_edital_id>/editar', views.PR_editalUpdateView, name='pr_edital-update'),
    path('editais/<int:pk>/excluir', views.PR_editalDeleteView.as_view(), name='pr_edital-delete'),
    path('editais/vincular_usuario', views.PR_associa_usuario_editalListView, name='pr_associa_usuario_edital-list'),
    path('editais/vincular_usuario/<int:user_id>', views.PR_associa_usuario_editalUpdateView, name='pr_associa_usuario_edital-update'),
    path('editais/etapas/cadastro', views.PR_etapaCreate.as_view(), name='pr_etapa-create'),
    path('editais/etapas/consulta', views.PR_etapaListView.as_view(), name='pr_etapa-list'),
    path('editais/etapas/<int:pk>/editar', views.PR_etapaUpdateView.as_view(), name='pr_etapa-update'),
    path('editais/etapas/<int:pk>/excluir', views.PR_etapaDeleteView.as_view(), name='pr_etapa-delete'),
    path('editais/<int:edital_id>/vincular_etapas', views.VincularEtapasView, name='vincular_etapas'),
    path('editais/<int:edital_id>/vincular_etapas/<int:vaga_id>', views.PR_associa_vaga_etapaUpdateView, name='pr_associa_vaga_etapa-update'),
]