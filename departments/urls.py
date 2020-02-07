from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('attrition', views.attrition, name='attrition'),
    path('compensation', views.compensation, name='compensation'),
    path('demographics', views.demographics, name='demographics'),
    path('recruitment', views.recruitment, name='recruitment'),	
    path('relations', views.relations, name='relations'),
    path('talent', views.talent, name='talent'),
    path('locater', views.locater, name='locater'),
    path('policies', views.policies, name='policies'),	
]

