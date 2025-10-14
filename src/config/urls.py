from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from src.dashboards import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("dashboards/", include("src.dashboards.urls")), 
    path("", views.homepage, name="homepage"),  
    path("accounts/", include("src.accounts.urls")),  
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)