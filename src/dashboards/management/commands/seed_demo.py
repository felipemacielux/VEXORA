from django.core.management.base import BaseCommand
from src.accounts.models import User, Organization, Membership
from src.datasources.models import DataSource
from src.dashboards.models import Dashboard, Panel, Query

class Command(BaseCommand):
    help = 'Cria dados de demonstração para o Vexora'

    def handle(self, *args, **options):
        # Criar organização
        org, created = Organization.objects.get_or_create(
            name="Organização Demo"
        )
        
        # Criar datasource de demonstração (Mock)
        datasource, created = DataSource.objects.get_or_create(
            organization=org,
            name="Dados Demo",
            defaults={
                'type': 'mock',
                'host': 'localhost',
                'database': 'demo'
            }
        )
        
        # Criar dashboard
        dashboard, created = Dashboard.objects.get_or_create(
            organization=org,
            slug="dashboard-demo",
            defaults={
                'name': 'Dashboard de Demonstração',
                'description': 'Dashboard de exemplo com dados mockados'
            }
        )
        
        if created:
            # Criar painéis de exemplo
            panel1 = Panel.objects.create(
                dashboard=dashboard,
                title="Métricas Principais",
                row=0,
                col=0,
                width=6,
                height=4
            )
            
            panel2 = Panel.objects.create(
                dashboard=dashboard,
                title="Tendências Temporais", 
                row=0,
                col=6,
                width=6,
                height=4
            )
            
            # Criar queries para os painéis
            Query.objects.create(
                panel=panel1,
                datasource=datasource,
                text="SELECT 'Usuários Ativos' as metric, 1542 as value UNION SELECT 'Taxa de Conversão', 3.2"
            )
            
            Query.objects.create(
                panel=panel2,
                datasource=datasource,
                text="SELECT '2024-01' as period, 100 as value UNION SELECT '2024-02', 150 UNION SELECT '2024-03', 120"
            )
            
            self.stdout.write(
                self.style.SUCCESS('✅ Dados de demonstração criados com sucesso!')
            )
            self.stdout.write(
                self.style.SUCCESS(f'📊 URL do dashboard: http://localhost:8000/dashboard-demo/')
            )
        else:
            self.stdout.write(
                self.style.WARNING('⚠️ Dados de demonstração já existem!')
            )