import datetime
from Curso.models import CM_curso, SI_curso_oferta
from django.contrib.auth.models import User

import django_filters
from django import forms

class CM_cursoFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(
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
        model = CM_curso
        fields = ['nome']
        
class SI_curso_ofertaFilter(django_filters.FilterSet):
    curso__nome = django_filters.CharFilter(
        lookup_expr='unaccent__icontains', 
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Insira o nome ou parte do nome da oferta que procura...',
                'class': 'form-control',
                'id': 'search-focus',
                'type': 'search',
            })
    )
    
    class Meta:
        model = SI_curso_oferta
        fields = ['curso__nome']

class UserEditalFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(
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
        model = User
        fields = ['username']