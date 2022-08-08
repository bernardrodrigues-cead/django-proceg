from django.db import models

from Acesso_Restrito.models import CM_pessoa
from Curso.models import CM_curso

# Create your models here
class FI_bolsa(models.Model):
    nome = models.CharField(max_length=200)
    valor = models.FloatField()
    
    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'CM - Pessoa/Bolsa'
        verbose_name_plural = 'CM - Pessoas/Bolsas'

class CM_pessoa_bolsa(models.Model):
    pessoa = models.ForeignKey(CM_pessoa, on_delete=models.RESTRICT)
    curso = models.ForeignKey(CM_curso, on_delete=models.RESTRICT)
    bolsa = models.ForeignKey(FI_bolsa, on_delete=models.RESTRICT)

    def __str__(self):
        return self.pessoa.nome + '/' + self.bolsa.nome

    class Meta:
        verbose_name = 'FI - Bolsa'