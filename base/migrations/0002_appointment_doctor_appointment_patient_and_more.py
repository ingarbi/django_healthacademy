# Generated by Django 5.1.4 on 2025-01-02 16:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0001_initial"),
        ("patient", "0001_initial"),
        ("physician", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="appointment",
            name="doctor",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="doctor_appointment",
                to="physician.doctor",
            ),
        ),
        migrations.AddField(
            model_name="appointment",
            name="patient",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="patient_appointment",
                to="patient.patient",
            ),
        ),
        migrations.AddField(
            model_name="billing",
            name="patient",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="patient_billing",
                to="patient.patient",
            ),
        ),
        migrations.AddField(
            model_name="service",
            name="available",
            field=models.ManyToManyField(blank=True, to="physician.doctor"),
        ),
    ]
