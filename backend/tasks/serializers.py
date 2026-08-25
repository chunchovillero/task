from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "category",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "category",
            "created_at",
        ]
