# Generated by Django 5.0.6 on 2024-09-23 22:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estudiante', '0020_modelasignacionjurados_modelproyectofinal_jurado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelproyectofinal',
            name='anteproyecto',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Proyecto_Final', to='estudiante.modelanteproyecto'),
        ),
    ]