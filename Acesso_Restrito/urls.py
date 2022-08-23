from django.urls import path

from Acesso_Restrito import views

urlpatterns = [
    path('', views.AdministracaoView, name='administracao'),
    
    path('pessoa/consulta', views.CM_pessoaListView, name='cm_pessoa-list'),
    path('pessoa/consulta=<str:consulta>', views.CM_pessoaListView, name='cm_pessoa-list'),
    path('pessoa/cadastro', views.CM_pessoaCreate, name='cm_pessoa-create'),
    path('pessoa/<int:pessoa_id>/editar', views.CM_pessoaUpdateView, name='cm_pessoa-update'),
    path('pessoa/<int:pk>/excluir', views.CM_pessoaDeleteView.as_view(), name='cm_pessoa-delete'),
    
    path('grupos/consulta', views.GrupoListView.as_view(), name='grupo-list'),
    path('grupos/cadastro', views.GrupoCreate.as_view(), name='grupo-create'),
    path('grupos/<int:pk>/editar', views.GrupoUpdateView.as_view(), name='grupo-update'),
    path('grupos/<int:pk>/excluir', views.GrupoDeleteView.as_view(), name='grupo-delete'),
    
    path('transacao/consulta', views.PermissaoListView.as_view(), name='permissao-list'),
    path('transacao/cadastro', views.PermissaoCreate.as_view(), name='permissao-create'),
    path('transacao/<int:pk>/editar', views.PermissaoUpdateView.as_view(), name='permissao-update'),
    path('transacao/<int:pk>/excluir', views.PermissaoDeleteView.as_view(), name='permissao-delete'),
    
    path('usuarios/consulta', views.UserView, name='user'),
    path('usuarios/<int:pessoa_id>/cadastro', views.UserCreateView, name='user-create'),
    path('usuarios/<int:user_id>/editar', views.UserUpdateView, name='user-update'),
    path('usuarios/<int:pk>/delete', views.UserDeleteView.as_view(), name='user-delete'),
    path('usuarios/<int:pk>/grupos', views.Usuario_grupoView.as_view(), name='user-grupo'),
    
    path('extra', views.CadastroAdicionalView, name='extra'),
    path('extra/fi_programa/consulta', views.FI_programaListView.as_view(), name='fi_programa-list'),
    path('extra/fi_programa/cadastro', views.FI_programaCreate.as_view(), name='fi_programa-create'),
    path('extra/fi_programa/<int:pk>/editar', views.FI_programaUpdateView.as_view(), name='fi_programa-update'),
    path('extra/fi_programa/<int:pk>/excluir', views.FI_programaDeleteView.as_view(), name='fi_programa-delete'),
    path('extra/si_tipo_curso/consulta', views.SI_tipo_cursoListView.as_view(), name='si_tipo_curso-list'),
    path('extra/si_tipo_curso/cadastro', views.SI_tipo_cursoCreate.as_view(), name='si_tipo_curso-create'),
    path('extra/si_tipo_curso/<int:pk>/editar', views.SI_tipo_cursoUpdateView.as_view(), name='si_tipo_curso-update'),
    path('extra/si_tipo_curso/<int:pk>/excluir', views.SI_tipo_cursoDeleteView.as_view(), name='si_tipo_curso-delete'),
    path('extra/si_curso_situacao/consulta', views.SI_curso_situacaoListView.as_view(), name='si_curso_situacao-list'),
    path('extra/si_curso_situacao/cadastro', views.SI_curso_situacaoCreate.as_view(), name='si_curso_situacao-create'),
    path('extra/si_curso_situacao/<int:pk>/editar', views.SI_curso_situacaoUpdateView.as_view(), name='si_curso_situacao-update'),
    path('extra/si_curso_situacao/<int:pk>/excluir', views.SI_curso_situacaoDeleteView.as_view(), name='si_curso_situacao-delete'),

    path('extra/funcionario/cadastro', views.FuncionarioCreate.as_view(), name='funcionario-create'),
    path('extra/funcionario/consulta', views.FuncionarioListView.as_view(), name='funcionario-list'),
    path('extra/funcionario/<int:pk>/editar', views.FuncionarioUpdateView.as_view(), name='funcionario-update'),
    path('extra/funcionario/<int:pk>/excluir', views.FuncionarioDeleteView.as_view(), name='funcionario-delete'),

    path('extra/setor/cadastro', views.SetorCreate.as_view(), name='setor-create'),
    path('extra/setor/consulta', views.SetorListView.as_view(), name='setor-list'),
    path('extra/setor/<int:pk>/editar', views.SetorUpdateView.as_view(), name='setor-update'),
    path('extra/setor/<int:pk>/excluir', views.SetorDeleteView.as_view(), name='setor-delete'),
]