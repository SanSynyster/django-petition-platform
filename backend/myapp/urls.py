from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create-petition/', views.create_petition, name='create_petition'),
    path('sign-petition/', views.sign_petition, name='sign_petition'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),  # Add this
    path('close-petition/', views.close_petition, name='close_petition'),  # Add this
    path('logout/', views.logout, name='logout'),
]