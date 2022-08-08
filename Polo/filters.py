import django_filters

from django import forms

from Polo.models import CM_polo, SI_ies, SI_mantenedor

class CM_poloFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(
        lookup_expr='unaccent__icontains', 
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Insira o nome ou parte do nome do polo que procura...',
                'class': 'form-control',
                'id': 'search-focus',
                'type': 'search',
            })
    )
    
    class Meta:
        model = CM_polo
        fields = ['nome']
        
class SI_iesFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(
        lookup_expr='unaccent__icontains', 
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Insira o nome ou parte do nome da IES que procura...',
                'class': 'form-control',
                'id': 'search-focus',
                'type': 'search',
            })
    )
    
    class Meta:
        model = SI_ies
        fields = ['nome']

class SI_mantenedorFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(
        lookup_expr='unaccent__icontains', 
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Insira o nome ou parte do nome do mantenedor que procura...',
                'class': 'form-control',
                'id': 'search-focus',
                'type': 'search',
            })
    )
    
    class Meta:
        model = SI_mantenedor
        fields = ['nome']