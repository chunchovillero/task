from django.db import models


class Task(models.Model):
    class Status(models.TextChoices):
        PENDIENTE = "pendiente", "Pendiente"
        COMPLETADO = "completado", "Completado"

    titulo = models.CharField(max_length=200)

    descripcion = models.TextField()

    estado = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDIENTE,
    )

    categoria = models.CharField(
        max_length=50,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.titulo