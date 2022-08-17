from django.contrib import admin

from Ticket.models import MensagemSolicitacao, Solicitacao, SolicitacaoCurso, SolicitacaoDisciplina

# Register your models here.
admin.site.register(
    (
        Solicitacao,
        MensagemSolicitacao,
        SolicitacaoCurso,
        SolicitacaoDisciplina
    )
)