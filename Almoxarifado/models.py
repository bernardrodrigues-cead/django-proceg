from distutils.text_file import TextFile
from tabnanny import verbose
from wsgiref.validate import validator
from django.db import models
from Acesso_Restrito.models import CM_pessoa
from procead.validators import validate_positive

# Create your models here.


class Categoria(models.Model):
    descricao = models.CharField(verbose_name = "Descrição", max_length=30, unique=True)   
    def __str__(self):
        return self.descricao
    

class Produto(models.Model):
    
    TIPOS_PRODUTO = (
        ("C" , "Consumível"),
        ("P" , "Permanente"),
    )
    codigo_siga = models.IntegerField(verbose_name = "Codigo", primary_key=True)
    descricao = models.CharField(max_length=30)
    unidade = models.CharField(max_length=15)
    categoria = models.ForeignKey(Categoria, on_delete=models.RESTRICT , verbose_name="Categoria")
    tipo_produto = models.CharField(max_length=1,choices=TIPOS_PRODUTO, verbose_name = "Tipo de Produto")
    quantidade_minima = models.PositiveIntegerField(validators = [validate_positive], verbose_name="Quantidade Mínima")

    def __str__(self):
        return self.descricao       

class Estoque(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.RESTRICT)
    quantidade_estoque = models.PositiveIntegerField(verbose_name="Quantidade em Estoque")
 
    def __str__(self):
        return self.produto.descricao + " - Quantidade: " + str(self.quantidade_estoque)

class Entrada_Produto(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.RESTRICT)
    quantidade_entrada = models.PositiveIntegerField(validators = [validate_positive]) 
    origem = models.CharField(max_length=25 )
    data_entrada = models.DateTimeField(verbose_name="Data de Entrada", blank=True, null=True)
    responsavel = models.ForeignKey(CM_pessoa, on_delete=models.RESTRICT,verbose_name="Responsável")

    def __str__(self):
        return str(self.quantidade_entrada) + " " + self.produto.descricao + " " + " " + str(self.data_entrada)
       
class Saida_Produto(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.RESTRICT)
    quantidade_saida = models.PositiveIntegerField(validators = [validate_positive], verbose_name="Quantidade Saída") 
    destino = models.TextField(max_length=25)
    data_saida = models.DateTimeField(verbose_name="Data de Saída", blank=True, null=True)
    responsavel = models.ForeignKey(CM_pessoa, on_delete=models.RESTRICT,verbose_name="Responsável") 
        
    def __str__(self):
       return str(self.quantidade_saida) + " " + self.produto.descricao + " " + " " + str(self.data_saida)