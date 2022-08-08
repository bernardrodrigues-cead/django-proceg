from Acesso_Restrito.models import CM_cidade, CM_dados_bancarios, CM_pessoa_documentacao
from procead.views import *

import random
import string
from django.shortcuts import render
from Curso.forms import CM_cidadeForm
from Curso.models import CM_curso, CM_pessoa
from Financeiro.forms import passo1Form, passo2Form, passo3Form, passo4FormPessoa, passo4FormPessoaDocumentacao, passo5Form
from Financeiro.models import CM_pessoa_bolsa, FI_bolsa

# from procead.qtpdf.generate import generate_pdf

# Create your views here.
#Financeiro
@login_required(login_url='/accounts/login/')
def FinanceiroView(request):
    return render(request, 'procead/financeiro/financeiro.html', {})

#Submenus de Financeiro
@login_required(login_url='/accounts/login/')
def BolsistaView(request):
    return render(request, 'procead/financeiro/bolsista.html', {})

@login_required(login_url='/accounts/login/')
def DesvincularBolsistaView(request):
    return render(request, 'procead/financeiro/desvincular_bolsista.html', {})

@login_required(login_url='/accounts/login/')
def PagamentoView(request):
    return render(request, 'procead/financeiro/pagamento.html', {})

@login_required(login_url='/accounts/login/')
def FrequenciaView(request):
    return render(request, 'procead/financeiro/frequencia.html', {})

@login_required(login_url='/accounts/login/')
def RelatoriosControleDeBolsistasView(request):
    return render(request, 'procead/financeiro/relatorio_controle_de_bolsistas.html', {})


#####################################################
# FICHA UAB #
#####################################################

# As views a seguir correspondem à formulação das fichas UAB de bolsistas


def passo1View(request):
    """Passo para verificação se o candidato à bolsa já está no sistema CEAD"""
    if request.method == 'POST':
        form = passo1Form(request.POST)
        if form.is_valid():
            pessoa = CM_pessoa.objects.exclude(cpf='000.000.000-00').filter(cpf=form.cleaned_data['cpf']).first()
            if(pessoa and pessoa.data_nascimento == form.cleaned_data['data_nascimento']):
                messages.success(request, "Email enviado")
                return redirect('passo2', pessoa.unique_id)
            else:
                messages.error(request, 'CPF e/ou Data de Nascimento não cadastrados em nossa base de dados.')
    form = passo1Form()
    context = {
        'form': form
    }
    return render(request, 'fichaUAB/passo1.html', context)

def passo2View(request, pessoa_uuid):
        
    if request.method == 'POST':
        form = passo2Form(request.POST)
        if form.is_valid():
            # if codigo == form.cleaned_data['codigo']:
            if form.cleaned_data['codigo'] == request.session.get('codigo'):
                return redirect('passo3', pessoa_uuid)
            else:
                messages.error(request, "Código não corresponde ao informado por e-mail.")
                return redirect('passo2', pessoa_uuid)
                
    # gera um código de 6 caracteres
    codigo = ""
    for _ in range(6):
        codigo += random.choice(string.ascii_letters)
    request.session['codigo'] = codigo
    pessoa = CM_pessoa.objects.filter(unique_id=pessoa_uuid).first()
    form = passo2Form()
    context = {
        'form': form,
        'pessoa': pessoa,
        'codigo': codigo
    }
    return render(request, 'fichaUAB/passo2.html', context)

def passo3View(request, pessoa_uuid):
    pessoa = CM_pessoa.objects.filter(unique_id=pessoa_uuid).first()
    if request.method == 'POST':
        form = passo3Form(request.POST)
        if form.is_valid():
            curso_id = form.cleaned_data['curso'].id
            bolsa_id = form.cleaned_data['bolsa'].id
            request.session['curso_id'] = curso_id
            request.session['bolsa_id'] = bolsa_id
            return redirect('passo4', pessoa_uuid)
    form = passo3Form()
    context = {
        'form': form,
        'pessoa': pessoa
    }
    return render(request, 'fichaUAB/passo3.html', context)

def passo4View(request, pessoa_uuid):
    instance_pessoa = CM_pessoa.objects.filter(unique_id=pessoa_uuid).first()
    if request.method == 'POST':
        form_pessoa = passo4FormPessoa(request.POST, instance=instance_pessoa)
        form_cidade = CM_cidadeForm(request.POST)
        try:
            instance_documentacao = instance_pessoa.cm_pessoa_documentacao
            form_documentacao = passo4FormPessoaDocumentacao(request.POST, instance=instance_documentacao)
        except:
            form_documentacao = passo4FormPessoaDocumentacao(request.POST)
        if form_cidade.is_valid():
            form_cidade.save()
        elif form_pessoa.is_valid() and form_documentacao.is_valid():
            
            # Foi necessario informar dado a dado, pois o Django não serializa alguns tipos
            pessoa_data = form_pessoa.clean()
            request.session['pessoa_data'] = {
                'nome': pessoa_data['nome'],
                'sexo': pessoa_data['sexo'],
                'cpf': pessoa_data['cpf'],
                'data_nascimento': str(pessoa_data['data_nascimento']),
                'rua': pessoa_data['rua'],
                'numero': pessoa_data['numero'],
                'complemento': pessoa_data['complemento'],
                'bairro': pessoa_data['bairro'],
                'uf': pessoa_data['uf'],
                'cidade': pessoa_data['cidade'].id,
                'cep': pessoa_data['cep'],
                'email': pessoa_data['email'],
                'ddd1': pessoa_data['ddd1'],
                'telefone1': pessoa_data['telefone1'],
                'ddd2': pessoa_data['ddd2'],
                'telefone2': pessoa_data['telefone2']
            }
            
            documentacao_data = form_documentacao.clean()
            request.session['documentacao_data'] = {
                'profissao': documentacao_data['profissao'],
                'tipo_documento': documentacao_data['tipo_documento'],
                'documento': documentacao_data['documento'],
                'data_emissao_documento': str(documentacao_data['data_emissao_documento']),
                'orgao_expeditor_documento': documentacao_data['orgao_expeditor_documento'],
                'uf_nascimento': documentacao_data['uf_nascimento'],
                'cidade_nascimento': documentacao_data['cidade_nascimento'].id,
                'nacionalidade': documentacao_data['nacionalidade'],
                'estado_civil': documentacao_data['estado_civil'],
                'nome_conjuge': documentacao_data['nome_conjuge'],
                'nome_pai': documentacao_data['nome_pai'],
                'nome_mae': documentacao_data['nome_mae'],
                'area_ultimo_curso_superior': documentacao_data['area_ultimo_curso_superior'],
                'ultimo_curso_titulacao': documentacao_data['ultimo_curso_titulacao'],
                'instituicao_titulacao': documentacao_data['instituicao_titulacao']
            }
            
            return redirect('passo5', pessoa_uuid)
        else:
            print(form_pessoa.errors.as_data())
            print(form_documentacao.errors.as_data())
            
    form_pessoa = passo4FormPessoa(instance=instance_pessoa)
    form_cidade = CM_cidadeForm()
    form_pessoa.fields['data_nascimento'].widget.attrs.update({'readonly': '', 'class': 'username-readonly'})
    form_pessoa.fields['cpf'].widget.attrs.update({'readonly': '', 'class': 'username-readonly'})
    
    try:
        instance_documentacao = instance_pessoa.cm_pessoa_documentacao
        form_documentacao = passo4FormPessoaDocumentacao(instance=instance_documentacao)
    except:
        form_documentacao = passo4FormPessoaDocumentacao()
    
    context = {
        'form_pessoa': form_pessoa,
        'form_cidade': form_cidade,
        'form_documentacao': form_documentacao
    }
    return render(request, 'fichaUAB/passo4.html', context)

def passo5View(request, pessoa_uuid):
    instance_pessoa = CM_pessoa.objects.filter(unique_id=pessoa_uuid).first()
    
    if request.method == 'POST':
        try:
            instance_banco = instance_pessoa.cm_pessoa_documentacao.banco
            form = passo5Form(request.POST, instance=instance_banco)
        except:
            form = passo5Form(request.POST)
        if form.is_valid():
            # Nesse ponto iremos salvar todos os dados armazenados na sessão
            
            #CM_pessoa_bolsa
            new_curso = CM_curso.objects.filter(pk=request.session.get('curso_id')).first()
            new_bolsa = FI_bolsa.objects.filter(pk=request.session.get('bolsa_id')).first()
            new_cm_pessoa_bolsa = CM_pessoa_bolsa(
                pessoa=instance_pessoa,
                curso=new_curso,
                bolsa=new_bolsa
            )
            new_cm_pessoa_bolsa.save()
            
            #CM_pessoa
            instance_pessoa.nome = request.session.get('pessoa_data')['nome']
            instance_pessoa.sexo = request.session.get('pessoa_data')['sexo']
            instance_pessoa.cpf = request.session.get('pessoa_data')['cpf']
            instance_pessoa.data_nascimento = request.session.get('pessoa_data')['data_nascimento']
            instance_pessoa.rua = request.session.get('pessoa_data')['rua']
            instance_pessoa.numero = request.session.get('pessoa_data')['numero']
            instance_pessoa.complemento = request.session.get('pessoa_data')['complemento']
            instance_pessoa.bairro = request.session.get('pessoa_data')['bairro']
            instance_pessoa.uf = request.session.get('pessoa_data')['uf']
            instance_pessoa.cidade = CM_cidade.objects.filter(pk=request.session.get('pessoa_data')['cidade']).first()
            instance_pessoa.cep = request.session.get('pessoa_data')['cep']
            instance_pessoa.email = request.session.get('pessoa_data')['email']
            instance_pessoa.ddd1 = request.session.get('pessoa_data')['ddd1']
            instance_pessoa.telefone1 = request.session.get('pessoa_data')['telefone1']
            instance_pessoa.ddd2 = request.session.get('pessoa_data')['ddd2']
            instance_pessoa.telefone2 = request.session.get('pessoa_data')['telefone2']
            instance_pessoa.save(update_fields=[
                'nome',
                'sexo',
                'cpf',
                'data_nascimento',
                'rua',
                'numero',
                'complemento',
                'bairro',
                'uf',
                'cidade',
                'cep',
                'email',
                'ddd1',
                'telefone1',
                'ddd2',
                'telefone2',
            ])
                
            #CM_dados_bancarios
            try:
                instance_banco.banco = form.cleaned_data['banco']
                instance_banco.agencia = form.cleaned_data['agencia']
                instance_banco.digito_verificador_agencia = form.cleaned_data['digito_verificador_agencia']
                instance_banco.conta = form.cleaned_data['conta']
                instance_banco.digito_verificador_conta = form.cleaned_data['digito_verificador_conta']
                instance_banco.operacao = form.cleaned_data['operacao']
                instance_banco.save(update_fields=[
                    'banco',
                    'agencia',
                    'digito_verificador_agencia',
                    'conta',
                    'digito_verificador_conta',
                    'operacao'
                ])
            except:
                instance_banco = CM_dados_bancarios(
                    banco=form.cleaned_data['banco'],
                    agencia=form.cleaned_data['agencia'],
                    digito_verificador_agencia=form.cleaned_data['digito_verificador_agencia'],
                    conta=form.cleaned_data['conta'],
                    digito_verificador_conta=form.cleaned_data['digito_verificador_conta'],
                    operacao=form.cleaned_data['operacao']
                )
                instance_banco.save()
            
            #CM_pessoa_documentacao
            try:
                #Caso a pessoa já tenha cadastro de documentos
                instance_documentacao = instance_pessoa.cm_pessoa_documentacao
                instance_documentacao.profissao = request.session.get('documentacao_data')['profissao']
                instance_documentacao.tipo_documento = request.session.get('documentacao_data')['tipo_documento']
                instance_documentacao.documento = request.session.get('documentacao_data')['documento']
                instance_documentacao.data_emissao_documento = request.session.get('documentacao_data')['data_emissao_documento']
                instance_documentacao.orgao_expeditor_documento = request.session.get('documentacao_data')['orgao_expeditor_documento']
                instance_documentacao.uf_nascimento = request.session.get('documentacao_data')['uf_nascimento']
                instance_documentacao.cidade_nascimento = CM_cidade.objects.filter(pk=request.session.get('documentacao_data')['cidade_nascimento']).first()
                instance_documentacao.nacionalidade = request.session.get('documentacao_data')['nacionalidade']
                instance_documentacao.estado_civil = request.session.get('documentacao_data')['estado_civil']
                instance_documentacao.nome_conjuge = request.session.get('documentacao_data')['nome_conjuge']
                instance_documentacao.nome_pai = request.session.get('documentacao_data')['nome_pai']
                instance_documentacao.nome_mae = request.session.get('documentacao_data')['nome_mae']
                instance_documentacao.area_ultimo_curso_superior = request.session.get('documentacao_data')['area_ultimo_curso_superior']
                instance_documentacao.ultimo_curso_titulacao = request.session.get('documentacao_data')['ultimo_curso_titulacao']
                instance_documentacao.instituicao_titulacao = request.session.get('documentacao_data')['instituicao_titulacao']
                instance_documentacao.banco = instance_banco
                instance_documentacao.save(update_fields=[
                    'profissao',
                    'tipo_documento',
                    'documento',
                    'data_emissao_documento',
                    'orgao_expeditor_documento',
                    'uf_nascimento',
                    'cidade_nascimento',
                    'nacionalidade',
                    'estado_civil',
                    'nome_conjuge',
                    'nome_pai',
                    'nome_mae',
                    'area_ultimo_curso_superior',
                    'ultimo_curso_titulacao',
                    'instituicao_titulacao',
                    'banco'
                ])
            except:
                #Caso contrário
                instance_documentacao = CM_pessoa_documentacao(
                    pessoa=instance_pessoa,
                    profissao=request.session.get('documentacao_data')['profissao'],
                    tipo_documento=request.session.get('documentacao_data')['tipo_documento'],
                    documento=request.session.get('documentacao_data')['documento'],
                    data_emissao_documento=request.session.get('documentacao_data')['data_emissao_documento'],
                    orgao_expeditor_documento=request.session.get('documentacao_data')['orgao_expeditor_documento'],
                    uf_nascimento=request.session.get('documentacao_data')['uf_nascimento'],
                    cidade_nascimento=CM_cidade.objects.filter(pk=request.session.get('documentacao_data')['cidade_nascimento']).first(),
                    nacionalidade=request.session.get('documentacao_data')['nacionalidade'],
                    estado_civil=request.session.get('documentacao_data')['estado_civil'],
                    nome_conjuge=request.session.get('documentacao_data')['nome_conjuge'],
                    nome_pai=request.session.get('documentacao_data')['nome_pai'],
                    nome_mae=request.session.get('documentacao_data')['nome_mae'],
                    area_ultimo_curso_superior=request.session.get('documentacao_data')['area_ultimo_curso_superior'],
                    ultimo_curso_titulacao=request.session.get('documentacao_data')['ultimo_curso_titulacao'],
                    instituicao_titulacao=request.session.get('documentacao_data')['instituicao_titulacao'],
                    data_cadastramento=date.today(),
                    banco=instance_banco
                )
                instance_documentacao.save()
            
            request.session['banco_nome'] = instance_banco.banco.codigo + ' - ' + instance_banco.banco.nome
            request.session['banco_agencia'] = instance_banco.agencia
            request.session['banco_digito_agencia'] = instance_banco.digito_verificador_agencia
            request.session['banco_conta'] = instance_banco.conta
            request.session['banco_digito_conta'] = instance_banco.digito_verificador_conta
            request.session['banco_operacao'] = instance_banco.operacao
            request.session['curso_nome'] = CM_curso.objects.filter(pk=request.session.get('curso_id')).first().nome
            request.session['tipo_curso'] = CM_curso.objects.filter(pk=request.session.get('curso_id')).first().tipo_curso.nome
            request.session['bolsa_nome'] = FI_bolsa.objects.filter(pk=request.session.get('bolsa_id')).first().nome
            request.session['data_cadastramento'] = str(date.today().day) + '/' + str(date.today().month) + '/' + str(date.today().year)
            request.session['pessoa_data']['data_nascimento'] = request.session.get('pessoa_data')['data_nascimento'][8:10] + '/' + request.session.get('pessoa_data')['data_nascimento'][5:7] + '/' + request.session.get('pessoa_data')['data_nascimento'][:4]
            request.session['pessoa_data']['cidade'] = CM_cidade.objects.filter(pk=request.session.get('pessoa_data')['cidade']).first().nome_cidade
            request.session['documentacao_data']['cidade_nascimento'] = CM_cidade.objects.filter(pk=request.session.get('documentacao_data')['cidade_nascimento']).first().nome_cidade
            request.session['documentacao_data']['data_emissao_documento'] = request.session.get('documentacao_data')['data_emissao_documento'][8:10] + '/' + request.session.get('documentacao_data')['data_emissao_documento'][5:7] + '/' + request.session.get('documentacao_data')['data_emissao_documento'][:4]
            
            return redirect('passo6', pessoa_uuid)
            
    try:
        instance_banco = instance_pessoa.cm_pessoa_documentacao.banco
        form = passo5Form(instance=instance_banco)
    except:
        form = passo5Form()
    context = {
        'form': form
    }
    return render(request, 'fichaUAB/passo5.html', context)

def passo6View(request, pessoa_uuid):
    
    pessoa = CM_pessoa.objects.get(unique_id=pessoa_uuid)
    
    current_dir = os.getcwd()

    media_dir = current_dir + '/procead/static/images'
    template_dir = current_dir + '/procead/templates/fichaUAB'
    template_path = 'index.html'
    context_path = current_dir + '/procead/context/context.json'
    
    output_path = current_dir + '/procead/static/media'
    
    try:
        with open(context_path, 'w') as jsonFile:
            jsonFile.write("{}")
            jsonFile.close()
    except OSError as e:
        print(e)

    try:
        with open(context_path, 'rb') as jsonFile:
            template_context = json.load(jsonFile)
            jsonFile.close()
    except OSError as e:
        print(e)
        
    
    for item in request.session.items():
        template_context[item[0]] = item[1]
    
    try:
        with open(context_path, 'w') as jsonFile:
            jsonFile.write(json.dumps(template_context))
            jsonFile.close()
            
    except OSError as e:
        print(e)
        
    output_filename = "fichaUAB_" + pessoa.nome.replace(' ','_') + '_' + str(pessoa.unique_id) + ".pdf"
    
    pdf = generate_pdf(template_path, template_dir, media_dir, template_context)

    print(output_path)

    with open(output_path + '/' + output_filename, 'wb') as output_file:
        output_file.write(pdf)
        output_file.close()
    
    context = {'output_filename': output_filename}
    return render(request, 'fichaUAB/passo6.html', context)