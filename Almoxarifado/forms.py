from django import forms

from Almoxarifado.models import Categoria, Entrada_Produto, Saida_Produto
from Almoxarifado.models import Produto

class CategoriaForm(forms.ModelForm):
    class Meta: 
        model  = Categoria
        fields = ['descricao']

class ProdutoForm(forms.ModelForm):
    class Meta: 
        model  = Produto
        fields = ['codigo_siga','descricao', 'unidade', 'categoria' , 'tipo_produto', 'quantidade_minima']
                
class EntradaForm(forms.ModelForm):
    class Meta: 
        model  = Entrada_Produto
        fields = ['produto', 'quantidade_entrada', 'origem', 'responsavel']

class SaidaForm(forms.ModelForm):
    
    class Meta: 
        model  = Saida_Produto
        fields = ['produto', 'quantidade_saida', 'destino', 'responsavel']        
                                
class TesteForm(forms.Form):
    nome  = forms.CharField()
    idade = forms.IntegerField() 
    sexo  = forms.CharField()

class DataIntervalo(forms.Form):
    data_inicio = forms.DateField(label="Data Início", widget=forms.widgets.DateInput(attrs={'type': 'date'}), required=False)
    data_fim    = forms.DateField(label="Data Fim",    widget=forms.widgets.DateInput(attrs={'type': 'date'}), required=False)
