from django import forms
from django.shortcuts import render
from Acesso_Restrito.filters import CM_cidadeFilter, CM_pessoaFilter, FI_programaFilter, FuncionarioFilter, GrupoFilter, PermissaoFilter, SI_curso_situacaoFilter, SI_tipo_cursoFilter, SetorFilter, UserFilter

from Acesso_Restrito.forms import CM_pessoaForm, GrupoForm, Usuario_grupoForm
from Acesso_Restrito.models import CM_cidade, CM_pessoa
from Curso.forms import CM_cidadeForm
from Curso.models import FI_programa, SI_curso_situacao, SI_tipo_curso

from django.contrib.auth.forms import UserCreationForm
from Ticket.models import Funcionario, Setor
from procead.filters import Filter

from procead.views import *

from django.core.mail import send_mail

# Create your views here.
#Acesso Restrito
@login_required(login_url='/accounts/login/')
@superuser_required()
def AdministracaoView(request):
    return render(request, 'Acesso_Restrito/administracao.html', {})

#Submenus de Administracao
@login_required(login_url='/accounts/login/')
def CadastroAdicionalView(request):
    return render(request, 'Acesso_Restrito/extra.html', {})

class GrupoCreate(SuperuserRequiredMixin, CreateView):
    login_url = '/procead/accounts/403'
    model = Group
    template_name = 'Acesso_Restrito/grupo_form.html'
    form_class = GrupoForm
    ordering = ['name']
    
    def get_success_url(self):
        return reverse('grupo-list')
    
class GrupoUpdateView(SuperuserRequiredMixin, UpdateView):
    login_url = '/procead/accounts/403'
    model = Group
    template_name = 'Acesso_Restrito/grupo_update.html'
    form_class = GrupoForm
    ordering = ['name']
    
    def get_success_url(self):
        return reverse('grupo-list')
   
class GrupoListView(SuperuserRequiredMixin, ListView):
    login_url = '/procead/accounts/403'
    model = Group
    template_name = 'Acesso_Restrito/grupo_list.html'
    paginate_by = 15
    ordering = ['name']
    
    def get_context_data(self, **kwargs):
        objects = Group.objects.all().order_by('name')
        filter = GrupoFilter(self.request.GET, queryset=objects)
        
        paginator = Paginator(filter.qs, 15)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = super().get_context_data(**kwargs)
        
        context['grupo_filter'] = filter
        context['page_obj'] = page_obj
        return context
    
class GrupoDeleteView(SuperuserRequiredMixin, DeleteView):
    login_url = '/procead/accounts/403'
    model = Group
    template_name = 'Acesso_Restrito/grupo_delete.html'
    
    def get_success_url(self):
        return reverse('grupo-list')
    
class PermissaoCreate(SuperuserRequiredMixin, CreateView):
    login_url = '/procead/accounts/403'
    model = Permission
    template_name = 'Acesso_Restrito/permissao_form.html'
    fields = '__all__'
    
    def get_success_url(self):
        return reverse('permissao-list')
    
class PermissaoListView(SuperuserRequiredMixin, ListView):
    login_url = '/procead/accounts/403'
    model = Permission
    template_name = 'Acesso_Restrito/permissao_list.html'
    paginate_by = 15
    ordering = ['name']
    
    def get_context_data(self, **kwargs):
        objects = Permission.objects.all().order_by('codename')
        filter = PermissaoFilter(self.request.GET, queryset=objects)
        
        paginator = Paginator(filter.qs, 15)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = super().get_context_data(**kwargs)
        
        context['permissao_filter'] = filter
        context['page_obj'] = page_obj
        return context
    
class PermissaoDeleteView(SuperuserRequiredMixin, DeleteView):
    login_url = '/procead/accounts/403'
    model = Permission
    template_name = 'Acesso_Restrito/permissao_delete.html'
    success_url = reverse_lazy('permissao-list')
    
    def get_success_url(self):
        return reverse('permissao-list')
    
class PermissaoUpdateView(SuperuserRequiredMixin, UpdateView):
    login_url = '/procead/accounts/403'
    model = Permission
    template_name = 'Acesso_Restrito/permissao_update.html'
    fields = '__all__'
    
    def get_success_url(self):
        return reverse('permissao-list')
    
class PermissaoListView(SuperuserRequiredMixin, ListView):
    login_url = '/procead/accounts/403'
    model = Permission
    template_name = 'Acesso_Restrito/permissao_list.html'
    paginate_by = 15
    ordering = ['name']
    
    def get_context_data(self, **kwargs):
        objects = Permission.objects.all().order_by('codename')
        filter = PermissaoFilter(self.request.GET, queryset=objects)
        
        paginator = Paginator(filter.qs, 15)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = super().get_context_data(**kwargs)
        
        context['permissao_filter'] = filter
        context['page_obj'] = page_obj
        return context
    
@login_required(login_url='/accounts/login/')
@group_required('Admin')
def UserView(request):
    pessoas = CM_pessoa.objects.all().exclude(cpf='000.000.000-00')
    filter = UserFilter(request.GET, queryset=pessoas)
    
    paginator = Paginator(filter.qs, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'user_filter': filter,
        'page_obj': page_obj,
        'pessoas': pessoas
    }
    
    return render(request, 'Acesso_Restrito/user.html', context)

@login_required(login_url='/accounts/login/')
@group_required('Admin')
def UserCreateView(request, pessoa_id):
    pessoa = CM_pessoa.objects.filter(pk=pessoa_id).first()
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = User.objects.filter(username=pessoa.cpf).first()
            user.first_name = pessoa.nome
            user.save(update_fields=['first_name'])
            pessoa.user = user
            pessoa.save(update_fields=['user'])
            messages.success(request, 'Usuário cadastrado com sucesso!')
            send_mail('Cadastro de Usuário', 'Você foi cadastrado como usuário no Sistema CEAD', 'bernard.rodrigues@uab.ufjf.br', ['bernard.rodrigues@uab.ufjf.br'], fail_silently=False)
            return redirect('user')
    else:
        form = UserCreationForm()
        form.fields['username'].widget.attrs.update({'value': str(pessoa.cpf), 'readonly': '', 'class': 'username-readonly'})
    
    form.fields['username'].widget.attrs.update({'value': str(pessoa.cpf), 'readonly': '', 'class': 'username-readonly'})
    context = {
        'form': form,
        'pessoa': pessoa
    }
    
    return render(request, 'Acesso_Restrito/user_form.html', context)

@login_required(login_url='/accounts/login/')
@group_required('Admin')
def UserUpdateView(request, pessoa_id):
    pessoa = CM_pessoa.objects.filter(pk=pessoa_id).first()
    user = User.objects.filter(username=pessoa.cpf).first()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user.set_password = form.cleaned_data.get('password2')
            user.save(update_fields=['password', 'email'])
            messages.success(request, 'Usuário atualizado com sucesso!')
            return redirect('user')
    else:
        form = UserCreationForm()
        form.fields['username'].widget.attrs.update({'value': str(pessoa.cpf), 'readonly': '', 'class': 'username-readonly'})
    
    form.fields['username'].widget.attrs.update({'value': str(pessoa.cpf), 'readonly': '', 'class': 'username-readonly'})
    context = {
        'form': form,
        'user': user
    }
    
    return render(request, 'Acesso_Restrito/user_update.html', context)

class UserDeleteView(SuperuserRequiredMixin, DeleteView):
    login_url = '/procead/accounts/403'
    model = User
    template_name = 'Acesso_Restrito/user_delete.html'
    
    def get_success_url(self):
        return reverse('user')

class Usuario_grupoView(SuperuserRequiredMixin, UpdateView):
    template_name = 'Acesso_Restrito/user_grupo.html'
    model = User
    form_class = Usuario_grupoForm
    ordering = ['name']
    
    def get_success_url(self):
        return reverse('user')

# Extra
class SI_tipo_cursoCreate(LoginRequiredMixin, CreateView):
    template_name = 'Acesso_Restrito/si_tipo_curso_form.html'
    model = SI_tipo_curso
    fields = '__all__'
    
    def get_success_url(self):
        return reverse('si_tipo_curso-list')
    
class SI_tipo_cursoListView(LoginRequiredMixin, ListView):
    template_name = 'Acesso_Restrito/si_tipo_curso_list.html'
    model = SI_tipo_curso
    paginate_by = 15
    
    def get_context_data(self, **kwargs):
        objects = SI_tipo_curso.objects.all().order_by('nome')
        filter = SI_tipo_cursoFilter(self.request.GET, queryset=objects)
        
        paginator = Paginator(filter.qs, 15)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = super().get_context_data(**kwargs)
        
        context['si_tipo_curso_filter'] = filter
        context['page_obj'] = page_obj
        return context
    
class SI_tipo_cursoUpdateView(LoginRequiredMixin, UpdateView):
    model = SI_tipo_curso
    template_name = 'Acesso_Restrito/si_tipo_curso_update.html'
    fields = '__all__'
    
    def get_success_url(self):
        return reverse('si_tipo_curso-list')

class SI_tipo_cursoDeleteView(LoginRequiredMixin, DeleteView):
    model = SI_tipo_curso
    template_name = 'Acesso_Restrito/si_tipo_curso_delete.html'
    
    def get_success_url(self):
        return reverse('si_tipo_curso-list')
    
    
class SI_curso_situacaoCreate(LoginRequiredMixin, CreateView):
    template_name = 'Acesso_Restrito/si_curso_situacao_form.html'
    model = SI_curso_situacao
    fields = '__all__'
    
    def get_success_url(self):
        return reverse('si_curso_situacao-list')
    
class SI_curso_situacaoListView(LoginRequiredMixin, ListView):
    template_name = 'Acesso_Restrito/si_curso_situacao_list.html'
    model = SI_curso_situacao
    paginate_by = 15
    
    def get_context_data(self, **kwargs):
        objects = SI_curso_situacao.objects.all().order_by('nome')
        filter = SI_curso_situacaoFilter(self.request.GET, queryset=objects)
        
        paginator = Paginator(filter.qs, 15)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = super().get_context_data(**kwargs)
        
        context['si_curso_situacao_filter'] = filter
        context['page_obj'] = page_obj
        return context
    
class SI_curso_situacaoUpdateView(LoginRequiredMixin, UpdateView):
    model = SI_curso_situacao
    template_name = 'Acesso_Restrito/si_curso_situacao_update.html'
    fields = '__all__'
    
    def get_success_url(self):
        return reverse('si_curso_situacao-list')

class SI_curso_situacaoDeleteView(LoginRequiredMixin, DeleteView):
    model = SI_curso_situacao
    template_name = 'Acesso_Restrito/si_curso_situacao_delete.html'
    
    def get_success_url(self):
        return reverse('si_curso_situacao-list')

def CM_pessoaCreate(request):
    if request.method == 'POST':
        form = CM_pessoaForm(request.POST)
        form_cidade = CM_cidadeForm(request.POST)
        if form_cidade.is_valid():
            form_cidade.save()
        elif form.is_valid():
            form.save()
        else:
            messages.error(request, form_cidade.errors.as_data())
            messages.error(request, form.errors.as_data())
    form = CM_pessoaForm()
    form.fields['data_nascimento'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    form_cidade = CM_cidadeForm()
    context = {
        'form': form,
        'form_cidade': form_cidade,
    }
    return render(request, 'Acesso_Restrito/cm_pessoa_form.html', context)

def CM_pessoaListView(request, consulta=""):
    if request.method == "POST":
        filter = Filter(request.POST)
        if filter.is_valid():
            return redirect('cm_pessoa-list', filter.cleaned_data['consulta'])
    
    filter = Filter()
    
    if consulta:
        pessoas_nome = CM_pessoa.objects.filter(nome__icontains=consulta)
        pessoas_email = CM_pessoa.objects.filter(email__icontains=consulta)
            
        pessoas = pessoas_nome
        pessoas |= pessoas_email

        pessoas = pessoas.order_by('nome')
    else:
        pessoas = CM_pessoa.objects.all().order_by('nome')
    
    paginator = Paginator(pessoas, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'cm_pessoa_list': pessoas,
        'filter': filter
    }

    return render(request, 'Acesso_Restrito/cm_pessoa_list.html', context)
    
class CM_pessoaDeleteView(SuperuserRequiredMixin, DeleteView):
    group_required = u"Admin"
    login_url = '/procead/accounts/403'
    model = CM_pessoa
    template_name = 'Acesso_Restrito/cm_pessoa_delete.html'
    success_url = reverse_lazy('cm_pessoa-list')
    
@login_required(login_url='/accounts/login/')
def CM_pessoaUpdateView(request, pessoa_id):
    instancia = CM_pessoa.objects.filter(pk=pessoa_id).first()
    
    if instancia is None:
        return redirect(reverse('cm_pessoa-list'))
    if request.method == 'GET':
        form = CM_pessoaForm(instance=instancia)
        form_cidade = CM_cidadeForm()
        context = {
            'form': form,
            'form_cidade': form_cidade,
            'instancia': instancia
        }
        return render(request, 'Acesso_Restrito/cm_pessoa_update.html', context)
    elif request.method == 'POST':
        form = CM_pessoaForm(request.POST, instance=instancia)
        form_cidade = CM_cidadeForm(request.POST)
        if form_cidade.is_valid():
            form_cidade.save()
        elif form.is_valid():
            form.save()
            usuario = User.objects.filter(username=instancia.cpf).first()
            usuario.first_name = instancia.nome
            usuario.save()
            messages.success(request, 'Pessoa atualizada com sucesso!')
            return redirect('cm_pessoa-list')
        else:
            messages.error(request, 'Erro na atualização da pessoa')
    form = CM_pessoaForm(instance=instancia)
    context = {
        'form': form,
        'instancia': instancia
    }
    return render(request, 'Acesso_Restrito/cm_pessoa_update.html', context)

class FuncionarioCreate(LoginRequiredMixin, CreateView):
    model = Funcionario
    fields = '__all__'
    template_name = 'Acesso_Restrito/funcionario_create.html'
    success_url = reverse_lazy('funcionario-list')

    def get_form(self, form_class=None):
        form = super(FuncionarioCreate, self).get_form(form_class)
        form.fields['pessoa'].queryset = CM_pessoa.objects.all().exclude(cpf="000.000.000-00").order_by('nome')
        return form

class FuncionarioListView(LoginRequiredMixin, ListView):
    model = Funcionario
    template_name = 'Acesso_Restrito/funcionario_list.html'
    paginate_by = 15

    def get_context_data(self, **kwargs):
        objects = Funcionario.objects.all().order_by('pessoa__nome')
        filter = FuncionarioFilter(self.request.GET, queryset=objects)
        
        paginator = Paginator(filter.qs, 15)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = super().get_context_data(**kwargs)
        
        context['funcionario_filter'] = filter
        context['page_obj'] = page_obj
        return context

class FuncionarioUpdateView(LoginRequiredMixin, UpdateView):
    model = Funcionario
    fields = '__all__'
    template_name = 'Acesso_Restrito/funcionario_update.html'
    success_url = reverse_lazy('funcionario-list')

class FuncionarioDeleteView(LoginRequiredMixin, DeleteView):
    model = Funcionario
    template_name = 'Acesso_Restrito/funcionario_delete.html'
    success_url = reverse_lazy('funcionario-list')

class CM_cidadeCreate(LoginRequiredMixin, CreateView):
    template_name = 'Acesso_Restrito/cm_cidade_form.html'
    form_class = CM_cidadeForm
    
    def get_success_url(self):
        return reverse('cm_cidade-list')
    
class CM_cidadeListView(LoginRequiredMixin, ListView):
    template_name = 'Acesso_Restrito/cm_cidade_list.html'
    model = CM_cidade
    paginate_by = 15
    
    def get_context_data(self, **kwargs):
        objects = CM_cidade.objects.all().order_by('nome_cidade')
        filter = CM_cidadeFilter(self.request.GET, queryset=objects)
        
        paginator = Paginator(filter.qs, 15)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = super().get_context_data(**kwargs)
        
        context['cm_cidade_filter'] = filter
        context['page_obj'] = page_obj
        return context
    
class CM_cidadeUpdateView(LoginRequiredMixin, UpdateView):
    model = CM_cidade
    template_name = 'Acesso_Restrito/cm_cidade_update.html'
    fields = '__all__'
    
    def get_success_url(self):
        return reverse('cm_cidade-list')

class CM_cidadeDeleteView(LoginRequiredMixin, DeleteView):
    model = CM_cidade
    template_name = 'Acesso_Restrito/cm_cidade_delete.html'
    
    def get_success_url(self):
        return reverse('cm_cidade-list')
   
class FI_programaCreate(LoginRequiredMixin, CreateView):
    template_name = 'Acesso_Restrito/fi_programa_form.html'
    model = FI_programa
    fields = '__all__'
    
    def get_success_url(self):
        return reverse('fi_programa-list')
    
class FI_programaListView(LoginRequiredMixin, ListView):
    template_name = 'Acesso_Restrito/fi_programa_list.html'
    model = FI_programa
    paginate_by = 15
    
    def get_context_data(self, **kwargs):
        objects = FI_programa.objects.all().order_by('nome')
        filter = FI_programaFilter(self.request.GET, queryset=objects)
        
        paginator = Paginator(filter.qs, 15)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = super().get_context_data(**kwargs)
        
        context['fi_programa_filter'] = filter
        context['page_obj'] = page_obj
        return context
    
class FI_programaUpdateView(LoginRequiredMixin, UpdateView):
    model = FI_programa
    template_name = 'Acesso_Restrito/fi_programa_update.html'
    fields = '__all__'
    
    def get_success_url(self):
        return reverse('fi_programa-list')

class FI_programaDeleteView(LoginRequiredMixin, DeleteView):
    model = FI_programa
    template_name = 'Acesso_Restrito/fi_programa_delete.html'
    
    def get_success_url(self):
        return reverse('fi_programa-list')

class SetorCreate(LoginRequiredMixin, CreateView):
    model = Setor
    template_name = 'Acesso_Restrito/setor_form.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('setor-list')

class SetorUpdateView(LoginRequiredMixin, UpdateView):
    model = Setor
    template_name = 'Acesso_Restrito/setor_update.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('setor-list')

class SetorDeleteView(LoginRequiredMixin, DeleteView):
    model = Setor
    template_name = 'Acesso_Restrito/setor_delete.html'

    def get_success_url(self):
        return reverse('setor-list')

class SetorListView(LoginRequiredMixin, ListView):
    model = Setor
    template_name = 'Acesso_Restrito/setor_list.html'
    paginate_by = 15
    
    def get_context_data(self, **kwargs):
        objects = Setor.objects.all().order_by('nome_setor')
        filter = SetorFilter(self.request.GET, queryset=objects)
        
        paginator = Paginator(filter.qs, 15)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = super().get_context_data(**kwargs)
        
        context['setor_filter'] = filter
        context['page_obj'] = page_obj
        return context