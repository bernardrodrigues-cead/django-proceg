import datetime
#from multiprocessing        import context
#from pickle import TRUE
from django                 import forms
from django.shortcuts       import render
from django.utils           import timezone
from Almoxarifado.models    import Categoria, Entrada_Produto, Estoque, Produto, Saida_Produto
from procead.views          import *
from Almoxarifado.forms     import CategoriaForm, DataIntervalo, EntradaForm, SaidaForm, ProdutoForm, TesteForm
from procead.filters        import Filter
# Create your views here.

#Almoxarifado

@login_required(login_url='/accounts/login/')
def AlmoxarifadoView(request):
    return render(request, 'Almoxarifado/almoxarifado.html', {})

@login_required(login_url='/accounts/login/')
def AlmoxarifadoNovoView(request):
    return render(request, 'Almoxarifado/almoxarifado_novo.html', {})

@login_required(login_url='/accounts/login/')
def AlmoxarifadoListarView(request):
    return render(request, 'Almoxarifado/almoxarifado_listar.html', {})

@login_required(login_url='/accounts/login/')
def AlmoxarifadoRelatorioView(request):
    return render(request, 'Almoxarifado/almoxarifado_relatorio.html', {})


#Submenus de Almoxarifado


@login_required(login_url='/accounts/login/')
def CategoriaListView(request, consulta=""): 
    
    if request.method == 'POST':
        filter = Filter(request.POST)

        if filter.is_valid():
            return redirect('list_categorias', filter.cleaned_data['consulta'] )    
    filter = Filter() 

    if consulta :
        lista_categorias  = Categoria.objects.filter(descricao__icontains=consulta).order_by('descricao')
    
    else:
        # cria lista de Entrada de Produtos ordenadas por data de entrada e salva na variavel
        lista_categorias = Categoria.objects.all().order_by('descricao')

    paginator = Paginator(lista_categorias, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # cria dicionario contendo a lsita de objetos e salva em context
    context = {'lista_categorias' : lista_categorias,
                'page_obj'        : page_obj , 
                'filter'          : filter }                   

    return render(request, 'Almoxarifado/categoria_list.html', context)

@login_required(login_url='/accounts/login/')
def CategoriaCreate(request): 
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        
        if form.is_valid(): 
            form.save()
            
            messages.success(request, "Categoria criada com sucesso!")

            return redirect('list_categorias')
        else:
            messages.error(request, "Descrição inválida")

    # Se  método for GET ou se o form for inválido
    form = CategoriaForm()
    context = {
        'form': form,
        }

    return render(request, 'Almoxarifado/categoria_create.html', context)

@login_required(login_url='/accounts/login/')
def CategoriaUpdate(request, categoria_id): 
    
    categoria = Categoria.objects.get(id=categoria_id)
    
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        
        if form.is_valid(): 
            form.save()
            
            messages.success(request, "Categoria editada com sucesso!")

            return redirect('list_categorias')
        else:
            messages.error(request, "Descrição inválida")

    # Se  método for GET ou se o form for inválido
    form = CategoriaForm(instance=categoria)
    context = {
        'form': form,
        }

    return render(request, 'Almoxarifado/categoria_update.html', context)

@login_required(login_url='/accounts/login/')
def CategoriaDelete(request, categoria_id): 
    
    categoria = Categoria.objects.get(id=categoria_id)

    if request.method == 'POST':
        categoria.delete()
        messages.success(request, "Categoria excluída com sucesso!")
 
        return redirect('list_categorias')

    context = {'categoria' : categoria }
    
    return render(request, 'Almoxarifado/categoria_delete.html' ,context)
    
@login_required(login_url='/accounts/login/')
def ProdutoUpdate(request, codigo_siga): 
    
    produto = Produto.objects.get(codigo_siga=codigo_siga)
    
    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        
        if form.is_valid(): 
            form.save()
            
            messages.success(request, "Produto editado com sucesso!")

            return redirect('list_produtos')
        else:
            messages.error(request, "Descrição inválida")

    # Se  método for GET ou se o form for inválido
    form = ProdutoForm(instance=produto)
    context = {
        'form': form,
        }

    return render(request, 'Almoxarifado/produto_update.html', context)



@login_required(login_url='/accounts/login/')
def ProdutoListView(request, consulta=""): 
    if request.method == 'POST':
        filter = Filter(request.POST)

        if filter.is_valid():
            return redirect('list_produtos', filter.cleaned_data['consulta'] )    
    filter = Filter() 

    if consulta :
        lista_produtos  = Produto.objects.filter(descricao__icontains=consulta).order_by('descricao')
        lista_produtos |= Produto.objects.filter(categoria__descricao__icontains=consulta).order_by('categoria__descricao')
    
    else:
        # cria lista de Entrada de Produtos ordenadas por data de entrada e salva na variavel
        lista_produtos = Produto.objects.all().order_by('descricao')
    

    paginator = Paginator(lista_produtos, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # cria dicionario contendo a lsita de objetos e salva em context
    context = {'lista_produtos': lista_produtos,
                'page_obj'     : page_obj,
                'filter'       : filter                 }               

    return render(request, 'Almoxarifado/produto_list.html', context)

@login_required(login_url='/accounts/login/')
def ProdutoCreate(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Produto criado com sucesso!") 

            return redirect('list_produtos')
        else:
            messages.error(request, "Produto inválido")   

# Se o metodo for GET ou se o form for invalido  
    form = ProdutoForm()
    context = {
        'form': form,
        }

    return render(request, 'Almoxarifado/produto_create.html', context)           

@login_required(login_url='/accounts/login/')
def ProdutoDelete(request, produto_id): 
    
    produto = Produto.objects.get(id=produto_id)

    if request.method == 'POST':
        produto.delete()
        messages.success(request, "Produto excluído com sucesso!")
 
        return redirect('list_produtos')

    context = {'produto' : produto }
    
    return render(request, 'Almoxarifado/produto_delete.html' ,context)
   

@login_required(login_url='/accounts/login/')
def EntradaListView(request, consulta="", data="") : 

    if request.method == 'POST':
        # formulário de busca por texto preenchido
        filter = Filter(request.POST)

        # formulario de busca por data preenchido
        form_data = DataIntervalo(request.POST)

        # verifica se o formulario de texto está preenchido
        if (filter.is_valid()) and (filter.cleaned_data['consulta'] !=""):

            # faz o redirecionamento para a pagina lsit_entradas com o campo consulta preenchido
            return redirect('list_entradas', consulta=filter.cleaned_data['consulta'] )    
    
        elif form_data.is_valid() and filter.cleaned_data['consulta'] =="" :
            print('farofa')
            data_inicio = form_data.cleaned_data['data_inicio'].strftime("%Y-%m-%d")
            data_fim = form_data.cleaned_data['data_fim'].strftime("%Y-%m-%d")
            
            return redirect('list_entradas', data=data_inicio+'-'+data_fim)

        else :
            print(form_data.errors.as_data())
        
    filter = Filter() 
    form_data = DataIntervalo()
       
    if data and consulta =="":
        intervalo = [data[:10], (data[11:]+" 23:59:59")]
        
        lista_entrada = Entrada_Produto.objects.filter(data_entrada__range=intervalo).order_by('-data_entrada')
        print(lista_entrada)

    elif consulta and data=="" :
        lista_entrada  = Entrada_Produto.objects.filter(produto__descricao__icontains=consulta).order_by('-data_entrada')
        lista_entrada |= Entrada_Produto.objects.filter(produto__categoria__descricao__icontains=consulta).order_by('-data_entrada')
    
    else:
        # cria lista de Entrada de Produtos ordenadas por data de entrada e salva na variavel
        lista_entrada = Entrada_Produto.objects.all().order_by('-data_entrada')


    paginator = Paginator(lista_entrada, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # cria dicionario contendo a lsita de objetos e salva em context
    context = {'lista_entrada_produtos': lista_entrada,
                'page_obj'             : page_obj,
                'filter'               : filter ,        
                'form'                 : form_data, 
                                                     }

    return render(request, 'Almoxarifado/entrada_produtos_list.html', context)

@login_required(login_url='/accounts/login/')
def SaidaListView(request, consulta=""): 
    
    if request.method == 'POST':
        filter = Filter(request.POST)

        if filter.is_valid():
            return redirect('list_saidas', filter.cleaned_data['consulta'])  


    filter = Filter() 
      

    if consulta :
        lista_saida  = Saida_Produto.objects.filter(produto__descricao__icontains=consulta).order_by('-data_saida')
        lista_saida |= Saida_Produto.objects.filter(produto__categoria__descricao__icontains=consulta).order_by('-data_saida')
    
    else:
        # cria lista de Entrada de Produtos ordenadas por data de entrada e salva na variavel
        lista_saida = Saida_Produto.objects.all().order_by('-data_saida')

    paginator = Paginator(lista_saida, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # cria dicionario contendo a lsita de objetos e salva em context
    context = {'lista_saida'         : lista_saida,
                'page_obj'           : page_obj,
                'filter'             : filter                        }

    return render(request, 'Almoxarifado/saida_produtos_list.html', context)

@login_required(login_url='/accounts/login/')
def EntradaCreate(request):

    # se request for post (form preenchido)
    if request.method == 'POST':

        #var form recebe valores do formulario
        form = EntradaForm(request.POST)
        
        # se o form passar pelas verificações
        if form.is_valid():

            #  pesquisa na na table estoque filtrando (Estoque.objects.filter) 
            #  se existe o produto procurado pelo user no formulario (form.cleaned_data['produto']) 
            if Estoque.objects.filter(produto = form.cleaned_data['produto']):

                # se o produto existir no estoque, var estoque_updated recebe o formulario
                # como um resultado da pesquisa acima
                estoque_updated = Estoque.objects.filter(produto = form.cleaned_data['produto']).first()
                # e sua quantidade em estoque é somada à quantidade digitada pelo usuário no formulario
                estoque_updated.quantidade_estoque += form.cleaned_data['quantidade_entrada']

            else:
                estoque_updated = Estoque(
                    produto = form.cleaned_data['produto'], 
                    quantidade_estoque = form.cleaned_data['quantidade_entrada']
                )   

            estoque_updated.save() # a variável do formulario é atualizada com o nome do produto
            # e a nova quantidade do estoque (se houver registros, se nao houver, apenas salva )

            # form é salvo em uma variável sem aplicar suas alteraçoẽs (commit=False)
            form_updated = form.save(commit=False)

            # form é atualizado com campo data entrada recebe o valor da data e hora de agora
            form_updated.data_entrada = datetime.datetime.now()

            # form é salvo e commitado
            form_updated.save()

            messages.success(request, "Entrada de produto criada com sucesso!") 

            return redirect('list_entradas')
        else:
            messages.error(request, "Entrada inválida")   

# Se o metodo for GET ou se o form for invalido  
    form = EntradaForm()

    form.fields['origem'] = forms.CharField(min_length = 3)

    context = {
        'form': form,
        }

    return render(request, 'Almoxarifado/entrada_create.html', context)         

@login_required(login_url='/accounts/login/')
def SaidaCreate(request):

    # se request for post (form preenchido)
    if request.method == 'POST':

        #var form recebe valores do formulario
        form = SaidaForm(request.POST)
        
        # se o form passar pelas verificações
        if form.is_valid():

            #  pesquisa na na table estoque filtrando (Estoque.objects.filter) 
            #  se existe o produto procurado pelo user no formulario (form.cleaned_data['produto']) 
            if Estoque.objects.filter(produto = form.cleaned_data['produto']):

                # se o produto existir no estoque, var estoque_updated recebe o formulario
                # como um resultado da pesquisa acima
                estoque_updated = Estoque.objects.get(produto = form.cleaned_data['produto'])
                
                produto = Produto.objects.get(pk = form.cleaned_data['produto'].codigo_siga )
        
                #verifica se a quantidade em estoque do produto está abaixo da quantidade minima e exibe um alerta ao usuario, tbm exibe o alerta se o estoque FICARÁ abaixo da quantidade minima apos a saida
                if(estoque_updated.quantidade_estoque > (estoque_updated.quantidade_estoque - form.cleaned_data['quantidade_saida']) and (estoque_updated.quantidade_estoque < produto.quantidade_minima) or (produto.quantidade_minima > (estoque_updated.quantidade_estoque - form.cleaned_data['quantidade_saida'])) ) : 
                    messages.warning(request, "Atenção: Produto abaixo da quantidade minima!") 

                if(estoque_updated.quantidade_estoque > 0 and ((estoque_updated.quantidade_estoque - form.cleaned_data['quantidade_saida'])>=0) ) :
                    estoque_updated.quantidade_estoque -= form.cleaned_data['quantidade_saida'] 
                    
                else :
                    messages.error(request, "Estoque insuficiente!") 
                    return redirect('list_saidas')

            else:
                messages.error(request, "Produto não encontrado!")  


            estoque_updated.save() # a variável do formulario é atualizada com o nome do produto
            # e a nova quantidade do estoque (se houver registros, se nao houver, apenas salva )

            # form é salvo em uma variável sem aplicar suas alteraçoẽs (commit=False)
            form_updated = form.save(commit=False)

            # form é atualizado com campo data entrada recebe o valor da data e hora de agora
            form_updated.data_saida = datetime.datetime.now()

            # form é salvo e commitado
            form_updated.save()

            messages.success(request, "Saida de produto criada com sucesso!") 

            return redirect('list_saidas')
        else:
            messages.error(request, "Saída inválida")   

# Se o metodo for GET ou se o form for invalido  
    form = SaidaForm()
    context = {
        'form': form, 
        }

    return render(request, 'Almoxarifado/saida_create.html', context)           
  

@login_required(login_url='/accounts/login/')
def EstoqueListView(request, consulta=""): 
    if request.method == 'POST':
        filter = Filter(request.POST)

        if filter.is_valid():
            return redirect('estoque', filter.cleaned_data['consulta'] )    
    filter = Filter() 

    if consulta:
        lista_estoque  = Estoque.objects.filter(produto__descricao__icontains=consulta).order_by('produto__descricao').exclude(quantidade_estoque=0)
        lista_estoque |= Estoque.objects.filter(produto__categoria__descricao__icontains=consulta).order_by('produto__categoria__descricao').exclude(quantidade_estoque=0)
 
    else:
        # cria lista de Entrada de Produtos ordenadas por data de entrada e salva na variavel
        lista_estoque = Estoque.objects.all().order_by('produto__descricao').exclude(quantidade_estoque=0)

    paginator = Paginator(lista_estoque, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # cria dicionario contendo a lsita de objetos e salva em context
    context = {'lista_estoque'         : lista_estoque,
                'page_obj'             : page_obj, 
                'filter'               : filter,                    }

    return render(request, 'Almoxarifado/estoque_list.html', context)

@login_required(login_url='/accounts/login/')
def ProdutoFaltanteListView(request): 

    lista_produtos_faltantes = []

    for estoque in Estoque.objects.all():
        if estoque.quantidade_estoque < estoque.produto.quantidade_minima :
            lista_produtos_faltantes.append(estoque.produto)

    paginator = Paginator(lista_produtos_faltantes, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
            
    # cria dicionario contendo a lsita de objetos e salva em context
    context = {'lista_produtos_faltantes': lista_produtos_faltantes,
                'page_obj'             : page_obj                }

    return render(request, 'Almoxarifado/produto_faltante_list.html', context)    

@login_required(login_url='/accounts/login/')
def ProdutoAcabaramListView(request): 

    lista_produtos_acabaram = []

    for estoque in Estoque.objects.all():
        if estoque.quantidade_estoque == 0 :
            lista_produtos_acabaram.append(estoque.produto)

    paginator = Paginator(lista_produtos_acabaram, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
            
    # cria dicionario contendo a lsita de objetos e salva em context
    context = {'lista_produtos_faltantes': lista_produtos_acabaram,
                'page_obj'             : page_obj                }

    return render(request, 'Almoxarifado/produtos_acabaram_list.html', context)    
