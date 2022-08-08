from django import forms
from django.shortcuts import render
from Acesso_Restrito.models import CM_pessoa
from Viagens.filters import VI_enderecoFilter
from Viagens.forms import VI_enderecoForm, VI_osForm
from Viagens.models import VI_endereco, VI_os

from procead.views import *

# Create your views here.
#Viagens
@login_required(login_url='/accounts/login/')
def ViagemView(request):
    return render(request, 'procead/viagem/viagem.html', {})

class VI_enderecoCreate(LoginRequiredMixin, CreateView):
    model = VI_endereco
    form_class = VI_enderecoForm
    template_name = 'procead/viagem/vi_endereco_form.html'
    
    def get_success_url(self):
        return reverse('vi_endereco-list')
    
class VI_enderecoListView(LoginRequiredMixin, ListView):
    model = VI_endereco
    template_name = 'procead/viagem/vi_endereco_list.html'
    paginate_by = 15
    
    def get_context_data(self, **kwargs):
        objects = VI_endereco.objects.all().order_by('nome')
        filter = VI_enderecoFilter(self.request.GET, queryset=objects)
        
        paginator = Paginator(filter.qs, 15)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = super().get_context_data(**kwargs)
        
        context['vi_endereco_filter'] = filter
        context['page_obj'] = page_obj
        return context
    
class VI_enderecoUpdateView(LoginRequiredMixin, UpdateView):
    model = VI_endereco
    form_class = VI_enderecoForm
    template_name = 'procead/viagem/vi_endereco_update.html'
    
    def get_success_url(self):
        return reverse('vi_endereco-list')
    
class VI_enderecoDeleteView(LoginRequiredMixin, DeleteView):
    model = VI_endereco
    template_name = 'procead/viagem/vi_endereco_delete.html'
    
    def get_success_url(self):
        return reverse('vi_endereco-list')
   
@login_required(login_url='/accounts/login/')    
def VI_osCreate(request):
    if request.method == 'POST':
        form = VI_osForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data['data_ida'] < date.today():
                messages.error(request, 'A data de saída precisa ser no futuro.')
            elif form.cleaned_data['data_ida'] > form.cleaned_data['data_volta']:
                messages.error(request, 'A data de retorno não pode ser anterior à data de saída.')
            elif form.cleaned_data['data_ida'] == form.cleaned_data['data_volta'] and form.cleaned_data['horario_ida'] > form.cleaned_data['horario_volta']:
                messages.error(request, 'O horário de partida na mesma data precisa ser inferior ao de retorno.')
            else:
                updated_form = form.save(commit=False)
                updated_form.solicitante = CM_pessoa.objects.filter(cpf=request.user.username).first()
                updated_form.save()
                os = VI_os.objects.last()
                os.viajante.set(form.cleaned_data['viajante'])
                os.save()
                return redirect('vi_os-list')
    form = VI_osForm()
    context = {
        'form': form
    }
    return render(request, 'procead/viagem/vi_os_form.html', context)

@login_required(login_url='/accounts/login/')    
def VI_osUpdateView(request, os_id):
    instance = VI_os.objects.filter(pk=os_id).first()
    if request.method == 'POST':
        form = VI_osForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            updated_form = form.save(commit=False)
            updated_form.solicitante = CM_pessoa.objects.filter(cpf=request.user.username).first()
            updated_form.save()
            instance.viajante.set(form.cleaned_data['viajante'])
            instance.save()
            return redirect('vi_os-list')
    form = VI_osForm(instance=instance)
    context = {
        'form': form
    }
    return render(request, 'procead/viagem/vi_os_update.html', context)

class VI_osDeleteView(LoginRequiredMixin, DeleteView):
    model = VI_os
    template_name = 'procead/viagem/vi_os_delete.html'
    
    def get_success_url(self):
        return reverse('vi_os-list')

class VI_osPendentesListView(LoginRequiredMixin, ListView):
    model = VI_os
    template_name = 'procead/viagem/vi_os_pendentes_list.html'
    paginate_by = 15
    
    def get_queryset(self):
        return VI_os.objects.filter(status='P')
    
    def get_context_data(self, **kwargs):
        objects = VI_os.objects.filter(status='P').order_by('-id')
        
        paginator = Paginator(objects, 15)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = super().get_context_data(**kwargs)
        
        context['page_obj'] = page_obj
        return context

class VI_osAprovadosListView(LoginRequiredMixin, ListView):
    model = VI_os
    template_name = 'procead/viagem/vi_os_aprovados_list.html'
    paginate_by = 15
    
    def get_queryset(self):
        return VI_os.objects.filter(status='A')
    
    def get_context_data(self, **kwargs):
        objects = VI_os.objects.filter(status='A').order_by('-id')
        
        paginator = Paginator(objects, 15)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = super().get_context_data(**kwargs)
        
        context['page_obj'] = page_obj
        return context
    
class VI_osReprovadosListView(LoginRequiredMixin, ListView):
    model = VI_os
    template_name = 'procead/viagem/vi_os_reprovados_list.html'
    paginate_by = 15
    
    def get_queryset(self):
        return VI_os.objects.filter(status='R')
    
    def get_context_data(self, **kwargs):
        objects = VI_os.objects.filter(status='R').order_by('-id')
        
        paginator = Paginator(objects, 15)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = super().get_context_data(**kwargs)
        
        context['page_obj'] = page_obj
        return context

class VI_osAprovacao(LoginRequiredMixin, UpdateView):
    model = VI_os
    fields = ['status']
    template_name = 'procead/viagem/vi_os_aprovacao.html'
    
    def get_context_data(self, **kwargs):
        os = self.object
        
        context = super().get_context_data(**kwargs)
        context['os'] = os
        return context
    
    def get_success_url(self):
        return reverse('vi_os_pendentes-list')

@login_required(login_url='/accounts/login/')    
def VI_osListView(request):
    solicitante = CM_pessoa.objects.filter(cpf=request.user.username).first()
    os_list = VI_os.objects.filter(solicitante=solicitante).order_by('-id')
    context = {
        'os_list': os_list,
        'solicitante': solicitante
    }
    return render(request, 'procead/viagem/vi_os_list.html', context)