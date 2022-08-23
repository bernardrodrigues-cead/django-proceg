from django import forms
from Acesso_Restrito.models import CM_dados_bancarios, CM_pessoa_documentacao
from Curso.models import CM_pessoa

from Financeiro.models import CM_pessoa_bolsa

#####################################################
# FICHA UAB #
#####################################################

class passo1Form(forms.Form):
    cpf = forms.CharField(max_length=14)
    data_nascimento = forms.DateField()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cpf'].widget.attrs.update({'class': 'maskedCpf'})
        self.fields['cpf'].label = "CPF"
        self.fields['data_nascimento'].widget.attrs.update({'class': 'maskedDate'})
        self.fields['data_nascimento'].label = "Data de Nascimento"
        
class passo2Form(forms.Form):
    codigo = forms.CharField(max_length=6, widget=forms.PasswordInput)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['codigo'].label = "Código"
        
class passo3Form(forms.ModelForm):
    class Meta:
        model = CM_pessoa_bolsa
        fields = ['curso', 'bolsa']
        
class passo4FormPessoa(forms.ModelForm):
    class Meta:
        model = CM_pessoa
        fields = [
            'nome',
            'sexo',
            'cpf',
            'data_nascimento',
            'rua',
            'numero',
            'complemento',
            'bairro',
            'uf',
            'cidade',
            'cep',
            'email',
            'ddd1',
            'telefone1',
            'ddd2',
            'telefone2'
        ]

class passo4FormPessoaDocumentacao(forms.ModelForm):
    class Meta:
        model = CM_pessoa_documentacao
        fields = [
            'profissao',
            'tipo_documento',
            'documento',
            'data_emissao_documento',
            'orgao_expeditor_documento',
            'uf_nascimento',
            'cidade_nascimento',
            'nacionalidade',
            'estado_civil',
            'nome_conjuge',
            'nome_pai',
            'nome_mae',
            'area_ultimo_curso_superior',
            'ultimo_curso_titulacao',
            'instituicao_titulacao'
        ]
        widgets = {
            'data_emissao_documento': forms.widgets.DateInput(attrs={'type': 'date'}),
        }

class passo5Form(forms.ModelForm):
    class Meta:
        model = CM_dados_bancarios
        fields = '__all__'