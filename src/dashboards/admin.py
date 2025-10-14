from django.contrib import admin
from .models import Dashboard, Panel, Query

@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'organization', 'created']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Panel)
class PanelAdmin(admin.ModelAdmin):
    list_display = ['title', 'dashboard', 'row', 'col']

@admin.register(Query)
class QueryAdmin(admin.ModelAdmin):
    list_display = ['panel', 'datasource', 'created']