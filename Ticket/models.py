from tabnanny import verbose
from django.db import models
from django.forms import CharField
from Curso.models import CM_curso

from Acesso_Restrito.models import CM_pessoa

# Create your models here.
class Setor(models.Model):
    nome_setor = models.CharField(max_length=50, verbose_name="Nome do Setor")
    email = models.EmailField(verbose_name="E-mail do Setor")

    def __str__(self):
        return self.nome_setor

class Funcionario(models.Model):
    pessoa = models.ForeignKey(CM_pessoa, on_delete=models.RESTRICT)
    setor = models.ForeignKey(Setor, on_delete=models.RESTRICT)
    is_coordenador = models.BooleanField(default=False, help_text = "Marque caso o funcionário seja coordenador do setor", verbose_name='Coordenadoria')

    def __str__(self):
        return self.pessoa.nome

    class Meta:
        verbose_name = 'Funcionário'


class Categoria(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

class Solicitacao(models.Model):
    STATUS_CHOICES = (
        ('A', 'Em aberto'),
        ('E', 'Em andamento'),
        ('F', 'Fechado'),
        ('P', 'Pendente'),
    )

    # ABERTURA
    data_abertura = models.DateTimeField(verbose_name="Data de Abertura", null=True, blank=True)
    solicitante = models.ForeignKey(Funcionario, on_delete=models.RESTRICT, verbose_name="Solicitante", null=True, blank=True)
    anexo = models.ImageField(upload_to='', blank=True, null=True)
    assunto = models.CharField(max_length=50)
    categoria = models.ForeignKey(Categoria, on_delete=models.RESTRICT)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="A")
    ultima_alteracao = models.DateTimeField(verbose_name="Última alteração", null=True, blank=True)
    
    # EM ANDAMENTO
    data_recebimento = models.DateTimeField(verbose_name="Data de Recebimento", null=True, blank=True)
    executante = models.ForeignKey(Funcionario, on_delete=models.RESTRICT, related_name="executante", null=True, blank=True)

    def __str__(self):
        return str(self.data_abertura.date()) + " - Assunto: " + self.assunto + " - Status: " + self.get_status_display()

    class Meta:
        verbose_name = 'Solicitação'
        verbose_name_plural = 'Solicitações'
class MensagemSolicitacao(models.Model):
    autor = models.ForeignKey(Funcionario, on_delete=models.RESTRICT, blank=True, null=True)
    data_mensagem = models.DateTimeField(blank=True, null=True)
    mensagem = models.TextField()
    solicitacao = models.ForeignKey(Solicitacao, on_delete=models.RESTRICT, blank=True, null=True)

    class Meta:
        verbose_name = "Mensagem - Solicitação"
        verbose_name_plural = "Mensagens - Solicitção"

    def __str__(self):
        return self.autor.pessoa.nome + " - " + str(self.data_mensagem)

TIPO_CURSO_CHOICES = (
    ('gra', 'Graduação'),
    ('esp', 'Especialização'),
    ('mes', 'Mestrado'),
    ('dou', 'Doutorado'),
    ('ext', 'Extensão'),
    ('cur', 'Curso Livre'),
)

STATUS_CHOICES = (
        ('A', 'Aberto'),
        ('E', 'Em Andamento'),
        ('P', 'Pendente'),
        ('F', 'Fechado')
    )

class SolicitacaoDisciplina(models.Model):
    solicitante = models.ForeignKey(CM_pessoa, on_delete=models.RESTRICT)
    professor_responsavel = models.CharField(max_length=255, verbose_name="Professor Responsável")
    siape = models.CharField(max_length=7, verbose_name="SIAPE")
    email = models.EmailField(verbose_name="E-mail")
    CATEGORIA_CHOICES = (
        ('SIGA/UAB', 'Correspondência no SIGA/UAB'),
        ('SIGA/Flex', 'Correspondência no SIGA/Flexibilização Curricular'),
        ('Livre', 'Sem Correspondência no SIGA/Curso Livre')
    )
    categoria = models.CharField(max_length=9, choices=CATEGORIA_CHOICES)
    unidade_lotacao = models.CharField(max_length=50, verbose_name="Unidade de Lotação")
    codigo_siga = models.CharField(max_length=30, verbose_name="Código SIGA", blank=True, null=True)
    nome_disciplina = models.CharField(max_length=255, verbose_name="Nome da Disciplina")
    tipo_curso = models.CharField(max_length=3, choices=TIPO_CURSO_CHOICES, verbose_name="Tipo de Curso")
    curso_disciplina = models.ForeignKey(CM_curso, on_delete=models.RESTRICT, verbose_name="A qual curso pertence a disciplina")
    departamento_disciplina = models.CharField(max_length=255, verbose_name="A qual departamento pertence a disciplina")
    ano = models.CharField(max_length=4)
    semestre = models.CharField(max_length=1, choices=(('1','1'),('2','2'),('3','3'), ('4','4')))
    turma = models.CharField(max_length=12, verbose_name="Turmas pelas quais sou responsável")
    grupos = models.CharField(max_length=64, null=True, blank=True, verbose_name="Grupos (ex.: AB, C, ...)")
    conteudo_passado = models.CharField(max_length=255, null=True, blank=True, verbose_name="Favor informar o nome breve da disciplina a importar")
    MODO_INSCRICAO_ALUNOS_CHOICES = (
        ('ime', 'Imediatamente'),
        ('pos', 'Posteriormente'),
    )
    modo_inscricao_alunos = models.CharField(max_length=3, choices=MODO_INSCRICAO_ALUNOS_CHOICES, verbose_name="Alunos constantes naa FAE (SIGA) devem ser inscritos")
    atividades_inicio = models.DateField()
    atividades_fim = models.DateField()

    data_abertura = models.DateTimeField(blank=True, null=True)
    
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    ultima_atualizacao = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "Solicitação de Disciplina"
        verbose_name_plural = "Solicitações de Disciplina"

class SolicitacaoCurso(models.Model):
    solicitante = models.ForeignKey(CM_pessoa, on_delete=models.RESTRICT)
    
    professor_responsavel = models.CharField(max_length=255, verbose_name="Professor Responsável")
    siape = models.CharField(max_length=7, verbose_name="SIAPE")
    unidade_lotacao = models.CharField(max_length=50, verbose_name="Unidade de Lotação")
    nome_curso = models.CharField(max_length=255, verbose_name="Nome do Curso")
    email = models.EmailField(verbose_name="E-mail")
    tipo_curso = models.CharField(max_length=3, choices=TIPO_CURSO_CHOICES, verbose_name="Tipo de Curso")
    CARACTERISTICAS_CHOICES = (
        ('UAB', 'UAB'),
        ('Não UAB', 'Não UAB'),
        ('ERE', 'ERE'),
        ('Híbrido', 'Híbrido'),
        ('Gratuito', 'Gratuito')
    )
    caracteristicas = models.CharField(max_length=8, choices=CARACTERISTICAS_CHOICES, verbose_name="Características")
    qtd_disciplinas = models.PositiveIntegerField(verbose_name="Quantidade de Disciplinas")
    inscricoes_inicio = models.DateField(verbose_name="Início das Inscrições")
    inscricoes_fim = models.DateField(verbose_name="Fim das Inscrições")
    curso_inicio = models.DateField(verbose_name="Início do Curso")
    curso_fim = models.DateField(verbose_name="Fim do Curso")
    # Quantidade de Interlocutores Envolvidos
    professores = models.PositiveIntegerField()
    tutores = models.PositiveIntegerField()
    demais_colaboradores = models.PositiveIntegerField()
    alunos = models.PositiveIntegerField()
    # Tipo de Demanda Requerida
    criacao_AVA = models.BooleanField(verbose_name="Criação de AVA", default=False, blank=True)
    matricula_alunos = models.BooleanField(verbose_name="Matrícula de Alunos", default=False, blank=True)
    capacitacao_interlocutores = models.BooleanField(verbose_name="Capacitação de Interlocutores", default=False, blank=True)
    outra = models.TextField(blank=True, null=True)
    producao_material = models.BooleanField(verbose_name="Acionamento do setor de produção de material do CEAD", default=False, blank=True)
    assessoria_comunicacao = models.BooleanField(verbose_name="Assessoria de comunicação para sua divulgação", default=False, blank=True)
    ambiente_pre_formatado = models.BooleanField(
        verbose_name="Seu curso/disciplina deseja ambiente pré formatado?", 
        help_text="O CEAD disponibiliza um Ambiente Modelo Pré Formatado para graduação e pós**",
        default=False, 
        blank=True)
    
    data_abertura = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    ultima_atualizacao = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.pk) + '. ' + self.nome_curso

    class Meta:
        verbose_name = "Solicitação de Curso"
        verbose_name_plural = "Solicitações de Curso"