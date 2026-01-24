from django.db import models
from users.models import Grade  # Пайдаланушылар бөліміндегі Grade моделін аламыз
from django.conf import settings

class Subject(models.Model):
    name = models.CharField(max_length=100, verbose_name="Пән аты")
    is_selectable = models.BooleanField(default=True, verbose_name="Таңдау пәні ме?")

    def __str__(self):
        return self.name

class Question(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Пән")
    text = models.TextField(verbose_name="Сұрақ мәтіні")
    
    # ЕНДІ СҰРАҚ НАҚТЫ СЫНЫПҚА БАЙЛАНАДЫ (МЫСАЛЫ: 10 "Ә")
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, verbose_name="Қай сыныпқа арналған?")
    
    context_text = models.TextField(null=True, blank=True, verbose_name="Мәтін (Context)")
    is_multiple_choice = models.BooleanField(default=False, verbose_name="Көп жауапты ма?")

    def __str__(self):
        return f"[{self.grade}] - {self.text[:50]}"

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

# Тест сессиясы (Кім тапсырып жатыр?)
class TestSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    is_finished = models.BooleanField(default=False)
    score = models.IntegerField(default=0)
    
    # Таңдалған пәндерді сақтаймыз
    subjects = models.ManyToManyField(Subject)

    def __str__(self):
        return f"{self.user} - {self.start_time}"