from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Task",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=150)),
                ("description", models.TextField()),
                (
                    "status",
                    models.CharField(
                        choices=[("pending", "Pendiente"), ("completed", "Completada")],
                        default="pending",
                        max_length=20,
                    ),
                ),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("unclassified", "Sin clasificar"),
                            ("personal", "Personal"),
                            ("work", "Trabajo"),
                            ("urgent", "Urgente"),
                            ("other", "Otra"),
                        ],
                        default="unclassified",
                        max_length=20,
                    ),
                ),
                ("subtasks", models.JSONField(blank=True, default=list)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"ordering": ["-created_at"]},
        )
    ]

