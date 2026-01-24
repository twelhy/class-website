from django.db import models
  # Пайдаланушылар бөліміндегі Grade моделін аламыз
from django.conf import settings

class Subject(models.Model):
    name = models.CharField(max_length=100, verbose_name="Пән аты")
    is_selectable = models.BooleanField(default=True, verbose_name="Таңдау пәні ме?")

    def __str__(self):
        return self.name

# quiz/models.py

class Question(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Пән")
    text = models.TextField(verbose_name="Сұрақ мәтіні")
    
    # Grade-ті импорттамай, мәтін ретінде жазамыз:
    grade = models.ForeignKey('users.Grade', on_delete=models.CASCADE, verbose_name="Қай сыныпқа арналған?")
    
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
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    subjects = models.ManyToManyField(Subject)
    # Сұрақтарды сақтау үшін осы жол міндетті:
    questions = models.ManyToManyField(Question, blank=True) 
    is_finished = models.BooleanField(default=False)
    # ...

    def __str__(self):
        return f"Сессия: {self.user.full_name} - {self.user.iin}"

class StudentAnswer(models.Model):
    session = models.ForeignKey(TestSession, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('session', 'question') # Бір сұраққа бір-ақ жауап сақталуы үшін