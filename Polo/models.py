from tabnanny import verbose
from Acesso_Restrito.models import CM_cidade, CM_pais, CM_pessoa
from procead.imports import *

from django.db import models

from localflavor.br.models import BRPostalCodeField, BRCNPJField

from procead.validators import validate_is_zero_or_positive, validate_national_phone_number, validate_positive

# Create your models here.
class SI_mantenedor(models.Model):
    """Armazena mantenedores: provedores de recursos para manutenção dos polos
    """
    # Opções para tipos de instancia
    OPCOES_INSTANCIA = (
        ('E', 'Estadual'),
        ('F', 'Federal'),
        ('M', 'Municipal'),
    )
    
    nome = models.CharField(max_length=200)
    responsavel = models.CharField(max_length=200, verbose_name="Responsável")
    cnpj = BRCNPJField(verbose_name='CNPJ')
    cep = BRPostalCodeField(verbose_name='CEP')
    rua = models.CharField(max_length=200, verbose_name="Logradouro")
    numero = models.CharField(max_length=10, verbose_name="Número")
    complemento = models.CharField(max_length=100, blank=True, null=True)
    bairro = models.CharField(max_length=50)
    cidade = models.ForeignKey(CM_cidade, on_delete=models.RESTRICT)
    uf = models.CharField(max_length=2, choices=STATE_CHOICES, verbose_name='UF')
    pais = models.ForeignKey(CM_pais, on_delete=models.RESTRICT, verbose_name="País")
    telefone1 = models.CharField(max_length=20, verbose_name="Telefone", validators=[validate_national_phone_number])
    telefone2 = models.CharField(max_length=20, null=True, blank=True, verbose_name='Telefone secundário (opcional)', validators=[validate_national_phone_number])
    email = models.EmailField()
    instancia = models.CharField(max_length=10, choices=OPCOES_INSTANCIA, verbose_name="Tipo de instância")
    
    class Meta:
        verbose_name = 'SI - Mantenedor'
        verbose_name_plural = 'SI - Mantenedores'
        
    def __str__(self):
        return self.nome
    
    def get_absolute_url(self):
        """Retorna a url para acessar uma instância de cm_pessoa"""
        return reverse('si_mantenedor-list')

class SI_ies(models.Model):
    """Armazena as IES: Instituto de Ensino Superior
    """
    nome = models.CharField(max_length=200)
    sigla = models.CharField(max_length=45)
    telefone1 = models.CharField(max_length=20)
    telefone2 = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField()
    
    class Meta:
        verbose_name = 'SI - IES'
        verbose_name_plural = "SI - IES"
        
    def __str__(self):
        return self.nome
    
    def get_absolute_url(self):
        """Retorna a url para acessar uma instância de cm_polo"""
        return reverse('si_ies-list')

class CM_polo(models.Model):
    """Armazena os polos
    """
    OPCOES_STATUS = (
        ('A', 'Ativo'),
        ('C', 'Cancelado'),
        ('P', 'Publicado'),
        ('S', 'Suspenso'),
        ('E', 'Em análise'),
    )
    
    OPCOES_CLASSIFICACAO_SEED = (
        ('L', 'L - Polo com interrupção de entrada de estudantes nos cursos que necessitam de laboratório'),
        ('R', 'R - Polo com interrupção de entradas de estudantes'),
        ('S', 'S - Polo com infraestrutura suficiente'),
        ('T', 'T - Polo com recomendação de melhoria'),
    )
    
    DIAS_SEMANA = (
        ('dom', 'Domingo'),
        ('seg', 'Segunda'),
        ('ter', 'Terça'),
        ('qua', 'Quarta'),
        ('qui', 'Quinta'),
        ('sex', 'Sexta'),
        ('sab', 'Sábado'),
    )
    
    nome = models.CharField(max_length=45)
    mantenedor = models.ForeignKey(SI_mantenedor, on_delete=models.RESTRICT, null=True)
    status = models.CharField(max_length=1, choices=OPCOES_STATUS)
    coordenador = models.ForeignKey(CM_pessoa, null=True, on_delete=models.RESTRICT)
    telefone1 = models.CharField(max_length=20, verbose_name="Telefone")
    telefone2 = models.CharField(max_length=20, null=True, blank=True, verbose_name="Telefone opcional")
    email_institucional = models.EmailField()
    email_opcional = models.EmailField(null=True, blank=True)
    cep = BRPostalCodeField()
    rua = models.CharField(max_length=200, verbose_name="Logradouro")
    numero = models.CharField(max_length=10, verbose_name="Número")
    complemento = models.CharField(max_length=100, blank=True, null=True)
    bairro = models.CharField(max_length=50)
    cidade = models.ForeignKey(CM_cidade, on_delete=models.RESTRICT)
    uf = models.CharField(max_length=2, choices=STATE_CHOICES)
    pais = models.ForeignKey(CM_pais, on_delete=models.RESTRICT, verbose_name="País")
    latitude = models.CharField(max_length=11)
    longitude = models.CharField(max_length=11)
    classificacao_seed = models.CharField(max_length=500, null=True, blank=True, choices=OPCOES_CLASSIFICACAO_SEED, verbose_name="Classificação SEED")
    distancia_JF = models.PositiveIntegerField(null=True, blank=True, verbose_name="Distância do polo a Juiz de Fora", help_text="(Km)", validators=[validate_positive])
    tempo_viagem = models.CharField(max_length=45, null=True, blank=True, verbose_name="Tempo de viagem partindo de Juiz de Fora", help_text="hh:mm")
    dia_funcionamento_inicio = models.CharField(max_length=3, choices=DIAS_SEMANA, null=True, blank=True, verbose_name="Dia de funcionamento (início)")
    dia_funcionamento_fim = models.CharField(max_length=3, choices=DIAS_SEMANA, null=True, blank=True, verbose_name="Dia de funcionamento (fim)")
    horario_funcionamento_inicio = models.TimeField(null=True, blank=True, verbose_name="Horário de funcionamento (início)", help_text="hh:mm")
    horario_funcionamento_fim = models.TimeField(null=True, blank=True, verbose_name="Horário de funcionamento (fim)", help_text="hh:mm")
    apresentacao = models.TextField(null=True, blank=True, verbose_name="Apresentação")
    ies_vinculadas = models.ManyToManyField(SI_ies, verbose_name="IES vinculadas")
    
    class Meta:
        verbose_name = 'CM - Polo'
        
    def get_absolute_url(self):
        """Retorna a url para acessar uma instância de cm_polo"""
        return reverse('cm_polo-list')
    
    def __str__(self):
        return self.nome