# Generated by Django 5.0.6 on 2024-10-02 06:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('estudiante', '0036_remove_modelobjetivogeneral_anteproyecto_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='modelobjetivogeneral',
            name='estado',
        ),
    ]
