from django.db import models


class Task(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pendiente"
        COMPLETED = "completed", "Completado"

    class Category(models.TextChoices):
        UNCLASSIFIED = "unclassified", "Sin clasificar"
        URGENT = "urgent", "Urgente"
        NOT_URGENT = "not_urgent", "No urgente"

    title = models.CharField(max_length=200)

    description = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    category = models.CharField(
        max_length=50,
        choices=Category.choices,
        default=Category.UNCLASSIFIED,
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title
