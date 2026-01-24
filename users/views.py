# users/views.py файлының басы
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

from .models import CustomUser, Grade
# quiz қосымшасынан барлық керек модельдерді импорттаймыз:
from quiz.models import Subject, TestSession, Question
@csrf_protect
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

@csrf_protect
@login_required
def profile_edit(request):
    if request.method == 'POST':
        last_name = request.POST.get('last_name')
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name')
        grade_id = request.POST.get('grade_id')
        
        user = request.user
        user.last_name = last_name
        user.first_name = first_name
        user.middle_name = middle_name
        
        if grade_id:
            user.grade = Grade.objects.get(id=grade_id)
            user.save()
            
            # 1. Ескі сессияны тазалау
            TestSession.objects.filter(user=user, is_finished=False).delete()
            
            # 2. Жаңа сессия құру
            session = TestSession.objects.create(user=user)
            
            # 3. Пәндерді жинау (Міндетті + Бейіндік)
            compulsory = Subject.objects.filter(is_selectable=False)
            specialized = user.grade.specialized_subjects.all()
            all_selected_subjects = list(compulsory) + list(specialized)
            
            # Сессияға пәндерді қосамыз
            session.subjects.add(*all_selected_subjects)
            
            # 4. МІНЕ ОСЫ ЖЕРДЕ СҰРАҚТАРДЫ ҚОСАМЫЗ:
            for subj in all_selected_subjects:
                # Осы пәнге және осы сыныпқа арналған сұрақтарды аламыз
                questions = Question.objects.filter(subject=subj, grade=user.grade)
                # Егер сессия мен сұрақтар арасында ManyToMany байланыс болса:
                session.questions.add(*questions) 
            
            return redirect('test_runner', session_id=session.id)

    all_grades = Grade.objects.all().order_by('number', 'letter')
    return render(request, 'profile_edit.html', {'all_grades': all_grades})