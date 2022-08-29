import django_filters

from django import forms
from django.contrib.auth.models import Group, Permission
from Acesso_Restrito.models import CM_pessoa

from Curso.models import FI_orgao_fomento, FI_programa, SI_curso_situacao, SI_tipo_curso
from Ticket.models import Funcionario, Setor
class CM_pessoaFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(
        lookup_expr='unaccent__icontains', 
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Insira o nome ou parte do nome da pessoa que procura...',
                'class': 'form-control',
                'id': 'search-focus',
                'type': 'search',
            })
    )
    
    class Meta:
        model = CM_pessoa
        fields = ['nome']

class GrupoFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr='unaccent__icontains', 
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Insira o nome ou parte do nome do grupo que procura...',
                'class': 'form-control',
                'id': 'search-focus',
                'type': 'search',
            })
    )
    
    class Meta:
        model = Group
        fields = ['name']
        
class PermissaoFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr='unaccent__icontains', 
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Insira o nome ou parte do nome da permissão que procura...',
                'class': 'form-control',
                'id': 'search-focus',
                'type': 'search',
            })
    )
    
    class Meta:
        model = Permission
        fields = ['name']

class UserFilter(django_filters.FilterSet):
    cpf = django_filters.CharFilter(
        lookup_expr='iexact', 
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Insira o CPF do usuário...',
                'class': 'form-control maskedCpf',
                'id': 'search-focus',
                'type': 'search',
            })
    )
    
    class Meta:
        model = CM_pessoa
        fields = ['cpf']

class SI_tipo_cursoFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(
        lookup_expr='unaccent__icontains', 
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Insira o nome ou parte do nome do tipo de curso que procura...',
                'id': 'search-focus',
                'type': 'search',
            })
    )
    
    class Meta:
        model = SI_tipo_curso
        fields = ['nome']
        
class SI_curso_situacaoFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(
        lookup_expr='unaccent__icontains', 
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Insira o nome ou parte do nome da situação que procura...',
                'id': 'search-focus',
                'type': 'search',
            })
    )
    
    class Meta:
        model = SI_curso_situacao
        fields = ['nome']
        
class FI_programaFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(
        lookup_expr='unaccent__icontains', 
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Insira o nome ou parte do nome do programa que procura...',
                'id': 'search-focus',
                'type': 'search',
            })
    )
    
    class Meta:
        model = FI_programa
        fields = ['nome']

class FuncionarioFilter(django_filters.FilterSet):
    pessoa = django_filters.CharFilter(
        lookup_expr='unaccent__icontains', 
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Insira o nome ou parte do nome do funcionario que procura...',
                'id': 'search-focus',
                'type': 'search',
            }
        )
    )
    
    class Meta:
        model = Funcionario
        fields = ['pessoa__nome']

class SetorFilter(django_filters.FilterSet):
    nome_setor = django_filters.CharFilter(
        lookup_expr='unaccent__icontains', 
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Insira o nome ou parte do nome do setor que procura...',
                'id': 'search-focus',
                'type': 'search',
            }
        )
    )
    
    class Meta:
        model = Setor
        fields = ['nome_setor']
class FI_orgao_fomentoFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(
        lookup_expr='unaccent__icontains', 
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Insira o nome ou parte do nome do órgão de fomento que procura...',
                'id': 'search-focus',
                'type': 'search',
            }
        )
    )
    
    class Meta:
        model = FI_orgao_fomento
        fields = ['nome']