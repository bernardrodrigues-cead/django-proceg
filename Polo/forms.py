from django import forms
from Curso.models import CM_pessoa

from Polo.models import CM_polo, SI_ies

class CM_poloForm(forms.ModelForm):
    coordenador = forms.ModelChoiceField(queryset=CM_pessoa.objects.order_by('nome').exclude(cpf='000.000.000-00'))
    
    class Meta:
        model = CM_polo
        fields = [
            'nome',
            'mantenedor',
            'status',
            'coordenador',
            'telefone1',
            'telefone2',
            'email_institucional',
            'email_opcional',
            'cep',
            'rua',
            'numero',
            'complemento',
            'bairro',
            'cidade',
            'uf',
            'pais',
            'latitude',
            'longitude',
            'classificacao_seed',
            'distancia_JF',
            'tempo_viagem',
            'dia_funcionamento_inicio',
            'dia_funcionamento_fim',
            'horario_funcionamento_inicio',
            'horario_funcionamento_fim',
            'apresentacao',
        ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['horario_funcionamento_inicio'].widget.attrs['class'] = 'maskedTime'
        self.fields['horario_funcionamento_fim'].widget.attrs['class'] = 'maskedTime'           
        self.fields['cep'].widget.attrs.update({'class': 'maskedCep'})
        self.fields['telefone1'].widget.attrs.update({'class': 'maskedPhoneBR'})
        self.fields['telefone2'].widget.attrs.update({'class': 'maskedPhoneBR'})
            
class SI_associa_polo_iesForm(forms.ModelForm):
    ies_vinculadas = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=SI_ies.objects.all())
    
    class Meta:
        model = CM_polo
        fields = ['ies_vinculadas']