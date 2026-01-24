from django.urls import path
from .views import smart_login, profile_edit

urlpatterns = [
    path('login/', smart_login, name='login'),
    path('profile-edit/', profile_edit, name='profile_edit'),
]