from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.order_list, name='list'),
    path('new/', views.order_create, name='create'),
    path('mine/', views.my_orders, name='mine'),
    path('<int:pk>/', views.order_detail, name='detail'),
    path('<int:pk>/respond/', views.order_respond, name='respond'),
    path('<int:pk>/close/', views.order_close, name='close'),
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/read/', views.notifications_read, name='notifications_read'),
    path('notifications/<int:pk>/read/', views.notification_read, name='notification_read'),
]
