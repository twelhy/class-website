from django.contrib import admin
from .models import CustomUser, Grade
from django.views.decorators.csrf import csrf_protect

# 1. Сыныптарды басқару (10А, 11Ә т.б.)
# users/admin.py
@csrf_protect
@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('number', 'letter')
    list_filter = ('number',)
    # МЫНА ЖОЛДЫ ҚОС: Пәндерді оң жақтан сол жаққа тастап таңдау үшін өте ыңғайлы
    filter_horizontal = ('specialized_subjects',)

# 2. Пайдаланушыларды (Оқушыларды) басқару
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('iin', 'last_name', 'first_name', 'middle_name', 'get_grade_display')
    search_fields = ('iin', 'last_name', 'first_name')
    list_filter = ('grade__number', 'grade__letter')

    # Сыныпты әдемілеп көрсету үшін функция
    def get_grade_display(self, obj):
        if obj.grade:
            return f"{obj.grade.number}\"{obj.grade.letter}\""
        return "Тағайындалмаған"
    
    get_grade_display.short_description = 'Сыныбы'