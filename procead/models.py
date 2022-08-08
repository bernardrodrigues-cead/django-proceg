import requests, json, uuid

from django.db import models
from django.db.models.functions import Lower
from django.urls import reverse
from django.contrib.auth.models import Permission, Group, User

from localflavor.br.models import BRPostalCodeField, BRCPFField, BRCNPJField
from localflavor.br.br_states import STATE_CHOICES
from procead.validators import *

# ENVIADO PARA PROCEAD.IMPORTS
#opcoes para campos sim e não
SN = (
    (1, 'Sim'),
    (0, 'Não'),
)

STATE_CHOICES = list(STATE_CHOICES) + [('00', 'Estrangeiro (Foreign)')]

# def opcoes_pais():
#     """Retorna uma lista de opções contendo todos os países do mundo

#     Returns:
#         _type_: list of tuples (str: nome, str: nome)
#     """
#     OPCOES_PAIS = []
#     api = requests.get('https://servicodados.ibge.gov.br/api/v1/localidades/paises').content
#     api_json = json.loads(api)
#     for pais in api_json:
#         OPCOES_PAIS.append((pais['nome'], pais['nome']))
#     return OPCOES_PAIS

# # ENVIADO PARA O APP CURSO
# class CM_banco(models.Model):
#     nome = models.CharField(max_length=200)
#     codigo = models.CharField(max_length=5)
    
#     def __str__(self):
#         return self.nome + ' - (cód. ' + self.codigo + ')'
    
#     class Meta:
#         verbose_name = 'CM - Banco'
#         ordering = [Lower('nome')]

# class CM_dados_bancarios(models.Model):
#     banco = models.ForeignKey(CM_banco, on_delete=models.RESTRICT)
#     agencia = models.CharField(max_length=15, verbose_name='Agência')
#     digito_verificador_agencia = models.CharField(max_length=1, null=True, blank=True, verbose_name="Dígito Verificador")
#     conta = models.CharField(max_length=15, verbose_name='Conta')
#     digito_verificador_conta = models.CharField(max_length=1, null=True, blank=True, verbose_name='Dígito Verificador')
#     operacao = models.CharField(max_length=5, null=True, blank=True, verbose_name='Operação')

#     def __str__(self):
#         return str(self.banco) + ' - Agência: ' + self.agencia

#     class Meta:
#         verbose_name = 'CM - Dados Bancários'
#         verbose_name_plural = 'CM - Dados Bancários'

# class CM_cidade(models.Model):
#     nome_cidade = models.CharField(max_length=100)
#     uf_cidade = models.CharField(max_length=2, choices=STATE_CHOICES)
    
#     class Meta:
#         verbose_name = "CM - Cidade"
        
#     def __str__(self):
#         return self.nome_cidade

# class CM_pessoa(models.Model):
#     """Opções para o campo sexo
#     """
#     OPCOES_SEXO = (
#         ('M', 'Masculino'),
#         ('F', 'Feminino'),
#         ('O', 'Outro'),
#     )
    
#     cpf = models.name = BRCPFField(verbose_name="CPF", unique=True)
#     nome = models.CharField('Nome/Nome Social', max_length=200)
#     sexo = models.CharField(max_length=1, choices=OPCOES_SEXO)
#     data_nascimento = models.DateField()
#     cep = BRPostalCodeField(verbose_name="CEP")
#     rua = models.CharField(max_length=200, verbose_name='Logradouro')
#     numero = models.CharField(max_length=10, verbose_name="Número")
#     complemento = models.CharField(max_length=100, blank=True, null=True)
#     bairro = models.CharField(max_length=50)
#     cidade = models.ForeignKey(CM_cidade, on_delete=models.RESTRICT)
#     uf = models.CharField(max_length=2, choices=STATE_CHOICES, verbose_name="UF")
#     pais = models.CharField(max_length=50, choices=opcoes_pais(), default=opcoes_pais()[20], verbose_name="País")
#     ddd1 = models.CharField(max_length=4, verbose_name="DDD")
#     telefone1 = models.CharField(max_length=20, verbose_name="Telefone")
#     ddd2 = models.CharField(max_length=4, verbose_name="DDD")
#     telefone2 = models.CharField(max_length=20, verbose_name='Telefone Celular')
#     email = models.EmailField()
#     descricao_deficiencia = models.TextField(blank=True, null=True, verbose_name="Descrição de Deficiência (opcional)")
    
#     unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
#     user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    
#     def get_absolute_url(self):
#         """Retorna a url para acessar uma instância de cm_pessoa"""
#         return reverse('cm_pessoa-list')
    
#     class Meta:
#         verbose_name = 'CM - Pessoa'
        
#     def __str__(self):
#         return self.nome

# class CM_pessoa_documentacao(models.Model):
#     AREA_SUPERIOR_CHOICES = (
#         ('B', 'Biológicas'),
#         ('E', 'Exatas'),
#         ('H', 'Humanas')
#     )
    
#     ESTADO_CIVIL_CHOICES = (
#         ('Solteiro(a)', 'Solteiro(a)'),
#         ('Casado(a)', 'Casado(a)'),
#         ('Separado(a)', 'Separado(a)'),
#         ('Divorciado(a)', 'Divorciado(a)'),
#         ('Viúvo(a)', 'Viúvo(a)'),
#         ('União Estável', 'União Estável'),
#     )
    
#     pessoa = models.OneToOneField(CM_pessoa, on_delete=models.RESTRICT)

#     banco = models.OneToOneField(CM_dados_bancarios, on_delete=models.RESTRICT)
#     # Caso seja servidor
#     siape = models.CharField(max_length=8, blank=True, null=True)
    
#     # Ainda a definir se vai permanecer
#     pispasep = models.CharField(max_length=12, blank=True, null=True)
#     data_pispasep = models.DateField(blank=True, null=True)
    
#     # Passo 4 - Ficha UAB
#     profissao = models.CharField(max_length=100, verbose_name='Profissão')
#     tipo_documento = models.CharField(max_length=50, verbose_name='Tipo de Documento')
#     documento = models.CharField(max_length=20, verbose_name='Número do Documento')
#     data_emissao_documento = models.DateField(verbose_name='Data de Emissão')
#     orgao_expeditor_documento = models.CharField(max_length=30, verbose_name='Órgão Expeditor')
#     uf_nascimento = models.CharField(max_length=2, verbose_name='UF de Nascimento')
#     cidade_nascimento = models.ForeignKey(CM_cidade, on_delete=models.RESTRICT, verbose_name='Cidade de Nascimento')
#     nacionalidade = models.CharField(max_length=30, default="Brasileiro(a)")
#     estado_civil = models.CharField(max_length=20, verbose_name='Estado Civil', choices=ESTADO_CIVIL_CHOICES)
#     nome_conjuge = models.CharField(max_length=200, blank=True, null=True, verbose_name='Nome do(a) cônjuge')
#     nome_pai = models.CharField(max_length=200, blank=True, null=True, verbose_name='Nome do Pai')
#     nome_mae = models.CharField(max_length=200, verbose_name='Nome da Mãe')
#     data_cadastramento = models.DateTimeField()
#     data_ultima_atualizacao = models.DateTimeField(blank=True, null=True)
    
#     area_ultimo_curso_superior = models.CharField(max_length=1, choices=AREA_SUPERIOR_CHOICES, verbose_name='Área do último curso superior')
#     ultimo_curso_titulacao = models.CharField(max_length=200, verbose_name='Último curso de titulação')
#     instituicao_titulacao = models.CharField(max_length=200, verbose_name="Nome da Instituição de Titulação")
    
#     def __str__(self):
#         return "Documentos de " + self.pessoa.nome
    
#     class Meta:
#         verbose_name = 'CM - Pessoa - Documentação'

# # ENVIADO PARA O APP POLO
# class SI_mantenedor(models.Model):
#     """Armazena mantenedores: provedores de recursos para manutenção dos polos
#     """
#     # Opções para tipos de instancia
#     OPCOES_INSTANCIA = (
#         ('E', 'Estadual'),
#         ('F', 'Federal'),
#         ('M', 'Municipal'),
#     )
    
#     nome = models.CharField(max_length=200)
#     responsavel = models.CharField(max_length=200, verbose_name="Responsável")
#     cnpj = BRCNPJField(verbose_name='CNPJ')
#     cep = BRPostalCodeField(verbose_name='CEP')
#     rua = models.CharField(max_length=200, verbose_name="Logradouro")
#     numero = models.CharField(max_length=10, verbose_name="Número")
#     complemento = models.CharField(max_length=100, blank=True, null=True)
#     bairro = models.CharField(max_length=50)
#     cidade = models.ForeignKey(CM_cidade, on_delete=models.RESTRICT)
#     uf = models.CharField(max_length=2, choices=STATE_CHOICES, verbose_name='UF')
#     pais = models.CharField(max_length=50, choices=opcoes_pais(), default=opcoes_pais()[20], verbose_name="País")
#     telefone1 = models.CharField(max_length=20, verbose_name="Telefone", validators=[validate_national_phone_number])
#     telefone2 = models.CharField(max_length=20, null=True, blank=True, verbose_name='Telefone secundário (opcional)', validators=[validate_national_phone_number])
#     email = models.EmailField()
#     instancia = models.CharField(max_length=10, choices=OPCOES_INSTANCIA, verbose_name="Tipo de instância")
    
#     class Meta:
#         verbose_name = 'SI - Mantenedor'
#         verbose_name_plural = 'SI - Mantenedores'
        
#     def __str__(self):
#         return self.nome
    
#     def get_absolute_url(self):
#         """Retorna a url para acessar uma instância de cm_pessoa"""
#         return reverse('si_mantenedor-list')

# class SI_ies(models.Model):
#     """Armazena as IES: Instituto de Ensino Superior
#     """
#     nome = models.CharField(max_length=200)
#     sigla = models.CharField(max_length=45)
#     telefone1 = models.CharField(max_length=20)
#     telefone2 = models.CharField(max_length=20, null=True, blank=True)
#     email = models.EmailField()
    
#     class Meta:
#         verbose_name = 'SI - IES'
#         verbose_name_plural = "SI - IES"
        
#     def __str__(self):
#         return self.nome
    
#     def get_absolute_url(self):
#         """Retorna a url para acessar uma instância de cm_polo"""
#         return reverse('si_ies-list')

# class CM_polo(models.Model):
#     """Armazena os polos
#     """
#     OPCOES_STATUS = (
#         ('A', 'Ativo'),
#         ('C', 'Cancelado'),
#         ('P', 'Publicado'),
#         ('S', 'Suspenso'),
#         ('E', 'Em análise'),
#     )
    
#     OPCOES_CLASSIFICACAO_SEED = (
#         ('L', 'L - Polo com interrupção de entrada de estudantes nos cursos que necessitam de laboratório'),
#         ('R', 'R - Polo com interrupção de entradas de estudantes'),
#         ('S', 'S - Polo com infraestrutura suficiente'),
#         ('T', 'T - Polo com recomendação de melhoria'),
#     )
    
#     DIAS_SEMANA = (
#         ('dom', 'Domingo'),
#         ('seg', 'Segunda'),
#         ('ter', 'Terça'),
#         ('qua', 'Quarta'),
#         ('qui', 'Quinta'),
#         ('sex', 'Sexta'),
#         ('sab', 'Sábado'),
#     )
    
#     nome = models.CharField(max_length=45)
#     mantenedor = models.ForeignKey(SI_mantenedor, on_delete=models.RESTRICT, null=True)
#     status = models.CharField(max_length=1, choices=OPCOES_STATUS)
#     coordenador = models.ForeignKey(CM_pessoa, null=True, on_delete=models.RESTRICT)
#     telefone1 = models.CharField(max_length=20, verbose_name="Telefone")
#     telefone2 = models.CharField(max_length=20, null=True, blank=True, verbose_name="Telefone opcional")
#     email_institucional = models.EmailField()
#     email_opcional = models.EmailField(null=True, blank=True)
#     cep = BRPostalCodeField()
#     rua = models.CharField(max_length=200, verbose_name="Logradouro")
#     numero = models.CharField(max_length=10, verbose_name="Número")
#     complemento = models.CharField(max_length=100, blank=True, null=True)
#     bairro = models.CharField(max_length=50)
#     cidade = models.ForeignKey(CM_cidade, on_delete=models.RESTRICT)
#     uf = models.CharField(max_length=2, choices=STATE_CHOICES)
#     pais = models.CharField(max_length=50, choices=opcoes_pais(), default=opcoes_pais()[20])
#     latitude = models.CharField(max_length=11)
#     longitude = models.CharField(max_length=11)
#     classificacao_seed = models.CharField(max_length=500, null=True, blank=True, choices=OPCOES_CLASSIFICACAO_SEED, verbose_name="Classificação SEED")
#     distancia_JF = models.PositiveIntegerField(null=True, blank=True, verbose_name="Distância do polo a Juiz de Fora", help_text="(Km)", validators=[validate_is_zero_or_positive])
#     tempo_viagem = models.CharField(max_length=45, null=True, blank=True, verbose_name="Tempo de viagem partindo de Juiz de Fora", help_text="hh:mm")
#     dia_funcionamento_inicio = models.CharField(max_length=3, choices=DIAS_SEMANA, null=True, blank=True, verbose_name="Dia de funcionamento (início)")
#     dia_funcionamento_fim = models.CharField(max_length=3, choices=DIAS_SEMANA, null=True, blank=True, verbose_name="Dia de funcionamento (fim)")
#     horario_funcionamento_inicio = models.TimeField(null=True, blank=True, verbose_name="Horário de funcionamento (início)", help_text="hh:mm")
#     horario_funcionamento_fim = models.TimeField(null=True, blank=True, verbose_name="Horário de funcionamento (fim)", help_text="hh:mm")
#     apresentacao = models.TextField(null=True, blank=True, verbose_name="Apresentação")
#     ies_vinculadas = models.ManyToManyField(SI_ies, verbose_name="IES vinculadas")
    
#     class Meta:
#         verbose_name = 'CM - Polo'
        
#     def get_absolute_url(self):
#         """Retorna a url para acessar uma instância de cm_polo"""
#         return reverse('cm_polo-list')
    
#     def __str__(self):
#         return self.nome


# # ENVIADO PARA FINANCEIRO
# class FI_orgao_fomento(models.Model):
#     nome = models.CharField(max_length=200)
    
#     class Meta:
#         verbose_name = 'FI - Orgão de Fomento'
#         verbose_name_plural = 'FI - Orgãos de Fomento'
        
#     def __str__(self):
#         return self.nome

# class FI_fonte_pagadora(models.Model):
#     nome = models.CharField(max_length=200)
#     sigla = models.CharField(max_length=50, null=True, blank=True)
#     orgao_fomento = models.ForeignKey(FI_orgao_fomento, on_delete=models.RESTRICT)
    
#     class Meta:
#         verbose_name = 'FI - Fonte Pagadora'
#         verbose_name_plural = 'FI - Fontes Pagadoras'
        
#     def __str__(self):
#         return self.nome
    
# class FI_programa(models.Model):
#     nome = models.CharField(max_length=200)
#     sigla = models.CharField(max_length=50, null=True, blank=True)
#     fonte_pagadora = models.ForeignKey(FI_fonte_pagadora, on_delete=models.RESTRICT)
    
#     class Meta:
#         verbose_name = 'FI - Programa'
        
#     def __str__(self):
#         return self.nome

# # ENVIADO PARA O APP CURSO
# class SI_tipo_curso(models.Model):
#     nome = models.CharField(max_length=45)
    
#     class Meta:
#         verbose_name = 'SI - Tipo de Curso'
#         verbose_name_plural = 'SI - Tipos de Curso'
        
#     def __str__(self):
#         return self.nome

# class SI_curso_projeto(models.Model):
#     nome = models.CharField(max_length=45)
#     denominacao_programa = models.CharField(max_length=500)
#     sigla_programa = models.CharField(max_length=20)
#     denominacao_secretaria = models.CharField(max_length=500)
#     sigla_secretaria = models.CharField(max_length=20)
    
#     class Meta:
#         verbose_name = 'SI - Curso-Projeto'
#         verbose_name_plural = 'SI - Cursos-Projetos'
        
#     def __str__(self):
#         return self.nome

# class SI_curso_situacao(models.Model):
#     nome = models.CharField(max_length=45)
    
#     class Meta:
#         verbose_name = 'SI - Curso Situação'
#         verbose_name_plural = 'SI - Cursos Situação'
        
#     def __str__(self):
#         return self.nome

# class CM_curso(models.Model):
#     OPCOES_STATUS = (
#         ('a', 'Ativo'),
#         ('i', 'Inativo'),
#     )
    
#     nome = models.CharField(max_length=200)
#     sigla = models.CharField(max_length=10, null=True, blank=True)
#     departamento = models.CharField(max_length=100, null=True, blank=True)
#     unidade = models.CharField(max_length=100, null=True, blank=True)
#     tipo_curso = models.ForeignKey(SI_tipo_curso, on_delete=models.RESTRICT, verbose_name="Tipo")
#     programa = models.ForeignKey(FI_programa, on_delete=models.RESTRICT)
#     curso_situacao = models.ForeignKey(SI_curso_situacao, on_delete=models.RESTRICT, verbose_name="Situação")
#     duracao_esperada = models.PositiveIntegerField(null=True, blank=True, verbose_name="Duração esperada", help_text="(meses)", validators=[validate_is_zero_or_positive])
#     email = models.EmailField(null=True, blank=True, verbose_name="E-mail")
#     telefone = models.CharField(max_length=20, null=True, blank=True, verbose_name="Telefone")
#     coordenador = models.ForeignKey(CM_pessoa, on_delete=models.RESTRICT)
#     status = models.CharField(max_length=1, choices=OPCOES_STATUS)
#     descricao = models.TextField(max_length=2000, verbose_name="Descrição/Apresentação")
#     perfil_egresso = models.TextField(max_length=2000, verbose_name="Perfil do Egresso")
    
#     ## Abaixo, campos que não estão no sistema atual
#     # curso_projeto = models.ForeignKey(SI_curso_projeto, on_delete=models.RESTRICT, null=True, blank=True)
#     # tipo_bolsa = models.CharField(max_length=4, null=True, blank=True)
#     # chamada_uab = models.CharField(max_length=45, null=True, blank=True)
#     # data_inicio = models.DateField(null=True, blank=True)
    
#     class Meta:
#         verbose_name = 'CM - Curso'
    
#     def __str__(self):
#         return self.nome
        
#     def get_absolute_url(self):
#         return reverse('cm_curso-list')
        
# class SI_curso_oferta(models.Model):
#     curso = models.ForeignKey(CM_curso, on_delete=models.RESTRICT)
#     numero_oferta = models.PositiveIntegerField(verbose_name="Número da Oferta", validators=[validate_is_zero_or_positive])
#     data_inicio = models.DateField(verbose_name="Data de início", help_text="(Data do SISUAB que possibilita cálculo e geração da planilha)")
#     data_fim = models.DateField(verbose_name="Data de término prevista")
#     periodos = models.PositiveIntegerField(verbose_name="Quantidade de Períodos", validators=[validate_is_zero_or_positive])
#     num_vagas = models.PositiveIntegerField(verbose_name="Número de Vagas", validators=[validate_is_zero_or_positive], default=0, help_text="(Cadastrar através da aba Vincular Oferta/Polo)")
#     polos_vinculados = models.ManyToManyField(CM_polo, through='SI_associa_curso_oferta_polo')
    
#     class Meta:
#         verbose_name = 'SI - Curso-Oferta'
#         verbose_name_plural = 'SI - Cursos-Ofertas'
        
#     def __str__(self):
#         return str(self.numero_oferta) + 'ª/' + str(self.data_inicio.year) + ": " + str(self.curso)
      
# class SI_associa_curso_oferta_polo(models.Model):
#     oferta = models.ForeignKey(SI_curso_oferta, on_delete=models.CASCADE)
#     polo = models.ForeignKey(CM_polo, on_delete=models.RESTRICT)
#     num_vagas = models.PositiveIntegerField(verbose_name="Número de vagas", validators=[validate_is_zero_or_positive])
    
#     class Meta:
#         verbose_name = 'SI - Curso-Oferta-Polo'
#         verbose_name_plural = 'SI - Cursos-Ofertas-Polos'
        
#     def get_absolute_url(self):
#         return reverse('si_curso_oferta-list')
    
#     def __str__(self):
#         return self.oferta.curso.nome + " - Polo: " + self.polo.nome + " - Vagas: " + str(self.num_vagas)

# # ENVIADO PARA O APP ACESSO_RESTRITO
# class CM_associa_grupo_permissao(models.Model):
#     grupo = models.ForeignKey(Group, on_delete=models.RESTRICT)
#     permissao = models.ForeignKey(Permission, on_delete=models.RESTRICT)
    
#     class Meta:
#         verbose_name = 'CM_associa_grupo_permissao'
#         verbose_name_plural = 'CM_associa_grupo_permissoes'
        
#     def __str__(self):
#         return str(self.grupo) + " -- " + str(self.permissao)

# # ENVIADO PARA O APP CURSO

# class PR_setor(models.Model):
#     nome = models.CharField(max_length=50)
#     sigla = models.CharField(max_length=15)
    
#     def __str__(self):
#         return self.sigla
    
#     class Meta:
#         verbose_name = 'PR - Setor'
#         verbose_name_plural = 'PR - Setores'

# class PR_modalidade(models.Model):
#     nome = models.CharField(max_length=100)
#     descricao = models.TextField()
    
#     def __str__(self):
#         return self.nome
    
#     class Meta:
#         verbose_name = 'PR - Modalidade'
    
# class PR_edital(models.Model):
#     num_edital = models.PositiveIntegerField(verbose_name="Edital número", unique=True)
#     ano_edital = models.PositiveIntegerField(verbose_name="Ano", validators=[validate_edital_year])
#     edital_string = models.CharField(max_length=8)
#     multiplas_inscricoes = models.BooleanField(verbose_name="Múltiplas Inscrições", help_text="Este edital permite a inscrição em mais de uma vaga")
#     setor = models.ForeignKey(PR_setor, on_delete=models.RESTRICT)
#     descricao = models.TextField(verbose_name="Descrição")
#     data_inicio = models.DateField(verbose_name="Data de início")
#     hora_inicio = models.TimeField(verbose_name="Hora de início", help_text="hh:mm")
#     modalidade = models.ForeignKey(PR_modalidade, on_delete=models.RESTRICT)
#     data_cadastro = models.DateTimeField()
#     usuario_vinculado = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True)
    
#     def __str__(self):
#         if(self.usuario_vinculado):
#             return self.edital_string + '* -- ' + self.descricao + ' -- (responsável: ' + str(self.usuario_vinculado.first_name) + ')'
#         else:
#             return self.edital_string + ' -- ' + self.descricao
    
#     class Meta:
#         verbose_name = 'PR - Edital'
#         verbose_name_plural = 'PR - Editais'

# class PR_etapa(models.Model):
#     nome = models.CharField(max_length=100, unique=True)
    
#     def __str__(self):
#         return self.nome
    
#     def get_absolute_url(self):
#         return reverse('pr_etapa-list')
    
#     class Meta:
#         verbose_name = 'PR - Etapa'

# class PR_vagas(models.Model):
#     edital = models.ForeignKey(PR_edital, on_delete=models.CASCADE)
#     quantidade = models.PositiveIntegerField()
#     vaga_para_polo = models.BooleanField(verbose_name="Esta vaga é referente  um polo")
#     polo = models.ForeignKey(CM_polo, on_delete=models.RESTRICT, null=True, blank=True)
#     etapas = models.ManyToManyField(PR_etapa, through='PR_associa_vaga_etapa')
    
#     class Meta:
#         verbose_name = 'PR - Vagas'
#         verbose_name_plural = 'PR - Vagas'
        
#     def __str__(self):
#         if(self.vaga_para_polo):
#             return self.edital.edital_string + " - " + str(self.polo.nome)
#         else:
#             return self.edital.edital_string + " - " + str(self.edital.modalidade)
        
# class PR_associa_vaga_etapa(models.Model):
#     etapa = models.ForeignKey(PR_etapa, on_delete=models.RESTRICT)
#     vaga = models.ForeignKey(PR_vagas, on_delete=models.RESTRICT)
#     data_final = models.DateField()
#     hora_final = models.TimeField(help_text="hh:mm")
    
#     def __str__(self):
#         return str(self.vaga) + ' - ' + str(self.etapa)
    
#     class Meta:
#         verbose_name = 'PR - Associa Vaga/Etapa'
#         verbose_name_plural = 'PR - Associa Vaga/Etapa'

# # ENVIADO PARA O APP VIAGENS
# class VI_endereco(models.Model):
#     nome = models.CharField(max_length=100)
#     cep = models.CharField(max_length=10, verbose_name="CEP")
#     rua = models.CharField(max_length=100, verbose_name="Logradouro")
#     numero = models.PositiveIntegerField(verbose_name="Número")
#     complemento = models.CharField(max_length=50, blank=True, null=True)
#     bairro = models.CharField(max_length=50)
#     cidade = models.ForeignKey(CM_cidade, on_delete=models.RESTRICT)
#     uf = models.CharField(max_length=2, choices=STATE_CHOICES, verbose_name="Estado")
    
#     def __str__(self):
#         return self.nome

# VI_STATUS_CHOICES = (
#     ('A', 'Aprovado'),
#     ('R', 'Reprovado'),
#     ('P', 'Pendente')
# )

# class VI_os(models.Model):
#     viajante = models.ManyToManyField(CM_pessoa, verbose_name="Viajante(s)", help_text="Selecione um ou mais")
#     solicitante = models.ForeignKey(CM_pessoa, on_delete=models.RESTRICT, related_name="coordenador")
#     curso = models.ForeignKey(CM_curso, on_delete=models.RESTRICT)
#     objetivo = models.TextField()
#     justificativa = models.TextField()
#     destino_ida = models.ForeignKey(VI_endereco, on_delete=models.RESTRICT, related_name="local_ida", verbose_name="Destino (ida)")
#     data_ida = models.DateField(verbose_name="Data (ida)")
#     horario_ida = models.TimeField(verbose_name="Horário (ida)", help_text="hh:mm")
#     destino_volta = models.ForeignKey(VI_endereco, on_delete=models.RESTRICT, related_name="local_volta", verbose_name="Destino (volta)")
#     data_volta = models.DateField(verbose_name="Data (volta)")
#     horario_volta = models.TimeField(verbose_name="Horário (volta)", help_text="hh:mm")
#     anexos = models.FileField(upload_to='upload', max_length=255, help_text='Espaço destinado à apresentação de documentos obrigatórios e acessórios à realização das viagens (justificativa formal, cronograma, folders, declarações diversas, etc)')
#     status = models.CharField(max_length=1, choices=VI_STATUS_CHOICES, default='P', verbose_name='Alterar Status')

#     def __str__(self):
#         return str(self.id) + ' - ' + str(self.destino_ida) + ' - ' + str(self.data_ida) + ' - ' + str(self.curso)
    
#     class Meta:
#         verbose_name = 'VI - OS'
#         verbose_name_plural = 'VI - OS'

# # ENVIADO PARA O APP FINANCEIRO
# class FI_bolsa(models.Model):
#     nome = models.CharField(max_length=200)
#     valor = models.FloatField()
    
#     def __str__(self):
#         return self.nome

# # ENVIADO PARA O APP FINANCEIRO  
# class CM_pessoa_bolsa(models.Model):
#     pessoa = models.ForeignKey(CM_pessoa, on_delete=models.RESTRICT)
#     curso = models.ForeignKey(CM_curso, on_delete=models.RESTRICT)
#     bolsa = models.ForeignKey(FI_bolsa, on_delete=models.RESTRICT)

#     def __str__(self):
#         return self.pessoa.nome + '/' + self.bolsa.nome

# Classe responsavel por permitir buscas independentes de acentuação
class Unaccent(models.Transform):
    bilateral = True
    lookup_name = 'unaccent'

    def as_postgresql(self, compiler, connection):
        lhs, params = compiler.compile(self.lhs)
        return "UNACCENT(%s)" % lhs, params

models.CharField.register_lookup(Unaccent)
models.TextField.register_lookup(Unaccent)