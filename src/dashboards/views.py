from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db import connection
from .models import Dashboard, Panel, Query
from .forms import DashboardForm
from src.datasources.models import DataSource
from src.accounts.models import Organization, Membership

def homepage(request):
    """Página inicial do Vexora"""
    if request.user.is_authenticated:
        # Pegar a primeira organização do usuário (por enquanto)
        user_orgs = Organization.objects.filter(membership__user=request.user)
        if user_orgs.exists():
            user_dashboards = Dashboard.objects.filter(
                organization=user_orgs.first()
            )[:6]
        else:
            user_dashboards = Dashboard.objects.none()
        
        return render(request, "homepage.html", {
            "user_dashboards": user_dashboards
        })
    return render(request, "homepage.html")

@login_required
def list_dashboards(request):
    """Lista todos os dashboards do usuário"""
    # Pegar a organização do usuário (simplificado por enquanto)
    user_orgs = Organization.objects.filter(membership__user=request.user)
    
    if not user_orgs.exists():
        # Criar organização padrão se não existir
        default_org = Organization.objects.create(name=f"Organização de {request.user.username}")
        Membership.objects.create(user=request.user, organization=default_org, role="admin")
        user_orgs = [default_org]
    
    dashboards = Dashboard.objects.filter(organization=user_orgs.first())
    
    return render(request, "dashboards/list.html", {
        "dashboards": dashboards,
        "current_organization": user_orgs.first()
    })

@login_required
def dashboard_create(request):
    """Cria um novo dashboard"""
    user_orgs = Organization.objects.filter(membership__user=request.user)
    
    if not user_orgs.exists():
        messages.error(request, "Você precisa pertencer a uma organização para criar dashboards.")
        return redirect('dashboards:list')
    
    if request.method == 'POST':
        form = DashboardForm(request.POST, organization=user_orgs.first())
        if form.is_valid():
            dashboard = form.save()
            messages.success(request, f'Dashboard "{dashboard.name}" criado com sucesso!')
            return redirect('dashboards:detail', slug=dashboard.slug)
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = DashboardForm(organization=user_orgs.first())
    
    return render(request, 'dashboards/create.html', {
        'form': form,
        'current_organization': user_orgs.first()
    })

@login_required
def dashboard_edit(request, slug):
    """Edita um dashboard existente"""
    dashboard = get_object_or_404(Dashboard, slug=slug)
    
    # Verificar permissão (simplificado - depois vamos implementar melhor)
    if not Organization.objects.filter(
        membership__user=request.user, 
        dashboard=dashboard
    ).exists():
        messages.error(request, "Você não tem permissão para editar este dashboard.")
        return redirect('dashboards:list')
    
    if request.method == 'POST':
        form = DashboardForm(request.POST, instance=dashboard)
        if form.is_valid():
            form.save()
            messages.success(request, f'Dashboard "{dashboard.name}" atualizado com sucesso!')
            return redirect('dashboards:detail', slug=dashboard.slug)
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = DashboardForm(instance=dashboard)
    
    return render(request, 'dashboards/edit.html', {
        'form': form,
        'dashboard': dashboard
    })

@login_required
def dashboard_delete(request, slug):
    """Exclui um dashboard"""
    dashboard = get_object_or_404(Dashboard, slug=slug)
    
    # Verificar permissão
    if not Organization.objects.filter(
        membership__user=request.user, 
        dashboard=dashboard
    ).exists():
        messages.error(request, "Você não tem permissão para excluir este dashboard.")
        return redirect('dashboards:list')
    
    if request.method == 'POST':
        dashboard_name = dashboard.name
        dashboard.delete()
        messages.success(request, f'Dashboard "{dashboard_name}" excluído com sucesso!')
        return redirect('dashboards:list')
    
    return render(request, 'dashboards/delete.html', {
        'dashboard': dashboard
    })

def detail(request, slug):
    """Visualiza um dashboard específico"""
    dashboard = get_object_or_404(Dashboard, slug=slug)
    panels = dashboard.panels.all().order_by("row", "col")
    
    return render(request, "dashboards/detail.html", {
        "dashboard": dashboard, 
        "panels": panels
    })

def panel_data(request, panel_id):
    """Retorna dados para um painel específico"""
    panel = get_object_or_404(Panel, pk=panel_id)
    query = panel.queries.first()
    
    if not query:
        return JsonResponse({"error": "No query defined for this panel"}, status=400)

    datasource = query.datasource
    
    try:
        if datasource.type == "postgres":
            return _handle_postgres_query(datasource, query.text)
        elif datasource.type == "http":
            return _handle_http_query(datasource, query.text)
        elif datasource.type == "mock":
            return _handle_mock_data()
        else:
            return JsonResponse({"error": "Unsupported datasource type"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def _handle_postgres_query(datasource, query_text):
    import psycopg2
    
    conn = psycopg2.connect(
        host=datasource.host,
        port=datasource.port,
        database=datasource.database,
        user=datasource.username,
        password=datasource.password
    )
    
    with conn.cursor() as cur:
        cur.execute(query_text)
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
    
    conn.close()
    
    return JsonResponse({
        "columns": columns,
        "rows": rows[:100]
    })

def _handle_http_query(datasource, query_text):
    return JsonResponse({"error": "HTTP datasource not yet implemented"}, status=501)

def _handle_mock_data():
    return JsonResponse({
        "columns": ["time", "value"],
        "rows": [
            ["2024-01-01", 100],
            ["2024-01-02", 150],
            ["2024-01-03", 120]
        ]
    })