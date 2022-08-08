from django import forms
from Curso.models import CM_pessoa

from Viagens.models import VI_endereco, VI_os

class VI_enderecoForm(forms.ModelForm):
    class Meta:
        model = VI_endereco
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cep'].widget.attrs.update({'class': 'maskedCep'})
 
class VI_osForm(forms.ModelForm):   
    class Meta:
        model = VI_os
        fields = [  
            'viajante', 
            'curso',
            'objetivo',
            'justificativa',
            'destino_ida',
            'data_ida',
            'horario_ida',
            'destino_volta',
            'data_volta',
            'horario_volta',
            'anexos'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['data_ida'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
        self.fields['data_volta'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
        self.fields['horario_ida'] = forms.TimeField(widget=forms.widgets.TimeInput(attrs={'type': 'time'}))
        self.fields['horario_volta'] = forms.TimeField(widget=forms.widgets.TimeInput(attrs={'type': 'time'}))
        self.fields['viajante'].queryset = CM_pessoa.objects.order_by('nome').exclude(cpf='000.000.000-00')
        self.fields['anexos'].widget.attrs.update({'multiple': True})