from Acesso_Restrito.models import CM_pessoa
from Polo.models import CM_polo

from procead.imports import *

from django.contrib.auth.models import User

from procead.validators import validate_edital_year, validate_is_zero_or_positive, validate_positive

# Create your models here.
class SI_tipo_curso(models.Model):
    nome = models.CharField(max_length=45)
    
    class Meta:
        verbose_name = 'SI - Tipo de Curso'
        verbose_name_plural = 'SI - Tipos de Curso'
        
    def __str__(self):
        return self.nome

class SI_curso_projeto(models.Model):
    nome = models.CharField(max_length=45)
    denominacao_programa = models.CharField(max_length=500)
    sigla_programa = models.CharField(max_length=20)
    denominacao_secretaria = models.CharField(max_length=500)
    sigla_secretaria = models.CharField(max_length=20)
    
    class Meta:
        verbose_name = 'SI - Curso-Projeto'
        verbose_name_plural = 'SI - Cursos-Projetos'
        
    def __str__(self):
        return self.nome

class SI_curso_situacao(models.Model):
    nome = models.CharField(max_length=45)
    
    class Meta:
        verbose_name = 'SI - Curso Situação'
        verbose_name_plural = 'SI - Cursos Situação'
        
    def __str__(self):
        return self.nome

class FI_orgao_fomento(models.Model):
    nome = models.CharField(max_length=200)
    
    class Meta:
        verbose_name = 'FI - Orgão de Fomento'
        verbose_name_plural = 'FI - Orgãos de Fomento'
        
    def __str__(self):
        return self.nome

class FI_fonte_pagadora(models.Model):
    nome = models.CharField(max_length=200)
    sigla = models.CharField(max_length=50, null=True, blank=True)
    orgao_fomento = models.ForeignKey(FI_orgao_fomento, on_delete=models.RESTRICT)
    
    class Meta:
        verbose_name = 'FI - Fonte Pagadora'
        verbose_name_plural = 'FI - Fontes Pagadoras'
        
    def __str__(self):
        return self.nome

class FI_programa(models.Model):
    nome = models.CharField(max_length=200)
    sigla = models.CharField(max_length=50, null=True, blank=True)
    fonte_pagadora = models.ForeignKey(FI_fonte_pagadora, on_delete=models.RESTRICT)
    
    class Meta:
        verbose_name = 'FI - Programa'
        
    def __str__(self):
        return self.nome

class CM_curso(models.Model):
    OPCOES_STATUS = (
        ('a', 'Ativo'),
        ('i', 'Inativo'),
    )
    
    nome = models.CharField(max_length=200)
    sigla = models.CharField(max_length=10, null=True, blank=True)
    departamento = models.CharField(max_length=100, null=True, blank=True)
    unidade = models.CharField(max_length=100, null=True, blank=True)
    tipo_curso = models.ForeignKey(SI_tipo_curso, on_delete=models.RESTRICT, verbose_name="Tipo")
    programa = models.ForeignKey(FI_programa, on_delete=models.RESTRICT)
    curso_situacao = models.ForeignKey(SI_curso_situacao, on_delete=models.RESTRICT, verbose_name="Situação")
    duracao_esperada = models.PositiveIntegerField(null=True, blank=True, verbose_name="Duração esperada", help_text="(meses)", validators=[validate_positive])
    email = models.EmailField(verbose_name="E-mail")
    telefone = models.CharField(max_length=20, null=True, blank=True, verbose_name="Telefone")
    coordenador = models.ForeignKey(CM_pessoa, on_delete=models.RESTRICT)
    status = models.CharField(max_length=1, choices=OPCOES_STATUS)
    descricao = models.TextField(max_length=2000, verbose_name="Descrição/Apresentação")
    perfil_egresso = models.TextField(max_length=2000, verbose_name="Perfil do Egresso")
    
    ## Abaixo, campos que não estão no sistema atual
    # curso_projeto = models.ForeignKey(SI_curso_projeto, on_delete=models.RESTRICT, null=True, blank=True)
    # tipo_bolsa = models.CharField(max_length=4, null=True, blank=True)
    # chamada_uab = models.CharField(max_length=45, null=True, blank=True)
    # data_inicio = models.DateField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'CM - Curso'
    
    def __str__(self):
        return self.nome
        
    def get_absolute_url(self):
        return reverse('cm_curso-list')
        
class SI_curso_oferta(models.Model):
    curso = models.ForeignKey(CM_curso, on_delete=models.RESTRICT)
    numero_oferta = models.PositiveIntegerField(verbose_name="Número da Oferta", validators=[validate_is_zero_or_positive])
    data_inicio = models.DateField(verbose_name="Data de início", help_text="(Data do SISUAB que possibilita cálculo e geração da planilha)")
    data_fim = models.DateField(verbose_name="Data de término prevista")
    periodos = models.PositiveIntegerField(verbose_name="Quantidade de Períodos", validators=[validate_positive])
    num_vagas = models.PositiveIntegerField(verbose_name="Número de Vagas", validators=[validate_is_zero_or_positive], default=0, help_text="(Cadastrar através da aba Vincular Oferta/Polo)")
    polos_vinculados = models.ManyToManyField(CM_polo, through='SI_associa_curso_oferta_polo')
    
    class Meta:
        verbose_name = 'SI - Curso-Oferta'
        verbose_name_plural = 'SI - Cursos-Ofertas'
        
    def __str__(self):
        return str(self.numero_oferta) + 'ª/' + str(self.data_inicio.year) + ": " + str(self.curso)
      
class SI_associa_curso_oferta_polo(models.Model):
    oferta = models.ForeignKey(SI_curso_oferta, on_delete=models.CASCADE)
    polo = models.ForeignKey(CM_polo, on_delete=models.RESTRICT)
    num_vagas = models.PositiveIntegerField(verbose_name="Número de vagas", validators=[validate_positive])
    
    class Meta:
        verbose_name = 'SI - Curso-Oferta-Polo'
        verbose_name_plural = 'SI - Cursos-Ofertas-Polos'
        
    def get_absolute_url(self):
        return reverse('si_curso_oferta-list')
    
    def __str__(self):
        return self.oferta.curso.nome + " - Polo: " + self.polo.nome + " - Vagas: " + str(self.num_vagas)


## Edital
class Edital(models.Model):
    numero = models.PositiveIntegerField(primary_key=True)
    curso = models.ForeignKey(CM_curso, on_delete=models.RESTRICT)
    descricao = models.TextField()
    data_cadastro = models.DateTimeField(auto_now_add=True)

class Vaga(models.Model):
    edital = models.ForeignKey(Edital, on_delete=models.RESTRICT)
    descricao = models.TextField()
    quantidade = models.PositiveIntegerField()
    data_inicio_inscricao = models.DateTimeField()
    data_fim_inscricao = models.DateTimeField()
    data_inicio_validacao = models.DateTimeField()
    data_fim_validacao = models.DateTimeField()
    polo = models.ForeignKey(CM_polo, on_delete=models.RESTRICT)

class InscricaoVaga(models.Model):
    vaga = models.ForeignKey(Vaga, on_delete=models.RESTRICT)
    pessoa = models.ForeignKey(CM_pessoa, on_delete=models.RESTRICT)

class ValidacaoVaga(models.Model):
    vaga = models.ForeignKey(Vaga, on_delete=models.RESTRICT)
    pessoa = models.ForeignKey(CM_pessoa, on_delete=models.RESTRICT)

class ConfirmacaoVaga(models.Model):
    vaga = models.ForeignKey(Vaga, on_delete=models.RESTRICT)
    pessoa = models.ForeignKey(CM_pessoa, on_delete=models.RESTRICT)
    confirmado = models.BooleanField()

class JustificativaVaga(models.Model):
    vaga = models.ForeignKey(Vaga, on_delete=models.RESTRICT)
    pessoa = models.ForeignKey(CM_pessoa, on_delete=models.RESTRICT)
    descricao = models.CharField(max_length=255)

class AprovacaoVaga(models.Model):
    vaga = models.ForeignKey(Vaga, on_delete=models.RESTRICT)
    pessoa = models.ForeignKey(CM_pessoa, on_delete=models.RESTRICT)
    aprovado = models.BooleanField()

class DescricaoCampo(models.Model):
    descricao = models.CharField(max_length=127)

class Campo(models.Model):
    descricao_campo = models.ForeignKey(DescricaoCampo, on_delete=models.RESTRICT)
    vaga = models.ForeignKey(Vaga, on_delete=models.RESTRICT)
    peso = models.FloatField()
    pontuacao_maxima = models.FloatField()
    data_inicio = models.DateField()
    data_fim = models.DateField()
    obrigatorio = models.BooleanField()
    upload = models.BooleanField()

class InscricaoVagaCampo(models.Model):
    inscricao_vaga = models.ForeignKey(InscricaoVaga, on_delete=models.RESTRICT)
    campo = models.ForeignKey(Campo, on_delete=models.RESTRICT)
    pontuacao = models.FloatField()

class DocumentacaoInscricaoVagaCampo(models.Model):
    inscricao_vaga = models.ForeignKey(InscricaoVaga, on_delete=models.RESTRICT)
    campo = models.ForeignKey(Campo, on_delete=models.RESTRICT)
    documentacao = models.FileField()