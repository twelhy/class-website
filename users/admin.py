from django.contrib import admin
from .models import CustomUser, Grade

# 1. Сыныптарды басқару (10А, 11Ә т.б.)
@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    # Админка тізімінде көрінетін бағандар
    list_display = ('number', 'letter', 'direction')
    # Оң жақтан сүзу (фильтр)
    list_filter = ('number',)
    # Іздеу мүмкіндігі
    search_fields = ('number', 'letter', 'direction')

# 2. Пайдаланушыларды (Оқушыларды) басқару
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    # ЖСН, Аты-жөні және Сыныбы көрініп тұрады
    list_display = ('iin', 'full_name', 'get_grade_display', 'is_staff')
    search_fields = ('iin', 'full_name')
    list_filter = ('grade__number', 'grade__letter')

    # Сыныпты әдемілеп көрсету үшін функция
    def get_grade_display(self, obj):
        if obj.grade:
            return f"{obj.grade.number}\"{obj.grade.letter}\""
        return "Тағайындалмаған"
    
    get_grade_display.short_description = 'Сыныбы'