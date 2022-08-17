import datetime
from io import StringIO
from operator import itemgetter
from django.utils import timezone
from django import forms
from django.shortcuts import render
import matplotlib

from procead.filters import Filter
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib.ticker import PercentFormatter
import numpy
from Acesso_Restrito.models import CM_pessoa
from Ticket.filters import SolicitacaoFilter
from Ticket.forms import MensagemSolicitacaoForm, RelatorioForm, SolicitacaoAprovacaoForm, SolicitacaoCursoForm, SolicitacaoDisciplinaForm, SolicitacaoForm
from Ticket.models import Categoria, MensagemSolicitacao, Setor, Funcionario, Solicitacao, SolicitacaoCurso, SolicitacaoDisciplina

from procead.views import *

# Create your views here.
def Solicitacoes(request):
    return render(request, 'Ticket/ticket.html')

def SolicitacaoAVA(request):
    return render(request, 'Ticket/ticket_AVA.html')

def SolicitacaoCreate(request):
    pessoa = CM_pessoa.objects.filter(cpf=request.user.username).first()

    if request.user.groups.filter(name__icontains="Funcionário do CEAD"):
        print("Chamex")
    else:
        print("Gol")

    if Funcionario.objects.filter(pessoa=pessoa):
        solicitante = Funcionario.objects.filter(pessoa=pessoa).first()
    else:
        solicitante = None

    if request.method == 'POST':
        form = SolicitacaoForm(request.POST, request.FILES)
        form_mensagem = MensagemSolicitacaoForm(request.POST)
        if form.is_valid() and form_mensagem.is_valid():
            updated_form = form.save(commit=False)
            updated_form.solicitante = solicitante
            updated_form.data_abertura = timezone.now()
            updated_form.ultima_alteracao = timezone.now()

            updated_form.save()
            
            updated_form_mensagem = form_mensagem.save(commit=False)
            updated_form_mensagem.data_mensagem = timezone.now()
            updated_form_mensagem.autor = solicitante
            updated_form_mensagem.solicitacao = Solicitacao.objects.last()

            updated_form_mensagem.save()

            messages.success(request, "Solicitação criada com sucesso.")

            return redirect(reverse('ticket-list'))
        else:
            messages.error(request, str(form.errors.as_data()) + str(form_mensagem.errors.as_data()))
    
    form = SolicitacaoForm()
    form_mensagem = MensagemSolicitacaoForm()
    context = {
        'form': form,
        'form_mensagem': form_mensagem,
        'solicitante': solicitante,
    }
    return render(request, 'Ticket/ticket_create.html', context)

def SolicitacaoUpdateView(request, solicitacao_id):
    solicitacao = Solicitacao.objects.get(id=solicitacao_id)
    solicitante = solicitacao.solicitante
    mensagem = solicitacao.mensagemsolicitacao_set.last()

    if request.method == 'POST':
        form = SolicitacaoForm(request.POST, request.FILES, instance=solicitacao)
        form_mensagem = MensagemSolicitacaoForm(request.POST, instance=mensagem)
        if form.is_valid() and form_mensagem.is_valid():
            updated_form = form.save(commit=False)
            updated_form.solicitante = solicitante
            updated_form.data_abertura = timezone.now()
            updated_form.ultima_alteracao = timezone.now()

            updated_form.save()
            
            updated_form_mensagem = form_mensagem.save(commit=False)
            updated_form_mensagem.data_mensagem = timezone.now()
            updated_form_mensagem.autor = solicitante
            updated_form_mensagem.solicitacao = solicitacao

            updated_form_mensagem.save()

            messages.success(request, "Solicitação editada com sucesso.")

            return redirect(reverse('ticket-list'))
        else:
            messages.error(request, str(form.errors.as_data()) + str(form_mensagem.errors.as_data()))
    
    form = SolicitacaoForm(instance=solicitacao)
    form_mensagem = MensagemSolicitacaoForm(instance=mensagem)
    context = {
        'form': form,
        'form_mensagem': form_mensagem,
        'solicitante': solicitante,
    }
    return render(request, 'Ticket/ticket_create.html', context)

def SolicitacaoListView(request):
    pessoa = CM_pessoa.objects.filter(cpf=request.user.username).first()
    form = MensagemSolicitacaoForm()
    if Funcionario.objects.filter(pessoa=pessoa):
        funcionario = Funcionario.objects.filter(pessoa=pessoa).first()
        
        if funcionario.setor.nome_setor == "Desenvolvimento":
            # Caso o funcionario seja do Deselnvolvimento, aparecem todas as Solicitações do sistema
            abertos = Solicitacao.objects.filter(status="A").order_by('-data_abertura')
            em_andamento = Solicitacao.objects.filter(status="E").order_by('-data_recebimento')
            pendentes = Solicitacao.objects.filter(status="P").order_by('-ultima_alteracao')
            fechadas = Solicitacao.objects.filter(status="F").order_by('-ultima_alteracao')
        else:
            id_setor = Setor.objects.get(nome_setor=funcionario.setor.nome_setor).id
            funcionarios_do_setor = Funcionario.objects.filter(setor=id_setor)
            solicitacoes_do_setor = Solicitacao.objects.none()
            for servidor in funcionarios_do_setor:
                solicitacoes_do_setor |= Solicitacao.objects.filter(solicitante=servidor)

            # Caso contrário, aparecem apenas as solicitações abertas por aquele funcionário
            abertos = solicitacoes_do_setor.filter(status="A").order_by('-data_abertura')
            em_andamento = solicitacoes_do_setor.filter(status="E").order_by('-data_recebimento')
            pendentes = solicitacoes_do_setor.filter(status="P").order_by('-ultima_alteracao')
            fechadas = solicitacoes_do_setor.filter(status="F").order_by('-ultima_alteracao')
        
        context = {
            'funcionario': funcionario,
            'abertos': abertos,
            'em_andamento': em_andamento,
            'fechadas': fechadas,
            'pendentes': pendentes,
            'form': form
        }
    else:
        funcionario = None
        context = {}

    return render(request, 'Ticket/ticket_list.html', context)

def solicitacaoDeleteView(request, solicitacao_id):
    solicitacao = Solicitacao.objects.get(id=solicitacao_id)
    mensagens = MensagemSolicitacao.objects.filter(solicitacao=solicitacao)

    if request.method == 'POST':
        for mensagem in mensagens:
            mensagem.delete()
        solicitacao.delete()
        messages.success(request, "Solicitação excluída com sucesso!")
        return redirect('ticket-list')
    return render(request, 'Ticket/ticket_delete.html', {'solicitacao': solicitacao})

def assumirSolicitacao(request, solicitacao_id, dev_id):
    executante = Funcionario.objects.get(id=dev_id)
    solicitacao = Solicitacao.objects.get(id=solicitacao_id)
    mensagens = MensagemSolicitacao.objects.filter(solicitacao=solicitacao)
    
    if request.method == 'POST':
        form = MensagemSolicitacaoForm(request.POST)
        if form.is_valid():
            updated_form = form.save(commit=False)
            updated_form.autor = executante
            updated_form.solicitacao = solicitacao
            updated_form.data_mensagem = timezone.now()

            updated_form.save()
            
            solicitacao.executante = executante
            solicitacao.status = 'E'
            solicitacao.data_recebimento = timezone.now()
            solicitacao.ultima_alteracao = timezone.now()
            solicitacao.save(update_fields=['executante', 'status', 'data_recebimento', 'ultima_alteracao'])

            return redirect(reverse('ticket-list'))
        else:
            print(form.errors.as_data())
    form = MensagemSolicitacaoForm()
    placeholder = 'Envie uma mensagem de feedback ao assumir uma solicitação (obrigatório).'
    form.fields['mensagem'].widget.attrs.update({'placeholder': placeholder})

    context = {
        'executante': executante,
        'solicitacao': solicitacao,
        'mensagens': mensagens,
        'form': form
    }

    return render(request, 'Ticket/assumir_ticket.html', context)

def encerrarSolicitacao(request, solicitacao_id, dev_id):
    executante = Funcionario.objects.get(id=dev_id)
    solicitacao = Solicitacao.objects.get(id=solicitacao_id)
    mensagens = MensagemSolicitacao.objects.filter(solicitacao=solicitacao)

    if request.method == 'POST':
        form = MensagemSolicitacaoForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['status'] == 'F':
                solicitacao.status = 'F'
            if form.cleaned_data['status'] == 'P':
                solicitacao.status = 'P'
            solicitacao.ultima_alteracao = timezone.now()
            solicitacao.save(update_fields=['status', 'ultima_alteracao'])
            
            updated_form = form.save(commit=False)
            updated_form.autor = executante
            updated_form.solicitacao = solicitacao
            updated_form.data_mensagem = timezone.now()

            updated_form.save()

            return redirect(reverse('ticket-list'))

    form = MensagemSolicitacaoForm()
    placeholder = 'Envie uma mensagem de feedback ao encerrar uma solicitação (obrigatório).'
    form.fields['mensagem'].widget.attrs.update({'placeholder': placeholder})

    context = {
        'executante': executante,
        'solicitacao': solicitacao,
        'mensagens': mensagens,
        'form': form
    }

    return render(request, 'Ticket/encerrar_ticket.html', context)

def atualizarSolicitacao(request, solicitacao_id):
    solicitacao = Solicitacao.objects.get(id=solicitacao_id)
    mensagens = MensagemSolicitacao.objects.filter(solicitacao=solicitacao)
    pessoa = CM_pessoa.objects.get(cpf=request.user.username)
    solicitante = Funcionario.objects.get(pessoa=pessoa)
    
    if request.method == 'POST':
        form = MensagemSolicitacaoForm(request.POST)
        
        
        if form.is_valid():
            updated_form = form.save(commit=False)
            updated_form.autor = solicitante
            updated_form.solicitacao = solicitacao
            updated_form.data_mensagem = timezone.now()
            updated_form.save()
            
            if form.cleaned_data['encerrar']:
                solicitacao.status = 'F'
            solicitacao.ultima_alteracao = timezone.now()
            solicitacao.save(update_fields=['status', 'ultima_alteracao'])

            return redirect(reverse('ticket-list'))
        else:
            print(form.errors.as_data())
    form = MensagemSolicitacaoForm()
    placeholder = 'Envie uma mensagem de feedback de atualização uma solicitação (obrigatório).'
    form.fields['mensagem'].widget.attrs.update({'placeholder': placeholder})

    context = {
        'solicitante': solicitante,
        'solicitacao': solicitacao,
        'mensagens': mensagens,
        'form': form
    }

    return render(request, 'Ticket/atualizar_ticket.html', context)

def FechadasListView(request, consulta=''):
    if request.method == 'POST':
        filter = Filter(request.POST)
        if filter.is_valid():
            return redirect('fechadas-list', filter.cleaned_data['consulta'])

    filter = Filter()

    if consulta:
        fechadas_assunto = Solicitacao.objects.filter(status='F').filter(assunto__icontains=consulta)
        fechadas_responsavel = Solicitacao.objects.filter(status='F').filter(executante__pessoa__nome__icontains=consulta)
        fechadas_categoria = Solicitacao.objects.filter(status='F').filter(categoria__nome__icontains=consulta)
        fechadas_setor = Solicitacao.objects.filter(status='F').filter(solicitante__setor__nome_setor__icontains=consulta)
        
        fechadas = Solicitacao.objects.none()
        fechadas |= fechadas_assunto
        fechadas |= fechadas_responsavel
        fechadas |= fechadas_categoria
        fechadas |= fechadas_setor
    else:
        fechadas = Solicitacao.objects.filter(status='F').order_by('-ultima_alteracao')
    pessoa = CM_pessoa.objects.get(cpf=request.user.username)
    funcionario = Funcionario.objects.get(pessoa=pessoa)
    
    paginator = Paginator(fechadas, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'fechadas': fechadas,
        'page_obj': page_obj,
        'funcionario': funcionario,
        'filter': filter
    }
    return render(request, 'Ticket/fechadas_list.html', context)

def solicitacaoRelatorio(request, consulta="", intervalo=(timezone.now().date() - timezone.timedelta(days=30)).isoformat()+'-'+timezone.now().date().isoformat()):
    # Verifica se o formulário foi preenchido corretamente para redirecionar para a página com o gráfico de interesse
    if request.method == 'POST':
        form = RelatorioForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['data_inicio'] <= form.cleaned_data['data_fim']:
                return redirect('ticket-relatorios', intervalo=form.cleaned_data['data_inicio'].isoformat()+'-'+form.cleaned_data['data_fim'].isoformat())
            messages.error(request, "A data de início não pode ser anterior à data de fim.")
    
    form = RelatorioForm()
            
    # converte a string do cabeçalho para o formato de data aware
    data_inicio = timezone.make_aware(datetime.datetime.strptime(intervalo[:10], "%Y-%m-%d"))
    data_fim = timezone.make_aware(datetime.datetime.strptime(intervalo[11:], "%Y-%m-%d")) + timezone.timedelta(hours=23, minutes=59, seconds=59)

    # separa as solicitações por status
    todas_abertas = Solicitacao.objects.filter(status='A')
    todas_em_andamento = Solicitacao.objects.filter(status='E')
    todas_pendentes = Solicitacao.objects.filter(status='P')
    todas_fechadas = Solicitacao.objects.filter(status='F')

    # conta a quandidade de solicitações de cada status
    abertas = len(todas_abertas)
    em_andamento = len(todas_em_andamento)
    pendentes = len(todas_pendentes)
    fechadas = len(todas_fechadas)

    abertas_periodo = 0
    em_andamento_periodo = 0
    pendentes_periodo = 0
    fechadas_periodo = 0
    
    # conta a quantidade de solicitações de cada status no período solilcitado
    for item in todas_abertas:
        if item.data_abertura >= data_inicio and item.data_abertura <= data_fim:
            abertas_periodo += 1

    for item in todas_em_andamento:
        if item.data_recebimento >= data_inicio and item.data_recebimento <= data_fim:
            em_andamento_periodo += 1

    for item in todas_pendentes:
        if item.ultima_alteracao >= data_inicio and item.ultima_alteracao <= data_fim:
            pendentes_periodo += 1

    for item in todas_fechadas:
        if item.ultima_alteracao >= data_inicio and item.ultima_alteracao <= data_fim:
            fechadas_periodo += 1

    colors = ["#008400", "#edaf1a", "#e26666", "#8d8d8d"]


    # Gráfico de solicitações
    x = ('Abertas', 'Em Andamento', 'Pendentes', 'Fechadas')
    y = (abertas, em_andamento, pendentes, fechadas)

    fig = plt.figure()
    plt.bar(x, y, color=colors)
    plt.grid(axis='y', linestyle = '--', linewidth = 0.5)
    plt.title('Solicitações no Sistema')

    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)

    solicitacoes = imgdata.getvalue()

    plt.close()


    # Gráfico de solicitações por período
    x = ('Abertas', 'Em Andamento', 'Pendentes', 'Fechadas')
    y = (abertas_periodo, em_andamento_periodo, pendentes_periodo, fechadas_periodo)

    fig = plt.figure()
    plt.bar(x, y, color=colors)
    plt.grid(axis='y', linestyle = '--', linewidth = 0.5)
    plt.title('Solicitações no período de ' + data_inicio.strftime('%d/%m/%Y') + ' a ' + data_fim.strftime('%d/%m/%Y'))

    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)

    solicitacoes_por_periodo = imgdata.getvalue()

    plt.close()

    
    # Gráfico de solicitações pendentes por categoria
    solicitacoes_pendentes_por_categoria = []
    for categoria in Categoria.objects.all():
        solicitacoes_pendentes_por_categoria.append((categoria.nome, len(Solicitacao.objects.filter(categoria=categoria).filter(status="P"))))
    solicitacoes_pendentes_por_categoria = sorted(solicitacoes_pendentes_por_categoria, key=itemgetter(1), reverse=True)

    x = [item[0] for item in solicitacoes_pendentes_por_categoria]
    y = [item[1] for item in solicitacoes_pendentes_por_categoria]

    if y == [0]:
        total = 1
    else:
        total = 0
        
    for value in y:
        total += value

    perc_y = []
    for index in range(len(y)):
        if(perc_y):
            perc_y.append((y[index] / total) + perc_y[-1])
        else:
            perc_y.append(y[index] / total)
    perc_y = [item*100 for item in perc_y]

    fig, ax = plt.subplots()
    plt.title("Solicitações pendentes por categoria")
    plt.grid(axis='y', linestyle = '--', linewidth = 0.5)
    ax.bar(x, y, color=colors[2])
    ax.plot(x, y, marker="D", ms=4, color="#fdb913")

    ax2 = ax.twinx()
    ax2.plot(x, perc_y, marker="D", ms=4, color="#0088ff")
    
    ax2.yaxis.set_major_formatter(PercentFormatter())

    ax.tick_params(axis='y', colors=colors[2])
    ax2.tick_params(axis='y', colors="#0088ff")

    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)

    solicitacoes_pendentes = imgdata.getvalue()

    plt.close()
    
    
    # Gráfico de solicitações abertas por setor
    solicitacoes_abertas_por_setor = []
    for solicitacao in Solicitacao.objects.all():
        if not solicitacoes_abertas_por_setor:
            solicitacoes_abertas_por_setor.append([solicitacao.solicitante.setor.nome_setor, 1])
        elif solicitacao.solicitante.setor.nome_setor not in [item[0] for item in solicitacoes_abertas_por_setor]:
            solicitacoes_abertas_por_setor.append([solicitacao.solicitante.setor.nome_setor, 1])
        else:
            for item in solicitacoes_abertas_por_setor:
                if item[0] == solicitacao.solicitante.setor.nome_setor:
                    item[1] += 1

    solicitacoes_abertas_por_setor = sorted(solicitacoes_abertas_por_setor, key=itemgetter(1), reverse=True)
    x = [item[0] for item in solicitacoes_abertas_por_setor]
    y = [item[1] for item in solicitacoes_abertas_por_setor]

    for setor in Setor.objects.all():
        if setor.nome_setor not in x:
            x.append(setor.nome_setor)
            y.append(0)

    total = 0
    for value in y:
        total += value
    if total == 0: total = 1

    perc_y = []
    for index in range(len(y)):
        if(perc_y):
            perc_y.append((y[index] / total) + perc_y[-1])
        else:
            perc_y.append(y[index] / total)
    perc_y = [item*100 for item in perc_y]

    fig, ax = plt.subplots()
    plt.title('Solicitações abertas por setor')
    plt.grid(axis='y', linestyle = '--', linewidth = 0.5)
    ax.bar(x, y, color=colors[0])
    ax.plot(x, y, marker="D", ms=4, color="#fdb913")
    
    ax2 = ax.twinx()
    ax2.plot(x, perc_y, marker="D", ms=4, color="#0088ff", label="pareto")
    
    ax2.yaxis.set_major_formatter(PercentFormatter())

    ax.tick_params(axis='y', colors=colors[2])
    ax2.tick_params(axis='y', colors="#0088ff")

    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)

    solicitacoes_abertas_por_setor = imgdata.getvalue()

    plt.close()

    context = {
        'solicitacoes': solicitacoes,
        'solicitacoes_por_periodo': solicitacoes_por_periodo,
        'solicitacoes_pendentes': solicitacoes_pendentes,
        'solicitacoes_abertas_por_setor': solicitacoes_abertas_por_setor,
        'data_inicio': data_inicio,
        'data_fim': data_fim,

        'form': form,
    }

    return render(request, 'Ticket/relatorios.html', context)

def SolicitacaoDisciplinaCreate(request):
    solicitante = CM_pessoa.objects.get(cpf=request.user.username)
    if request.method == 'POST':
        form = SolicitacaoDisciplinaForm(request.POST)
        if form.is_valid():
            nova_solicitacao = form.save(commit=False)
            nova_solicitacao.solicitante = solicitante
            nova_solicitacao.data_abertura = timezone.now()
            nova_solicitacao.status = 'A'
            nova_solicitacao.ultima_atualizacao = timezone.now()
            nova_solicitacao.save()
            messages.success(request, "Solicitação criada com sucesso. Aguarde retorno do setor responsável.")
            return redirect('solicitacao-disciplina-list')

    form = SolicitacaoDisciplinaForm()
    form.fields['atividades_inicio'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), label="Data de início da disciplina")
    form.fields['atividades_fim'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), label="Data de término da disciplina")
    form.fields['ano'].widget.attrs.update({'class': ''})
    form.fields['turma'].widget.attrs.update({'class': 'num'})
    form.fields['siape'].widget.attrs.update({'class': 'siape'})
    context = {
        'form': form,
        'solicitante': solicitante
    }
    return render(request, 'Ticket/solicitacao_disciplina_form.html', context)

def SolicitacaoDisciplinaListView(request):
    abertas = SolicitacaoDisciplina.objects.filter(status='A').order_by('-data_abertura')
    em_andamento = SolicitacaoDisciplina.objects.filter(status='E').order_by('-data_abertura')
    pendentes = SolicitacaoDisciplina.objects.filter(status='P').order_by('-data_abertura')
    fechadas = SolicitacaoDisciplina.objects.filter(status='F').order_by('-data_abertura')

    context = {
        'abertas': abertas,
        'em_andamento': em_andamento,
        'pendentes': pendentes,
        'fechadas': fechadas
    }
    return render(request, 'Ticket/solicitacao_disciplina_list.html', context)

def SolicitacaoDisciplinaAprovacaoAcademico(request, solicitacao_id):
    solicitacao = SolicitacaoDisciplina.objects.get(pk=solicitacao_id)
    if request.method == 'POST':
        form = SolicitacaoAprovacaoForm(request.POST)
        if form.is_valid():
            if form.cleaned_data.get('aprovacao') == 'Aprovar':
                solicitacao.status = 'E'
                solicitacao.save(update_fields=['status'])
                return redirect('solicitacao-disciplina-list')
    form = SolicitacaoAprovacaoForm()
    context = {
        'solicitacao': solicitacao,
        'form': form
    }
    return render(request, 'Ticket/solicitacao_academico.html', context)

def SolicitacaoCursoListView(request):
    abertas = SolicitacaoCurso.objects.filter(status='A').order_by('-data_abertura')
    em_andamento = SolicitacaoCurso.objects.filter(status='E').order_by('-data_abertura')
    pendentes = SolicitacaoCurso.objects.filter(status='P').order_by('-data_abertura')
    fechadas = SolicitacaoCurso.objects.filter(status='F').order_by('-data_abertura')

    context = {
        'abertas': abertas,
        'em_andamento': em_andamento,
        'pendentes': pendentes,
        'fechadas': fechadas
    }
    return render(request, 'Ticket/solicitacao_curso_list.html', context)

class SolicitacaoCursoCreate(LoginRequiredMixin, CreateView):
    form_class = SolicitacaoCursoForm
    template_name = 'Ticket/solicitacao_curso_form.html'

    def form_valid(self, form):
        updated_form = form.save(commit=False)
        updated_form.solicitante = CM_pessoa.objects.get(cpf=self.request.user.username)
        updated_form.data_abertura = timezone.now()
        updated_form.status = 'A'
        updated_form.ultima_atualizacao = timezone.now()
        updated_form.save()
        return redirect('index')
