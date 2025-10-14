from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from src.dashboards.models import Dashboard

def homepage(request):
    """Página inicial do Vexora"""
    if request.user.is_authenticated:
        user_dashboards = Dashboard.objects.filter(
            organization__membership__user=request.user
        )[:6]
        return render(request, "homepage.html", {
            "user_dashboards": user_dashboards
        })
    return render(request, "homepage.html")

def custom_login(request):
    """Página de login customizada"""
    if request.user.is_authenticated:
        return redirect('homepage')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bem-vindo de volta, {username}!')
                
                # Redirecionar para a página que tentava acessar ou homepage
                next_page = request.GET.get('next', 'homepage')
                return redirect(next_page)
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})

def custom_logout(request):
    """Logout customizado"""
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Você saiu da sua conta.')
    return redirect('homepage')

def register(request):
    """Página de registro de novos usuários"""
    if request.user.is_authenticated:
        return redirect('homepage')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Fazer login automático após registro
            login(request, user)
            messages.success(request, f'Conta criada com sucesso! Bem-vindo, {user.username}!')
            return redirect('homepage')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    """Página de perfil do usuário"""
    return render(request, 'accounts/profile.html', {'user': request.user})