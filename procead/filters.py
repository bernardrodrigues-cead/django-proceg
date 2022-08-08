from django import forms


class Filter(forms.Form):
    consulta = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Insira o nome ou parte do nome do que procura...',
                'class': 'form-control',
                'id': 'search-focus',
                'type': 'search',
            })
        )