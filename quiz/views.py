from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Subject, Question, TestSession, Answer
import random

@login_required
def home(request):
    # Тек таңдау пәндерін көрсетеміз (Физика, Мат, Гео...)
    selectable_subjects = Subject.objects.filter(is_selectable=True)
    return render(request, 'login.html', {'subjects': selectable_subjects})

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
    
    # Сұрақтарды пән бойынша топтау
    subjects_data = []
    for subject in session.subjects.all():
        questions = session.questions.filter(subject=subject)
        subjects_data.append({
            'subject': subject,
            'questions': questions
        })

    # Оқушының бұрын белгілеген жауаптары (reload болғанда сақталу үшін)
    from .models import StudentAnswer
    student_answers = StudentAnswer.objects.filter(session=session).values_list('question_id', 'selected_answer_id')
    ans_dict = dict(student_answers)

    return render(request, 'test_runner.html', {
        'session': session,
        'subjects_data': subjects_data,
        'ans_dict': ans_dict
    })

import json
from django.http import JsonResponse
from .models import StudentAnswer, Question, Answer, TestSession

def save_answer(request):
    if request.method == "POST":
        data = json.loads(request.body)
        session_id = data.get('session_id')
        question_id = data.get('question_id')
        answer_id = data.get('answer_id')

        session = TestSession.objects.get(id=session_id)
        question = Question.objects.get(id=question_id)
        answer = Answer.objects.get(id=answer_id)

        # Егер бұл сұраққа бұрын жауап берілсе - жаңартамыз, берілмесе - құрамыз
        student_ans, created = StudentAnswer.objects.update_or_create(
            session=session, 
            question=question,
            defaults={'selected_answer': answer}
        )

        return JsonResponse({"status": "success"})