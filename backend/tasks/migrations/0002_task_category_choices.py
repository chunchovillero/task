from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tasks", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="categoria",
            field=models.CharField(
                choices=[
                    ("sin_clasificar", "Sin clasificar"),
                    ("urgente", "Urgente"),
                    ("no_urgente", "No urgente"),
                ],
                default="sin_clasificar",
                max_length=50,
            ),
        ),
    ]
