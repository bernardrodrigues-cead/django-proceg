from django import forms

from Ticket.models import MensagemSolicitacao, Solicitacao, SolicitacaoCurso, SolicitacaoDisciplina
from procead.models import SN
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
    criar_grupos = forms.ChoiceField(choices=SN, label="As turmas devem ser separadas por grupos?", initial=0)
    importar_conteudo_passado = forms.BooleanField(label="É necessário importar conteúdo de períodos passados?", required=False)

    class Meta:
        model = SolicitacaoDisciplina
        fields = [
            'professor_responsavel',
            'email',
            'siape',
            'unidade_lotacao',
            'categoria',
            'codigo_siga',
            'ano',
            'semestre',
            'turma',
            'grupos',
            'nome_disciplina',
            'tipo_curso',
            'curso_disciplina',
            'departamento_disciplina',
            'conteudo_passado',
            'modo_inscricao_alunos',
            'atividades_inicio',
            'atividades_fim',
        ]

class SolicitacaoCursoForm(forms.ModelForm):
    class Meta:
        model = SolicitacaoCurso
        fields = [
            'professor_responsavel',
            'siape',
            'unidade_lotacao',
            'nome_curso',
            'tipo_curso',
            'caracteristicas',
            'qtd_disciplinas',
            'inscricoes_inicio',
            'inscricoes_fim',
            'curso_inicio',
            'curso_fim',
            'professores',
            'tutores',
            'demais_colaboradores',
            'alunos',
            'criacao_AVA',
            'matricula_alunos',
            'capacitacao_interlocutores',
            'outra',
            'producao_material',
            'assessoria_comunicacao',
            'ambiente_pre_formatado',
        ]
        widgets = {
            'outra': forms.TextInput(attrs={'placeholder': 'Especificar em caso de demanda adicional'}),
            'inscricoes_inicio': forms.widgets.DateInput(attrs={'type': 'date'}),
            'inscricoes_fim': forms.widgets.DateInput(attrs={'type': 'date'}),
            'curso_inicio': forms.widgets.DateInput(attrs={'type': 'date'}),
            'curso_fim': forms.widgets.DateInput(attrs={'type': 'date'}),
            'professores': forms.widgets.NumberInput(attrs={'class': 'num'}),
            'tutores': forms.widgets.NumberInput(attrs={'class': 'num'}),
            'demais_colaboradores': forms.widgets.NumberInput(attrs={'class': 'num'}),
            'alunos': forms.widgets.NumberInput(attrs={'class': 'num'}),
            'qtd_disciplinas': forms.widgets.NumberInput(attrs={'class': 'num'}),
        }

class SolicitacaoAprovacaoForm(forms.Form):
    aprovacao = forms.CharField()