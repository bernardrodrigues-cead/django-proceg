from django import forms

from Ticket.models import MensagemSolicitacao, Solicitacao, SolicitacaoDisciplina
class SolicitacaoForm(forms.ModelForm):
    class Meta:
        model = Solicitacao
        fields = [
            'categoria',
            'assunto',
            'anexo',

            'data_abertura',
            'solicitante',
            'ultima_alteracao'
        ]

class MensagemSolicitacaoForm(forms.ModelForm):
    CHOICES = (
        ('P', 'Pendente'),
        ('F', 'Fechado')
    )
    
    status = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, required=False, initial="F")
    encerrar = forms.BooleanField(required=False)
    class Meta:
        model = MensagemSolicitacao
        fields = [
            'autor',
            'data_mensagem',
            'mensagem',
            'solicitacao'
        ]

class RelatorioForm(forms.Form):
    data_inicio = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    data_fim = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))

class SolicitacaoDisciplinaForm(forms.ModelForm):
    possui_turma = forms.BooleanField(label="As turmas devem ser separadas por grupos?", required=False)
    importar_conteudo_passado = forms.BooleanField(label="É necessário importar conteúdo de períodos passados?", required=False)

    class Meta:
        model = SolicitacaoDisciplina
        fields = [
            'professor_responsavel',
            'siape',
            'unidade_lotacao',
            'categoria',
            'codigo_siga',
            'nome_disciplina',
            'tipo_curso',
            'curso_disciplina',
            'departamento_disciplina',
            'ano',
            'semestre',
            'turma',
            'conteudo_passado',
            'modo_inscricao_alunos',
            'atividades_inicio',
            'atividades_fim',
            # 'observacao'
        ]