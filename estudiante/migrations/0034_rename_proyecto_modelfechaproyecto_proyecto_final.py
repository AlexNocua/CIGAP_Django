# Generated by Django 5.0.6 on 2024-10-02 05:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('estudiante', '0033_rename_fechaproyecto_modelfechaproyecto'),
    ]

    operations = [
        migrations.RenameField(
            model_name='modelfechaproyecto',
            old_name='proyecto',
            new_name='proyecto_final',
        ),
    ]
