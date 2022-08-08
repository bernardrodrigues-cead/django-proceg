from tabnanny import verbose
from django.db import models
from django.forms import CharField
from Curso.models import CM_curso

from Acesso_Restrito.models import CM_pessoa

# Create your models here.
class Setor(models.Model):
    nome_setor = models.CharField(max_length=50)
    email = models.EmailField()

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
        verbose_name = "Mensagem - Solicitção"
        verbose_name_plural = "Mensagens - Solicitção"

    def __str__(self):
        return self.autor.pessoa.nome + " - " + str(self.data_mensagem)

class SolicitacaoDisciplina(models.Model):
    solicitante = models.ForeignKey(CM_pessoa, on_delete=models.RESTRICT)
    professor_responsavel = models.CharField(max_length=255, verbose_name="Professor Responsável")
    siape = models.CharField(max_length=64, verbose_name="SIAPE")
    categoria = models.CharField(max_length=10, choices=(('SIGA UFJF', 'SIGA UFJF'),('SIGA UAB', 'SIGA UAB'), ('UFJF Livre', 'UFJF Livre')))
    unidade_lotacao = models.CharField(max_length=50, verbose_name="Unidade de Lotação")
    codigo_siga = models.CharField(max_length=30, verbose_name="Código SIGA", blank=True, null=True)
    nome_disciplina = models.CharField(max_length=255, verbose_name="Nome da Disciplina")
    # nome_breve = models.CharField(max_length=30, verbose_name="Nome Breve")
    TIPO_CURSO_CHOICES = (
        ('gra', 'Graduação'),
        ('esp', 'Especialização'),
        ('mes', 'Mestrado'),
        ('dou', 'Doutorado'),
        ('ext', 'Extensão'),
        ('cur', 'Curso Livre'),
    )
    tipo_curso = models.CharField(max_length=3, choices=TIPO_CURSO_CHOICES)
    curso_disciplina = models.ForeignKey(CM_curso, on_delete=models.RESTRICT, verbose_name="A qual curso pertence a disciplina")
    departamento_disciplina = models.CharField(max_length=255, verbose_name="A qual departamento pertence a disciplina")
    ano = models.CharField(max_length=4)
    semestre = models.CharField(max_length=1, choices=(('1','1'),('2','2'),('3','3'), ('4','4')), verbose_name="Período")
    turma = models.CharField(max_length=100, blank=True, null=True, verbose_name="Turma (ex.: A, B, C)")
    conteudo_passado = models.CharField(max_length=255, null=True, blank=True, verbose_name="Favor informar a disciplina, código, ano, semestre e turma a importar")
    MODO_INSCRICAO_ALUNOS_CHOICES = (
        ('ime', 'Imediatamente'),
        ('pos', 'Posteriormente'),
    )
    modo_inscricao_alunos = models.CharField(max_length=3, choices=MODO_INSCRICAO_ALUNOS_CHOICES, verbose_name="Alunos constantes naa FAE (SIGA) devem ser inscritos")
    atividades_inicio = models.DateField()
    atividades_fim = models.DateField()
    # observacao = models.TextField(verbose_name="Observação")

    data_abertura = models.DateTimeField(blank=True, null=True)
    STATUS_CHOICES = (
        ('A', 'Aberto'),
        ('E', 'Em Andamento'),
        ('P', 'Pendente'),
        ('F', 'Fechado')
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    ultima_atualizacao = models.DateTimeField(blank=True, null=True)