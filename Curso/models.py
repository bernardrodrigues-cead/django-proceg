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
    oferta = models.PositiveIntegerField()
    data_inicio = models.DateField(verbose_name="Data de início", help_text="(Data do SISUAB que possibilita cálculo e geração da planilha)")
    data_fim = models.DateField(verbose_name="Data de término prevista")
    periodos = models.PositiveIntegerField(verbose_name="Quantidade de Períodos", validators=[validate_positive])
    num_vagas = models.PositiveIntegerField(verbose_name="Número de Vagas", validators=[validate_is_zero_or_positive], default=0, help_text="(Cadastrar através da aba Vincular Oferta/Polo)")
    polos_vinculados = models.ManyToManyField(CM_polo, through='SI_associa_curso_oferta_polo')
    
    class Meta:
        verbose_name = 'SI - Curso-Oferta'
        verbose_name_plural = 'SI - Cursos-Ofertas'
        
    def __str__(self):
        return str(self.oferta)[4:7] + '/' + str(self.oferta)[:4] + ": " + str(self.curso)
      
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

class PR_setor(models.Model):
    nome = models.CharField(max_length=50)
    sigla = models.CharField(max_length=15)
    
    def __str__(self):
        return self.sigla
    
    class Meta:
        verbose_name = 'PR - Setor'
        verbose_name_plural = 'PR - Setores'

class PR_modalidade(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'PR - Modalidade'
    
class PR_edital(models.Model):
    num_edital = models.PositiveIntegerField(verbose_name="Edital número")
    ano_edital = models.PositiveIntegerField(verbose_name="Ano", validators=[validate_edital_year])
    edital_string = models.CharField(max_length=8, unique=True)
    multiplas_inscricoes = models.BooleanField(verbose_name="Múltiplas Inscrições", help_text="Este edital permite a inscrição em mais de uma vaga")
    setor = models.ForeignKey(PR_setor, on_delete=models.RESTRICT)
    descricao = models.TextField(verbose_name="Descrição")
    curso = models.ManyToManyField(CM_curso)

    modalidade = models.ForeignKey(PR_modalidade, on_delete=models.RESTRICT)
    data_cadastro = models.DateTimeField(auto_now=True)
    usuario_vinculado = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True)
    
    def __str__(self):
        if(self.usuario_vinculado):
            return self.edital_string + '* -- ' + self.descricao + ' -- (responsável: ' + str(self.usuario_vinculado.first_name) + ')'
        else:
            return self.edital_string + ' -- ' + self.descricao
    
    class Meta:
        verbose_name = 'PR - Edital'
        verbose_name_plural = 'PR - Editais'

class PR_etapa(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.nome
    
    def get_absolute_url(self):
        return reverse('pr_etapa-list')
    
    class Meta:
        verbose_name = 'PR - Etapa'

class PR_vagas(models.Model):
    edital = models.ForeignKey(PR_edital, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    vaga_para_polo = models.BooleanField(verbose_name="Esta vaga é referente  um polo")
    polo = models.ForeignKey(CM_polo, on_delete=models.RESTRICT, null=True, blank=True)
    etapas = models.ManyToManyField(PR_etapa, through='PR_associa_vaga_etapa')
    
    class Meta:
        verbose_name = 'PR - Vagas'
        verbose_name_plural = 'PR - Vagas'
        
    def __str__(self):
        if(self.vaga_para_polo):
            return self.edital.edital_string + " - " + str(self.polo.nome)
        else:
            return self.edital.edital_string + " - " + str(self.edital.modalidade)
        
class PR_associa_vaga_etapa(models.Model):
    etapa = models.ForeignKey(PR_etapa, on_delete=models.RESTRICT)
    vaga = models.ForeignKey(PR_vagas, on_delete=models.RESTRICT)
    data_final = models.DateField()
    hora_final = models.TimeField(help_text="hh:mm")
    
    def __str__(self):
        return str(self.vaga) + ' - ' + str(self.etapa)
    
    class Meta:
        verbose_name = 'PR - Associa Vaga/Etapa'
        verbose_name_plural = 'PR - Associa Vaga/Etapa'