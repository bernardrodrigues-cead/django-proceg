import datetime
from django import forms

from Curso.models import PR_associa_vaga_etapa, PR_edital, PR_etapa, PR_vagas, SI_associa_curso_oferta_polo, SI_curso_oferta

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

class PR_editalForm(forms.ModelForm):
    class Meta:
        model = PR_edital
        fields = [
            'num_edital',
            'ano_edital',
            'multiplas_inscricoes',
            'setor',
            'descricao',
            'data_inicio',
            'hora_inicio',
            'modalidade',
        ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['num_edital'].widget.attrs.update({'class': 'maskedEdital'})
        # Confere se existe algum edital lançado no ano corrente
        if PR_edital.objects.all() and PR_edital.objects.all().last().ano_edital == datetime.date.today().year:
            self.fields['num_edital'].initial = PR_edital.objects.last().num_edital + 1
        else:
            self.fields['num_edital'].initial = 1
        self.fields['ano_edital'].initial = datetime.date.today().year
        self.fields['ano_edital'].widget.attrs.update({'class': 'maskedAno'})
        self.fields['data_inicio'].widget.attrs.update({'class': 'maskedDate'})
        self.fields['hora_inicio'].widget.attrs.update({'class': 'maskedTime'})
        
class PR_vagasForm(forms.ModelForm):
    class Meta:
        model = PR_vagas
        fields = [
            'quantidade',
            'vaga_para_polo',
            'polo'
        ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quantidade'].widget.attrs['required'] = ''
        self.fields['quantidade'].widget.attrs.update({'class': 'count'})
        self.fields['polo'].widget.attrs.update({'class': 'hide'})
        self.fields['vaga_para_polo'].widget.attrs.update({'class': 'vaga_checkbox'})

# Criei um formulário extra devido ao campo polo, que estava, por padrão, hidden, durante a criação
class PR_vagasUpdateForm(forms.ModelForm):
    class Meta:
        model = PR_vagas
        fields = [
            'quantidade',
            'vaga_para_polo',
            'polo'
        ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quantidade'].widget.attrs['required'] = ''
        self.fields['quantidade'].widget.attrs.update({'class': 'count'})
        self.fields['vaga_para_polo'].widget.attrs.update({'class': 'vaga_checkbox'})

class PR_associa_usuario_editalForm(forms.Form):
    editais = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, 
        queryset=PR_edital.objects.all().order_by('-num_edital'), 
        help_text="* edital já vinculado a algum coordenador (responsável ao final da descrição)", 
        blank=True
    )

class vagasForm(forms.ModelForm):
    etapas = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=PR_etapa.objects.all().order_by('nome'))

    class Meta:
        model = PR_vagas
        fields = [
            'etapas',
        ]

class PR_associa_vaga_etapaForm(forms.ModelForm):
    class Meta:
        model = PR_associa_vaga_etapa
        fields = [
            'data_final',
            'hora_final'
        ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['data_final'].widget.attrs.update({'class': 'maskedDate hide'})
        self.fields['hora_final'].widget.attrs.update({'class': 'maskedTime hide'})