from django import forms
from django.shortcuts import render
from Polo.filters import CM_poloFilter, SI_iesFilter, SI_mantenedorFilter
from Polo.forms import CM_poloForm, SI_associa_polo_iesForm
from Polo.models import CM_polo, SI_ies, SI_mantenedor

from procead.views import *

# Create your views here.
#Polo
@login_required(login_url='/accounts/login/')
def PoloView(request):
    return render(request, 'procead/polo/polo.html', {})

class CM_poloCreate(LoginRequiredMixin, CreateView):
    form_class = CM_poloForm
    template_name = 'procead/polo/cm_polo_form.html'

    def get_form(self, form_class=None):
        form = super(CM_poloCreate, self).get_form(form_class)
        form.fields['horario_funcionamento_inicio'] = forms.TimeField(widget=forms.widgets.TimeInput(attrs={'type': 'time'}))
        form.fields['horario_funcionamento_fim'] = forms.TimeField(widget=forms.widgets.TimeInput(attrs={'type': 'time'}))
        return form
    
class CM_poloUpdateView(LoginRequiredMixin, UpdateView):
    model = CM_polo
    form_class = CM_poloForm
    template_name = 'procead/polo/cm_polo_update.html'

class CM_poloListView(LoginRequiredMixin, ListView):
    model = CM_polo
    template_name = 'procead/polo/cm_polo_list.html'
    paginate_by = 15
    ordering = ['nome']
    
    def get_context_data(self, **kwargs):
        objects = CM_polo.objects.all().order_by('nome')
        filter = CM_poloFilter(self.request.GET, queryset=objects)
        
        paginator = Paginator(filter.qs, 15)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = super().get_context_data(**kwargs)
        
        context['cm_polo_filter'] = filter
        context['page_obj'] = page_obj
        return context
    
class CM_poloDeleteView(LoginRequiredMixin, DeleteView):
    model = CM_polo
    template_name = 'procead/polo/cm_polo_delete.html'
    success_url = reverse_lazy('cm_polo-list')
    
class SI_associa_polo_iesUpdate(LoginRequiredMixin, UpdateView):
    model = CM_polo
    form_class = SI_associa_polo_iesForm
    template_name = 'procead/polo/si_associa_polo_ies_update.html'
    success_url = reverse_lazy('cm_polo-list')
       
class SI_mantenedorCreate(LoginRequiredMixin, CreateView):
    model = SI_mantenedor
    template_name = 'procead/polo/si_mantenedor_form.html'
    fields = '__all__'
    
    def get_form(self, form_class=None):
        form = super(SI_mantenedorCreate, self).get_form(form_class)
        form.fields['cnpj'].widget.attrs.update({'class': 'maskedCnpj'})
        form.fields['cep'].widget.attrs.update({'class': 'maskedCep'})
        form.fields['telefone1'].widget.attrs.update({'class': 'maskedPhoneBR'})
        form.fields['telefone2'].widget.attrs.update({'class': 'maskedPhoneBR'})
        return form
        
class SI_mantenedorListView(LoginRequiredMixin, ListView):
    model = SI_mantenedor
    template_name = 'procead/polo/si_mantenedor_list.html'
    paginate_by = 15
    ordering = ['nome']
    
    def get_context_data(self, **kwargs):
        objects = SI_mantenedor.objects.all().order_by('nome')
        filter = SI_mantenedorFilter(self.request.GET, queryset=objects)
        
        paginator = Paginator(filter.qs, 15)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = super().get_context_data(**kwargs)
        
        context['si_mantenedor_filter'] = filter
        context['page_obj'] = page_obj
        return context
    
class SI_mantenedorUpdateView(LoginRequiredMixin, UpdateView):
    model = SI_mantenedor
    template_name = 'procead/polo/si_mantenedor_update.html'
    fields = '__all__'
    
class SI_mantenedorDeleteView(LoginRequiredMixin, DeleteView):
    model = SI_mantenedor
    template_name = 'procead/polo/si_mantenedor_delete.html'
    success_url = reverse_lazy('si_mantenedor-list')

class SI_iesCreate(LoginRequiredMixin, CreateView):
    model = SI_ies
    template_name = 'procead/polo/si_ies_form.html'
    fields = '__all__'
    
    def get_form(self, form_class=None):
        form = super(SI_iesCreate, self).get_form(form_class)
        form.fields['telefone1'].widget.attrs.update({'class': 'maskedPhoneBR'})
        form.fields['telefone2'].widget.attrs.update({'class': 'maskedPhoneBR'})
        return form

class SI_iesListView(LoginRequiredMixin, ListView):
    model = SI_ies
    template_name = 'procead/polo/si_ies_list.html'
    paginate_by = 15
    ordering = ['nome']
    
    def get_context_data(self, **kwargs):
        objects = SI_ies.objects.all().order_by('nome')
        filter = SI_iesFilter(self.request.GET, queryset=objects)
        
        paginator = Paginator(filter.qs, 15)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = super().get_context_data(**kwargs)
        
        context['si_ies_filter'] = filter
        context['page_obj'] = page_obj
        return context
    
class SI_iesUpdateView(LoginRequiredMixin, UpdateView):
    model = SI_ies
    template_name = 'procead/polo/si_ies_update.html'
    fields = '__all__'
    
class SI_iesDeleteView(LoginRequiredMixin, DeleteView):
    model = SI_ies
    template_name = 'procead/polo/si_ies_delete.html'
    success_url = reverse_lazy('si_ies-list')