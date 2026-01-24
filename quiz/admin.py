from django.contrib import admin
from .models import Subject, Question, Answer, TestSession
from .models import StudentAnswer

@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ('session', 'question', 'selected_answer')
    list_filter = ('session', 'question__subject')

# Сұрақтың астында бірден жауаптарды жазу үшін
class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4  # Әдепкі бойынша 4 жауап ұяшығын шығарады

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    # Енді тізімде 10 "Ә" немесе 11 "А" деп нақты көрінеді
    list_display = ('text', 'subject', 'grade', 'is_multiple_choice')
    list_filter = ('grade', 'subject') # Сыныптар бойынша сүзу
    inlines = [AnswerInline]

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_selectable')

admin.site.register(TestSession)