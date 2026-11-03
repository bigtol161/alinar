from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'news'

urlpatterns = [
    path('', views.home, name='home'),
    path('news/', views.article_list, name='article_list'),
    path('news/stats/', views.stats, name='stats'),
    path('news/masters/', views.executor_list, name='executor_list'),
    path('news/masters/<slug:slug>/', views.executor_detail, name='executor_detail'),
    path('news/masters/<slug:slug>/edit/', views.executor_edit, name='executor_edit'),
    path('news/my-leads/', views.my_leads, name='my_leads'),
    path('news/executor-leads/', views.executor_leads, name='executor_leads'),
    path('news/lead/<int:pk>/done/', views.lead_done, name='lead_done'),
    path('news/register/', views.register, name='register'),
    path('news/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('news/<slug:slug>/', views.article_detail, name='article_detail'),
]
