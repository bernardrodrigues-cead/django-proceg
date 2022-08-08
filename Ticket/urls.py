from django.urls import path

from Ticket import views

urlpatterns = [
    path('', views.Solicitacoes, name='ticket'),
    path('solicitacao/consulta', views.SolicitacaoListView, name='ticket-list'),
    path('solicitacao/cadastro', views.SolicitacaoCreate, name='ticket-create'),
    path('solicitacao/<int:solicitacao_id>/edicao', views.SolicitacaoUpdateView, name='ticket-update'),
    path('solicitacao/<int:solicitacao_id>/assumir/<int:dev_id>', views.assumirSolicitacao, name='ticket-assumir'),
    path('solicitacao/<int:solicitacao_id>/encerrar/<int:dev_id>', views.encerrarSolicitacao, name='ticket-encerrar'),
    path('solicitacao/<int:solicitacao_id>/atualizar', views.atualizarSolicitacao, name='ticket-atualizar'),
    path('solicitacao/<int:solicitacao_id>/excluir', views.solicitacaoDeleteView, name='ticket-delete'),
    path('solicitacao/fechadas', views.FechadasListView, name='fechadas-list'),
    path('solicitacao/fechadas/consulta=<str:consulta>', views.FechadasListView, name='fechadas-list'),
    path('solicitacao/relatorios', views.solicitacaoRelatorio, name='ticket-relatorios'),
    path('solicitacao/relatorios/<str:intervalo>', views.solicitacaoRelatorio, name='ticket-relatorios'),
    path('solicitacao/relatorios/<str:consulta>', views.solicitacaoRelatorio, name='ticket-relatorios'),

    path('solicitacao/AVA', views.SolicitacaoAVA, name='ticket-ava'),
    path('solicitacao/AVA/disciplina/consulta', views.SolicitacaoDisciplinaListView, name='solicitacao-disciplina-list'),
    path('solicitacao/AVA/disciplina/cadastro', views.SolicitacaoDisciplinaCreate, name='solicitacao-disciplina-create'),
    path('setor', views.SetorCreate.as_view(), name='ticket-setor'),
]