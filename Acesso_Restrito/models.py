from django.db import models

from django.contrib.auth.models import Group, Permission

from procead.models import *

# Create your models here.
class CM_associa_grupo_permissao(models.Model):
    grupo = models.ForeignKey(Group, on_delete=models.RESTRICT)
    permissao = models.ForeignKey(Permission, on_delete=models.RESTRICT)
    
    class Meta:
        verbose_name = 'CM - Associa Grupo/Permissao'
        verbose_name_plural = 'CM - Associa Grupo/Permissoes'
        
    def __str__(self):
        return str(self.grupo) + " -- " + str(self.permissao)

class CM_banco(models.Model):
    nome = models.CharField(max_length=200)
    codigo = models.CharField(max_length=5)
    
    def __str__(self):
        return self.nome + ' - (cód. ' + self.codigo + ')'
    
    class Meta:
        verbose_name = 'CM - Banco'
        ordering = [Lower('nome')]

class CM_dados_bancarios(models.Model):
    banco = models.ForeignKey(CM_banco, on_delete=models.RESTRICT)
    agencia = models.CharField(max_length=15, verbose_name='Agência')
    digito_verificador_agencia = models.CharField(max_length=1, null=True, blank=True, verbose_name="Dígito Verificador")
    conta = models.CharField(max_length=15, verbose_name='Conta')
    digito_verificador_conta = models.CharField(max_length=1, null=True, blank=True, verbose_name='Dígito Verificador')
    operacao = models.CharField(max_length=5, null=True, blank=True, verbose_name='Operação')

    def __str__(self):
        return str(self.banco) + ' - Agência: ' + self.agencia

    class Meta:
        verbose_name = 'CM - Dados Bancários'
        verbose_name_plural = 'CM - Dados Bancários'

class CM_cidade(models.Model):
    nome_cidade = models.CharField(max_length=100)
    uf_cidade = models.CharField(max_length=2, choices=STATE_CHOICES)
    
    class Meta:
        verbose_name = "CM - Cidade"
        
    def __str__(self):
        return self.nome_cidade

class CM_pais(models.Model):
    nome_pais = models.CharField(max_length=100)

    def __str__(self):
        return self.nome_pais
    class Meta:
        verbose_name = "CM - País"
        verbose_name_plural = "CM - Países"

class CM_pessoa(models.Model):
    """Opções para o campo sexo
    """
    OPCOES_SEXO = (
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    )
    
    cpf = models.name = BRCPFField(verbose_name="CPF", unique=True)
    nome = models.CharField('Nome/Nome Social', max_length=200)
    sexo = models.CharField(max_length=1, choices=OPCOES_SEXO)
    data_nascimento = models.DateField()
    cep = BRPostalCodeField(verbose_name="CEP")
    rua = models.CharField(max_length=200, verbose_name='Logradouro')
    numero = models.CharField(max_length=10, verbose_name="Número")
    complemento = models.CharField(max_length=100, blank=True, null=True)
    bairro = models.CharField(max_length=50)
    cidade = models.ForeignKey(CM_cidade, on_delete=models.RESTRICT)
    uf = models.CharField(max_length=2, choices=STATE_CHOICES, verbose_name="UF")
    pais = models.ForeignKey(CM_pais, on_delete=models.RESTRICT, verbose_name="País", default=CM_pais.objects.get(nome_pais="Brasil").pk)
    ddd1 = models.CharField(max_length=4, verbose_name="DDD")
    telefone1 = models.CharField(max_length=20, verbose_name="Telefone")
    ddd2 = models.CharField(max_length=4, verbose_name="DDD")
    telefone2 = models.CharField(max_length=20, verbose_name='Telefone Celular')
    email = models.EmailField()
    descricao_deficiencia = models.TextField(blank=True, null=True, verbose_name="Descrição de Deficiência (opcional)")
    
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    def get_absolute_url(self):
        """Retorna a url para acessar uma instância de cm_pessoa"""
        return reverse('cm_pessoa-list')
    
    class Meta:
        verbose_name = 'CM - Pessoa'
        
    def __str__(self):
        return self.nome

class CM_pessoa_documentacao(models.Model):
    AREA_SUPERIOR_CHOICES = (
        ('B', 'Biológicas'),
        ('E', 'Exatas'),
        ('H', 'Humanas')
    )
    
    ESTADO_CIVIL_CHOICES = (
        ('Solteiro(a)', 'Solteiro(a)'),
        ('Casado(a)', 'Casado(a)'),
        ('Separado(a)', 'Separado(a)'),
        ('Divorciado(a)', 'Divorciado(a)'),
        ('Viúvo(a)', 'Viúvo(a)'),
        ('União Estável', 'União Estável'),
    )
    
    pessoa = models.OneToOneField(CM_pessoa, on_delete=models.RESTRICT)

    banco = models.OneToOneField(CM_dados_bancarios, on_delete=models.RESTRICT)
    # Caso seja servidor
    siape = models.CharField(max_length=8, blank=True, null=True)
    
    # Ainda a definir se vai permanecer
    pispasep = models.CharField(max_length=12, blank=True, null=True)
    data_pispasep = models.DateField(blank=True, null=True)
    
    # Passo 4 - Ficha UAB
    profissao = models.CharField(max_length=100, verbose_name='Profissão')
    tipo_documento = models.CharField(max_length=50, verbose_name='Tipo de Documento')
    documento = models.CharField(max_length=20, verbose_name='Número do Documento')
    data_emissao_documento = models.DateField(verbose_name='Data de Emissão')
    orgao_expeditor_documento = models.CharField(max_length=30, verbose_name='Órgão Expeditor')
    uf_nascimento = models.CharField(max_length=2, verbose_name='UF de Nascimento')
    cidade_nascimento = models.ForeignKey(CM_cidade, on_delete=models.RESTRICT, verbose_name='Cidade de Nascimento')
    nacionalidade = models.CharField(max_length=30, default="Brasileiro(a)")
    estado_civil = models.CharField(max_length=20, verbose_name='Estado Civil', choices=ESTADO_CIVIL_CHOICES)
    nome_conjuge = models.CharField(max_length=200, blank=True, null=True, verbose_name='Nome do(a) cônjuge')
    nome_pai = models.CharField(max_length=200, blank=True, null=True, verbose_name='Nome do Pai')
    nome_mae = models.CharField(max_length=200, verbose_name='Nome da Mãe')
    data_cadastramento = models.DateTimeField()
    data_ultima_atualizacao = models.DateTimeField(blank=True, null=True)
    
    area_ultimo_curso_superior = models.CharField(max_length=1, choices=AREA_SUPERIOR_CHOICES, verbose_name='Área do último curso superior')
    ultimo_curso_titulacao = models.CharField(max_length=200, verbose_name='Último curso de titulação')
    instituicao_titulacao = models.CharField(max_length=200, verbose_name="Nome da Instituição de Titulação")
    
    def __str__(self):
        return "Documentos de " + self.pessoa.nome
    
    class Meta:
        verbose_name = 'CM - Pessoa - Documentação'