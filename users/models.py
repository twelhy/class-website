from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
class Grade(models.Model):
    number = models.IntegerField(verbose_name="Сынып саны (10, 11)")
    letter = models.CharField(max_length=5, verbose_name="Сынып әрпі (А, Ә, Б...)")
    direction = models.CharField(max_length=100, blank=True, help_text="Мысалы: Физ-мат")

    class Meta:
        verbose_name = "Сынып"
        verbose_name_plural = "Сыныптар"
        unique_together = ('number', 'letter') # 10А екеу болмауы үшін

    def __str__(self):
        return f"{self.number}\"{self.letter}\" ({self.direction})"
class CustomUserManager(BaseUserManager):
    def create_user(self, iin, password=None, **extra_fields):
        if not iin:
            raise ValueError('ЖСН міндетті түрде керек')
        user = self.model(iin=iin, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, iin, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(iin, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None
    iin = models.CharField(max_length=12, unique=True, verbose_name="ЖСН")
    full_name = models.CharField(max_length=255, default="Жаңа оқушы")
    
    # ForeignKey арқылы Grade моделіне байланыстыру
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Сыныбы")

    objects = CustomUserManager()
    USERNAME_FIELD = 'iin'
    REQUIRED_FIELDS = ['full_name']
    
