from django.contrib import admin
from .models import Interface, UserInterfaceAccess
from exams.models import Course, Exam, Question, UserExam, ExamSession

@admin.register(Interface)
class InterfaceAdmin(admin.ModelAdmin):
    list_display = ('interface_id', 'module_name', 'function', 'url', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('module_name', 'function', 'url')
    ordering = ('-created_at',)

@admin.register(UserInterfaceAccess)
class UserInterfaceAccessAdmin(admin.ModelAdmin):
    list_display = ('access_id', 'user', 'interface', 'has_access', 'granted_date')
    list_filter = ('has_access', 'granted_date', 'interface')
    search_fields = ('user__name', 'interface__module_name')
    ordering = ('-granted_date',)
