from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models



class Grade(models.Model):
    number = models.IntegerField(verbose_name="Сынып саны")
    letter = models.CharField(max_length=5, verbose_name="Сынып әрпі")
    # ОСЫ ЖОЛДЫ ҚОС:
    direction = models.CharField(max_length=100, blank=True, verbose_name="Бағыты (мысалы: Физ-мат)")
    specialized_subjects = models.ManyToManyField('quiz.Subject', blank=True, verbose_name="Бейіндік пәндер")
    class Meta:
        verbose_name = "Сынып"
        verbose_name_plural = "Сыныптар"
        unique_together = ('number', 'letter')
    
    def __str__(self):
        return f"{self.number}\"{self.letter}\""

class CustomUserManager(BaseUserManager):
    def create_user(self, iin, password=None, **extra_fields):
        user = self.model(iin=iin, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, iin, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(iin, password, **extra_fields)

class CustomUser(AbstractUser):
    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name} {self.middle_name or ''}".strip()
    username = None
    iin = models.CharField(max_length=12, unique=True, verbose_name="ЖСН")
    
    # Жаңа өрістер
    last_name = models.CharField(max_length=100, verbose_name="Тегі")
    first_name = models.CharField(max_length=100, verbose_name="Аты")
    middle_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Әкесінің аты")
    
    grade = models.ForeignKey('Grade', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Сыныбы")

    USERNAME_FIELD = 'iin'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.iin})"