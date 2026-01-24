from django.urls import path
from . import views
from users import views as vs

urlpatterns = [
    path('', vs.smart_login, name='login'),
    path('start/', views.start_test, name='start_test'),
    path('test/<int:session_id>/', views.test_runner, name='test_runner'),
    path('save-answer/', views.save_answer, name='save_answer'),
]