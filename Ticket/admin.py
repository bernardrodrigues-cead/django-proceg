from django.contrib import admin

from Ticket.models import Funcionario, MensagemSolicitacao, Solicitacao, SolicitacaoCurso

# Register your models here.
admin.site.register(
    (
        Solicitacao,
        Funcionario,
        MensagemSolicitacao,
        SolicitacaoCurso
    )
)