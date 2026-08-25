from django.db import migrations, models


def translate_values_to_english(apps, schema_editor):
    Task = apps.get_model("tasks", "Task")
    Task.objects.filter(status="pendiente").update(status="pending")
    Task.objects.filter(status="completado").update(status="completed")
    Task.objects.filter(category="sin_clasificar").update(category="unclassified")
    Task.objects.filter(category="urgente").update(category="urgent")
    Task.objects.filter(category="no_urgente").update(category="not_urgent")


def translate_values_to_spanish(apps, schema_editor):
    Task = apps.get_model("tasks", "Task")
    Task.objects.filter(status="pending").update(status="pendiente")
    Task.objects.filter(status="completed").update(status="completado")
    Task.objects.filter(category="unclassified").update(category="sin_clasificar")
    Task.objects.filter(category="urgent").update(category="urgente")
    Task.objects.filter(category="not_urgent").update(category="no_urgente")


class Migration(migrations.Migration):
    dependencies = [
        ("tasks", "0002_task_category_choices"),
    ]

    operations = [
        migrations.RenameField(model_name="task", old_name="titulo", new_name="title"),
        migrations.RenameField(
            model_name="task", old_name="descripcion", new_name="description"
        ),
        migrations.RenameField(model_name="task", old_name="estado", new_name="status"),
        migrations.RenameField(
            model_name="task", old_name="categoria", new_name="category"
        ),
        migrations.RunPython(
            translate_values_to_english,
            reverse_code=translate_values_to_spanish,
        ),
        migrations.AlterField(
            model_name="task",
            name="status",
            field=models.CharField(
                choices=[("pending", "Pendiente"), ("completed", "Completado")],
                default="pending",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="category",
            field=models.CharField(
                choices=[
                    ("unclassified", "Sin clasificar"),
                    ("urgent", "Urgente"),
                    ("not_urgent", "No urgente"),
                ],
                default="unclassified",
                max_length=50,
            ),
        ),
    ]
