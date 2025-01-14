# Generated by Django 5.1.4 on 2025-01-08 06:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("userauths", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="user_type",
            field=models.CharField(
                blank=True,
                choices=[("Doctor", "Доктор"), ("Patient", "Пациент")],
                default=None,
                max_length=50,
                null=True,
            ),
        ),
    ]
