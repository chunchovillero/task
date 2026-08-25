from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "titulo",
            "descripcion",
            "estado",
            "categoria",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "categoria",
            "created_at",
        ]
