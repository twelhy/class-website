from django.shortcuts import render, redirect
from django.contrib.auth import login
from .models import CustomUser

def smart_login(request):
    if request.method == 'POST':
        iin = request.POST.get('iin')
        
        # Пайдаланушыны табамыз немесе жаңадан құрамыз
        user, created = CustomUser.objects.get_or_create(iin=iin)
        
        if created:
            user.set_password(iin)
            user.save()
            
        # Жүйеге кіргіземіз
        login(request, user)
        
        # МІНЕ ОСЫ ЖЕРДЕ: Профиль редактор бетіне бағыттаймыз
        return redirect('profile_edit') 

    return render(request, 'login.html')

def profile_edit(request):
    if request.method == 'POST':
        # ... (мәліметтерді сақтау коды) ...
        request.user.full_name = request.POST.get('full_name')
        request.user.save()
        
        # Сақтап болған соң, тест таңдайтын басты бетке жіберу
        return redirect('home') 

    return render(request, 'profile_edit.html')