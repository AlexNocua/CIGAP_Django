# Generated by Django 5.0.6 on 2024-08-31 16:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('estudiante', '0006_alter_modelanteproyecto_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='modelanteproyecto',
            old_name='nombre_proyecto',
            new_name='nombre_anteproyecto',
        ),
        migrations.RemoveField(
            model_name='modelanteproyecto',
            name='estado_solicitud_anteproyecto',
        ),
        migrations.RemoveField(
            model_name='modelanteproyecto',
            name='retroalimentacion',
        ),
    ]
