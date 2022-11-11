import datetime
from django import forms
from Acesso_Restrito.models import CM_cidade

from Curso.models import SI_associa_curso_oferta_polo, SI_curso_oferta

class CM_cidadeForm(forms.ModelForm):
    class Meta:
        model = CM_cidade
        fields = '__all__'

class SI_curso_ofertaForm(forms.ModelForm):
    class Meta:
        model = SI_curso_oferta
        fields = [
            'curso',
            'numero_oferta',
            'data_inicio',
            'data_fim',
            'periodos'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['data_inicio'].widget.attrs['class'] = 'maskedDate'
        self.fields['data_fim'].widget.attrs['class'] = 'maskedDate'
        
class SI_associa_curso_oferta_poloForm(forms.ModelForm):
    class Meta:
        model = SI_associa_curso_oferta_polo
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['polo'].widget.attrs['required'] = ''
        self.fields['num_vagas'].widget.attrs['required'] = ''