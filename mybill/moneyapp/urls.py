from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('category/', views.category, name='category'),
    path('expenses/', views.expenses, name='expenses'),
    path('stats/', views.stats, name='stats'),
    path('login/', views.login_usr, name='login_usr'),
    path('register/', views.register_usr, name='register_usr'),
]