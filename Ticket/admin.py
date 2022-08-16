from django.contrib import admin

from Ticket.models import Funcionario, MensagemSolicitacao, Solicitacao, SolicitacaoCurso, SolicitacaoDisciplina

# Register your models here.
admin.site.register(
    (
        Solicitacao,
        Funcionario,
        MensagemSolicitacao,
        SolicitacaoCurso,
        SolicitacaoDisciplina
    )
)