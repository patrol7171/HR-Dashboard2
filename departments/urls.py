from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('attrition/<int:tabnum>', views.attrition, name='attrition'),
    path('compensation/<int:tabnum>', views.compensation, name='compensation'),
    path('demographics', views.demographics, name='demographics'),
    path('recruitment/<int:tabnum>', views.recruitment, name='recruitment'),	
    path('relations/<int:tabnum>', views.relations, name='relations'),
    path('talent/<int:tabnum>', views.talent, name='talent'),
    path('locater/<int:tabnum>', views.locater, name='locater'),
]
