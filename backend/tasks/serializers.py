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
            "subtasks",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["category", "subtasks", "created_at", "updated_at"]

    def validate_title(self, value):
        value = value.strip()
        if len(value) < 3:
            raise serializers.ValidationError("El título debe tener al menos 3 caracteres.")
        return value

    def validate_description(self, value):
        value = value.strip()
        if len(value) < 5:
            raise serializers.ValidationError(
                "La descripción debe tener al menos 5 caracteres."
            )
        return value

