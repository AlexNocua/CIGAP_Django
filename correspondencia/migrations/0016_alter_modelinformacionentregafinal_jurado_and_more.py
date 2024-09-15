# Generated by Django 5.0.6 on 2024-09-12 21:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('correspondencia', '0015_remove_modelretroalimentaciones_jurado'),
        ('estudiante', '0020_modelasignacionjurados_modelproyectofinal_jurado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelinformacionentregafinal',
            name='jurado',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Informacion_Entrega_Final', to='estudiante.modelasignacionjurados'),
        ),
        migrations.DeleteModel(
            name='ModelAsignacionJurados',
        ),
    ]