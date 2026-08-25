from django.db import models


class Task(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pendiente"
        COMPLETED = "completed", "Completada"

    class Category(models.TextChoices):
        UNCLASSIFIED = "unclassified", "Sin clasificar"
        PERSONAL = "personal", "Personal"
        WORK = "work", "Trabajo"
        URGENT = "urgent", "Urgente"
        OTHER = "other", "Otra"

    title = models.CharField(max_length=150)
    description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.UNCLASSIFIED,
    )
    subtasks = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

