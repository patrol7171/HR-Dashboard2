"""hr_dashboard2 URL Configuration"""
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path, include
from departments import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.welcome, name='welcome'),
    path('home', views.home, name='home'),    
    path('about', views.about, name='about'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('accounts/', include('accounts.urls')),
	path('departments/', include('departments.urls')),
    
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)