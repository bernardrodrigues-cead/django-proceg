from django.db import models
from Acesso_Restrito.models import CM_cidade, CM_pessoa

from procead.imports import *

from Curso.models import CM_curso

# Create your models here.
class VI_endereco(models.Model):
    nome = models.CharField(max_length=100)
    cep = models.CharField(max_length=10, verbose_name="CEP")
    rua = models.CharField(max_length=100, verbose_name="Logradouro")
    numero = models.PositiveIntegerField(verbose_name="Número")
    complemento = models.CharField(max_length=50, blank=True, null=True)
    bairro = models.CharField(max_length=50)
    cidade = models.ForeignKey(CM_cidade, on_delete=models.RESTRICT)
    uf = models.CharField(max_length=2, choices=STATE_CHOICES, verbose_name="Estado")
    
    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'VI - Endereço'


class VI_os(models.Model):
    VI_STATUS_CHOICES = (
        ('A', 'Aprovado'),
        ('R', 'Reprovado'),
        ('P', 'Pendente')
    )
    
    viajante = models.ManyToManyField(CM_pessoa, verbose_name="Viajante(s)", help_text="Selecione um ou mais")
    solicitante = models.ForeignKey(CM_pessoa, on_delete=models.RESTRICT, related_name="coordenador")
    curso = models.ForeignKey(CM_curso, on_delete=models.RESTRICT)
    objetivo = models.TextField()
    justificativa = models.TextField()
    destino_ida = models.ForeignKey(VI_endereco, on_delete=models.RESTRICT, related_name="local_ida", verbose_name="Destino (ida)")
    data_ida = models.DateField(verbose_name="Data (ida)")
    horario_ida = models.TimeField(verbose_name="Horário (ida)", help_text="hh:mm")
    destino_volta = models.ForeignKey(VI_endereco, on_delete=models.RESTRICT, related_name="local_volta", verbose_name="Destino (volta)")
    data_volta = models.DateField(verbose_name="Data (volta)")
    horario_volta = models.TimeField(verbose_name="Horário (volta)", help_text="hh:mm")
    anexos = models.FileField(upload_to='upload', max_length=255, help_text='Espaço destinado à apresentação de documentos obrigatórios e acessórios à realização das viagens (justificativa formal, cronograma, folders, declarações diversas, etc)')
    status = models.CharField(max_length=1, choices=VI_STATUS_CHOICES, default='P', verbose_name='Alterar Status')

    def __str__(self):
        return str(self.id) + ' - ' + str(self.destino_ida) + ' - ' + str(self.data_ida) + ' - ' + str(self.curso)
    
    class Meta:
        verbose_name = 'VI - OS'
        verbose_name_plural = 'VI - OS'