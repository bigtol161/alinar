
from django.urls import path
from . import views

urlpatterns = [
    path('test-log/', views.test_log_view, name='test-log'),
]

