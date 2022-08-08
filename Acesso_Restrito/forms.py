from django import forms
from django.contrib.auth.models import Group, Permission, User

from Acesso_Restrito.models import CM_pessoa

class CM_pessoaForm(forms.ModelForm):
    class Meta:
        model = CM_pessoa
        fields = [
            'cpf',
            'nome',
            'sexo',
            'data_nascimento',
            'cep',
            'rua',
            'numero',
            'bairro',
            'cidade',
            'uf',
            'pais',
            'ddd1',
            'telefone1',
            'ddd2',
            'telefone2',
            'email',
            'descricao_deficiencia',
        ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cpf'].widget.attrs.update({'class': 'maskedCpf'})
        self.fields['cep'].widget.attrs.update({'class': 'maskedCep'})
        self.fields['data_nascimento'].widget.attrs.update({'class': 'maskedDate'})


class GrupoForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Permission.objects.all())
    
    class Meta:
        model = Group
        fields = ['name', 'permissions']
        
class Usuario_grupoForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Group.objects.all())
    
    class Meta:
        model = User
        fields = ['groups']