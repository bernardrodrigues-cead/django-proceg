import django_filters

from django import forms

from Viagens.models import VI_endereco

class VI_enderecoFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(
        lookup_expr='unaccent__icontains', 
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Insira o nome ou parte do nome do endereço que procura...',
                'id': 'search-focus',
                'type': 'search',
                'class': 'h-100 rounded-0 rounded-start',
            })
    )
    
    class Meta:
        model = VI_endereco
        fields = ['nome']