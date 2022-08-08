from django import forms

import django_filters

from Ticket.models import Solicitacao

class SolicitacaoFilter(django_filters.FilterSet):
    assunto = django_filters.CharFilter(
        lookup_expr='unaccent__icontains', 
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Insira o nome ou parte do nome do assunto que procura...',
                'class': 'form-control',
                'id': 'search-focus',
                'type': 'search',
            })
    )
    
    class Meta:
        model = Solicitacao
        fields = ['assunto']