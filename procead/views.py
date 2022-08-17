import os
from django.http import FileResponse

from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test

# Imports para as demais views
from braces.views import GroupRequiredMixin, SuperuserRequiredMixin

from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from django.core.paginator import Paginator

from django.urls import reverse_lazy

from procead.models import *

from django.core.mail import send_mail


def group_required(*group_names):
    """Decorator utilizado para exigir que o usuário seja membro de um dos grupos descritos em group_names
    """    
    def in_groups(user):
        if user.is_authenticated:
            if bool(user.groups.filter(name__in=group_names)) | user.is_superuser:
                return True
        return False
    
    return user_passes_test(in_groups, login_url='/procead/accounts/403')

def superuser_required():
    """Decorator utilizado para exigir que o usuário seja superuser
    """    
    def in_groups(user):
        if user.is_authenticated:
            if user.is_superuser:
                return True
        return False
    
    return user_passes_test(in_groups, login_url='/procead/accounts/403')

@login_required(login_url='/accounts/login/')
def DeniedView(request):
    return render(request, '403.html')

@login_required(login_url='/accounts/login/')
def index(request):
    # try:
    #     send_mail('Hello World', 'Você entrou no site do CEAD', 'no-reply@uab.ufjf.br', ['bernard.rodrigues@uab.ufjf.br'], fail_silently=False)
    # except:
    #     print('deu bosta')
    # finally:
        return render(request, 'index.html')

# Função para mudança de senha
@login_required(login_url='/accounts/login/')
def alterar_senha(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Sua senha foi alterada com sucesso!')
            return redirect('password_reset_complete')
        else:
            messages.error(request, 'Falha na atualização.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'procead/administracao/alterar_senha.html', {
        'form': form
    })

@login_required(login_url='/accounts/login/')
def UserUpdateView(request, user_id):
    user = User.objects.filter(pk=user_id).first()
    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return redirect('password_reset_complete')
        else:
            messages.error(request, 'Falha na atualização.')
    else:
        form = PasswordChangeForm(user)
    return render(request, 'procead/administracao/alterar_senha.html', {
        'form': form
    })

#####################################################
# UTILS #
#####################################################

def show_pdf(request, file_name):
    
    current_dir = os.getcwd()

    filepath = os.path.join(current_dir + '/procead/static', 'media/' + file_name)
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')