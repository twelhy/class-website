from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('start/', views.start_test, name='start_test'),
    path('test/<int:session_id>/', views.test_runner, name='test_runner'),
]