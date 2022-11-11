from datetime import timezone
from django import forms
from django.shortcuts import render
from Curso.filters import CM_cursoFilter, SI_curso_ofertaFilter

from Curso.forms import SI_associa_curso_oferta_poloForm, SI_curso_ofertaForm
from Curso.models import CM_curso, CM_pessoa, FI_programa, SI_associa_curso_oferta_polo, SI_curso_oferta, SI_curso_situacao, SI_tipo_curso

from procead.views import *

# Create your views here.
#Curso
@login_required(login_url='/accounts/login/')
def CursoView(request):
    return render(request, 'Curso/curso.html', {})

class CM_cursoCreate(LoginRequiredMixin, CreateView):
    model = CM_curso
    template_name = 'Curso/cm_curso_form.html'
    fields = "__all__"
    success_url = reverse_lazy('cm_curso-list')
    
    # Organiza em ordem alfabética os itens da chave estrangeira CM_curso
    def get_form(self, form_class=None):
        form = super(CM_cursoCreate, self).get_form(form_class)
        form.fields['tipo_curso'].queryset = SI_tipo_curso.objects.order_by('nome')
        form.fields['programa'].queryset = FI_programa.objects.order_by('nome')
        form.fields['curso_situacao'].queryset = SI_curso_situacao.objects.order_by('nome')
        form.fields['coordenador'].queryset = CM_pessoa.objects.order_by('nome').exclude(cpf='000.000.000-00')
        return form
    
class CM_cursoListView(LoginRequiredMixin, ListView):
    model = CM_curso
    template_name = 'Curso/cm_curso_list.html'
    paginate_by = 15
    ordering = ['nome']
    
    def get_context_data(self, **kwargs):
        # Contexto adicional para filtragem
        objects = CM_curso.objects.all().order_by('nome')
        filter = CM_cursoFilter(self.request.GET, queryset=objects)
        
        # Contexto adicional para paginação
        paginator = Paginator(filter.qs, 15)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = super().get_context_data(**kwargs)
        
        context['cm_curso_filter'] = filter
        context['page_obj'] = page_obj
        
        return context

def curso_ofertaView(request, cm_curso_id):
    """View responsável por mostrar uma listagem das vagas destinadas a cada polo, por oferta do curso em questão
    """
    # Objeto guardando as informações do curso
    curso = CM_curso.objects.filter(id=cm_curso_id)[0]
    
    # Ofertas destinadas ao cuso
    ofertas = SI_curso_oferta.objects.filter(curso=curso)
    
    # Armazena o vínculo entre as ofertas e cada polo, contendo o número de vagas destinadas a cada um
    curso_oferta_polos = []
    for oferta in ofertas:
        curso_oferta_polos.append(SI_associa_curso_oferta_polo.objects.filter(oferta=oferta))
    
    context = {
        'curso_oferta_polos': zip(curso_oferta_polos, ofertas),
        'curso': curso
    }
    return render(request, 'Curso/curso_oferta.html', context)
    
class CM_cursoDetailView(LoginRequiredMixin, DetailView):
    model = CM_curso
    
class CM_cursoUpdateView(LoginRequiredMixin, UpdateView):
    model = CM_curso
    template_name = 'Curso/cm_curso_update.html'
    fields = '__all__'
    
class CM_cursoDeleteView(LoginRequiredMixin, DeleteView):
    model = CM_curso
    template_name = 'Curso/cm_curso_delete.html'
    success_url = reverse_lazy('cm_curso-list')
    
class SI_curso_ofertaListView(LoginRequiredMixin, ListView):
    model = SI_curso_oferta
    template_name = 'Curso/si_curso_oferta_list.html'
    paginate_by = 15
    ordering = ['curso__nome']
    
    def get_context_data(self, **kwargs):
        # Contexto adicional para filtragem
        objects = SI_curso_oferta.objects.all().order_by('curso__nome')
        filter = SI_curso_ofertaFilter(self.request.GET, queryset=objects)
        
        # Contexto adicional para paginação
        paginator = Paginator(filter.qs, 15)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = super().get_context_data(**kwargs)
        
        context['si_curso_oferta_filter'] = filter
        context['page_obj'] = page_obj
        return context
    
class SI_curso_ofertaDetailView(LoginRequiredMixin, DetailView):
    model = SI_curso_oferta
    
class SI_curso_ofertaDeleteView(LoginRequiredMixin, DeleteView):
    model = SI_curso_oferta
    template_name = 'Curso/si_curso_oferta_delete.html'
    success_url = reverse_lazy('si_curso_oferta-list')


@login_required(login_url='/accounts/login/')
def SI_curso_ofertaCreate(request):
    """Função para criação de uma SI_curso_oferta e criação conjunta de um grupo de SI_associa_curso_oferta_polo's
    diretamente vinculadas a essa oferta. A função também atualiza o total de vagas de SI_curso_oferta segundo o
    somatório das vagas destinadas a cada polo.
    """
    if request.method == "POST":
        form = SI_curso_ofertaForm(request.POST)
        form_si_associa_curso_oferta_polo_factory = forms.inlineformset_factory(SI_curso_oferta, SI_associa_curso_oferta_polo, form=SI_associa_curso_oferta_poloForm)
        form_si_associa_curso_oferta_polo = form_si_associa_curso_oferta_polo_factory(request.POST)
        if form.is_valid() and form_si_associa_curso_oferta_polo.is_valid():
            if form.cleaned_data['data_inicio'] < form.cleaned_data['data_fim']:
                oferta = form.save()
                form_si_associa_curso_oferta_polo.instance = oferta
                form_si_associa_curso_oferta_polo.save()
                
                # atualiza o total de vagas em SI_curso_oferta conforme o número de vagas dos polos daquela oferta
                total_vagas = 0
                for vagas_polo in form_si_associa_curso_oferta_polo.cleaned_data:
                    total_vagas += vagas_polo['num_vagas']
                oferta.num_vagas = total_vagas
                oferta.save(update_fields=['num_vagas'])
                messages.success(request, _('Oferta criada com sucesso'))
                return redirect(reverse('si_curso_oferta-list'))
            else:
                messages.error(request, _('A data de término prevista não pode ser anterior à data de início.'))
    
    form = SI_curso_ofertaForm()
    form.fields['data_inicio'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    form.fields['data_fim'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    # cria um inlineformset_factory para associação da ofertas aos polos
    form_si_associa_curso_oferta_polo_factory = forms.inlineformset_factory(SI_curso_oferta, SI_associa_curso_oferta_polo, form=SI_associa_curso_oferta_poloForm, extra=1, max_num=5)
    form_si_associa_curso_oferta_polo = form_si_associa_curso_oferta_polo_factory()
    context = {
        'form': form,
        'form_si_associa_curso_oferta_polo': form_si_associa_curso_oferta_polo,
    }
    return render(request, 'Curso/si_curso_oferta_form.html', context)

@login_required(login_url='/accounts/login/')
def SI_curso_ofertaUpdateView(request, si_curso_oferta_id):
    """O funcionamento dessa função é semelhante ao da imediatamente anterior, porém voltada para a atualização dos
    SI_curso_ofertas já cadastrados.
    """
    if request.method == "GET":
        instancia = SI_curso_oferta.objects.filter(id=si_curso_oferta_id).first()
        if instancia is None:
            return redirect(reverse('si_curso_oferta-list'))
            
        form = SI_curso_ofertaForm(instance=instancia)
        form_si_associa_curso_oferta_polo_factory = forms.inlineformset_factory(SI_curso_oferta, SI_associa_curso_oferta_polo, form=SI_associa_curso_oferta_poloForm, extra=1, max_num=5)
        form_si_associa_curso_oferta_polo = form_si_associa_curso_oferta_polo_factory(instance=instancia)
        oferta = str(instancia.numero_oferta) + "ª/" + str(instancia.data_inicio.year) + " - " + str(instancia.curso.nome)
        context = {
            'form': form,
            'form_si_associa_curso_oferta_polo': form_si_associa_curso_oferta_polo,
            'instancia': instancia,
            'oferta': oferta
        }
        return render(request, 'Curso/si_curso_oferta_update.html', context)
    elif request.method == "POST":
        instancia = SI_curso_oferta.objects.filter(id=si_curso_oferta_id).first()
        if instancia is None:
            return redirect(reverse('si_curso_oferta-list'))
        # armazena os IDs dos antigos polos cadastrados
        unfiltered_data = []
        for data in SI_associa_curso_oferta_polo.objects.filter(oferta=instancia):
            unfiltered_data.append(data.id)
            
        form = SI_curso_ofertaForm(request.POST, instance=instancia)
        form_si_associa_curso_oferta_polo_factory = forms.inlineformset_factory(SI_curso_oferta, SI_associa_curso_oferta_polo, form=SI_associa_curso_oferta_poloForm)
        form_si_associa_curso_oferta_polo = form_si_associa_curso_oferta_polo_factory(request.POST, instance=instancia)
        if form.is_valid() and form_si_associa_curso_oferta_polo.is_valid():
            oferta = form.save()
            form_si_associa_curso_oferta_polo.instance = oferta
            form_si_associa_curso_oferta_polo.save()
            
            # armazena os IDs dos novos polos cadastrados
            filtered_data = []
            for data in form_si_associa_curso_oferta_polo.cleaned_data:
                if(data['id']):
                    filtered_data.append(data['id'].id)
                
            # remove os filhos que não estão mais presentes na oferta
            for index in unfiltered_data:
                if(index not in filtered_data):
                    vaga = SI_associa_curso_oferta_polo.objects.filter(pk=index).first()
                    vaga.delete()
            
            total_vagas = 0
            for vagas_polo in form_si_associa_curso_oferta_polo.cleaned_data:
                total_vagas += vagas_polo['num_vagas']
            oferta.num_vagas = total_vagas
            oferta.save(update_fields=['num_vagas'])
            return redirect(reverse('si_curso_oferta-list'))
        else:
            context = {
                'form': form,
                'form_si_associa_curso_oferta_polo': form_si_associa_curso_oferta_polo,
                'instancia': instancia,
            }
            return render(request, 'Curso/si_curso_oferta_update.html', context)