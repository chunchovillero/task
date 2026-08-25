from django.db import models


class Task(models.Model):
    class Status(models.TextChoices):
        PENDIENTE = "pendiente", "Pendiente"
        COMPLETADO = "completado", "Completado"

    class Category(models.TextChoices):
        SIN_CLASIFICAR = "sin_clasificar", "Sin clasificar"
        URGENTE = "urgente", "Urgente"
        NO_URGENTE = "no_urgente", "No urgente"

    titulo = models.CharField(max_length=200)

    descripcion = models.TextField()

    estado = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDIENTE,
    )

    categoria = models.CharField(
        max_length=50,
        choices=Category.choices,
        default=Category.SIN_CLASIFICAR,
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.titulo
