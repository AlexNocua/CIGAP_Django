# Generated by Django 5.0.6 on 2024-09-28 22:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('estudiante', '0024_remove_modelproyectofinal_descripcion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='modelproyectofinal',
            name='codirector',
        ),
    ]
