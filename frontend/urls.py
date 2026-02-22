# from django.urls import path
# from .views import (
#     dashboard_stats, financial_summary, spending_analysis
# )

# urlpatterns = [
   
#     path('dashboard-stats/', dashboard_stats, name='dashboard_stats'),
#     path('financial-summary/', financial_summary, name='financial_summary'),
#     path('spending-analysis/', spending_analysis, name='spending_analysis'),
    
# ]
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Authentication Pages
    path('login/', auth_views.LoginView.as_view(template_name='frontend/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup_view, name='signup'),
    
    # Homepage
    path('', views.homepage, name='homepage'),
    
    # Dashboard & Analytics (your existing views)
    path('dashboard-stats/', views.dashboard_stats, name='dashboard_stats'),
    path('financial-summary/', views.financial_summary, name='financial_summary'),
    path('spending-analysis/', views.spending_analysis, name='spending_analysis'),
    
    # Feature Pages
    path('dashboard/', views.dashboard_stats, name='dashboard'),
    path('group-expenses/', views.group_expenses_view, name='group_expenses'),
    path('budget/', views.budget_view, name='budget'),
    path('goals/', views.goals_view, name='goals'),
    path('transactions/', views.transactions_view, name='transactions'),
]