# Generated by Django 5.0.6 on 2024-09-12 21:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('correspondencia', '0014_alter_modelretroalimentaciones_estado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='modelretroalimentaciones',
            name='jurado',
        ),
    ]