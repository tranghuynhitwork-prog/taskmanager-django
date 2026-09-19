from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'priority', 'is_completed', 'due_date')
    list_filter = ('priority', 'is_completed')
    search_fields = ('title',)
    list_editable = ('is_completed',)
