from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Subject, Question, TestSession, Answer
import random

@login_required
def home(request):
    # Тек таңдау пәндерін көрсетеміз (Физика, Мат, Гео...)
    selectable_subjects = Subject.objects.filter(is_selectable=True)
    return render(request, 'home.html', {'subjects': selectable_subjects})

@login_required
def start_test(request):
    if request.method == 'POST':
        # 1. Студент таңдаған 2 бейіндік пәнді аламыз
        selected_ids = request.POST.getlist('subjects')
        if len(selected_ids) != 2:
            return render(request, 'home.html', {
                'error': 'Екі бейіндік пән таңдаңыз!', 
                'subjects': Subject.objects.filter(is_selectable=True)
            })
        
        # 2. Міндетті пәндерді қосамыз (Қаз.тарихы, Оқу сауаттылығы...)
        compulsory_subjects = Subject.objects.filter(is_selectable=False)
        selected_subjects = Subject.objects.filter(id__in=selected_ids)
        
        # 3. Сессия құру
        session = TestSession.objects.create(user=request.user)
        session.subjects.set(list(compulsory_subjects) + list(selected_subjects))
        session.save()
        
        return redirect('test_runner', session_id=session.id)
    return redirect('home')

@login_required
def test_runner(request, session_id):
    session = get_object_or_404(TestSession, id=session_id, user=request.user)
    
    # Оқушының нақты сыныбы (мысалы: 10 "Ә")
    user_grade = request.user.grade 

    all_questions = {}
    for subj in session.subjects.all():
        # Сүзгілеу: Пәні сәйкес және СЫНЫБЫ (10 "Ә") тура сәйкес келетін сұрақтар
        questions = list(Question.objects.filter(
            subject=subj, 
            grade=user_grade
        ))
        all_questions[subj] = questions
    
    return render(request, 'test_runner.html', {'all_questions': all_questions})