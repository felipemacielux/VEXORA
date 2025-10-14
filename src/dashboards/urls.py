from django.urls import path
from . import views

app_name = 'dashboards'

urlpatterns = [
    path("", views.list_dashboards, name="list"),  
    path("create/", views.dashboard_create, name="create"),
    path("<slug:slug>/", views.detail, name="detail"),
    path("<slug:slug>/edit/", views.dashboard_edit, name="edit"),
    path("<slug:slug>/delete/", views.dashboard_delete, name="delete"),
    path("panel/<int:panel_id>/data/", views.panel_data, name="panel_data"),
]