# Generated by Django 5.0.6 on 2024-09-04 20:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estudiante', '0011_alter_modelanteproyecto_descripcion'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ModelProyectoFinal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField(blank=True, max_length=10000, null=True)),
                ('carta_presentacion_final', models.BinaryField(blank=True, null=True)),
                ('proyecto_final', models.BinaryField(blank=True, null=True)),
                ('director', models.CharField(max_length=200, null=True)),
                ('fecha_envio', models.CharField(max_length=200)),
                ('solicitud_enviada', models.BooleanField()),
                ('anteproyecto', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='Proyecto_Final', to='estudiante.modelanteproyecto')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='Proyecto_Final', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Estudiante',
        ),
        migrations.DeleteModel(
            name='EtapasProyecto',
        ),
        migrations.DeleteModel(
            name='ModelPrimeraSolicitud',
        ),
        migrations.DeleteModel(
            name='Observaciones',
        ),
        migrations.DeleteModel(
            name='ProyectoGrado',
        ),
    ]