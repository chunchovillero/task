from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "category", "created_at")
    list_filter = ("status", "category")
    search_fields = ("title", "description")

