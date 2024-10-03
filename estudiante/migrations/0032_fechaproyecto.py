# Generated by Django 5.0.6 on 2024-10-02 05:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estudiante', '0031_modelanteproyecto_documento_radicado_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='FechaProyecto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inicio', models.DateField(blank=True, null=True)),
                ('fecha_finalizacion', models.DateField(blank=True, null=True)),
                ('fecha_etapa_uno', models.DateField(blank=True, null=True)),
                ('fecha_etapa_dos', models.DateField(blank=True, null=True)),
                ('fecha_etapa_tres', models.DateField(blank=True, null=True)),
                ('fecha_etapa_cuatro', models.DateField(blank=True, null=True)),
                ('fecha_etapa_cinco', models.DateField(blank=True, null=True)),
                ('fecha_etapa_seis', models.DateField(blank=True, null=True)),
                ('proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fechas', to='estudiante.modelproyectofinal')),
            ],
        ),
    ]
