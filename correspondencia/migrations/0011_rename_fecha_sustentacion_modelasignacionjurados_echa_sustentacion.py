# Generated by Django 5.0.6 on 2024-09-12 03:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('correspondencia', '0010_alter_modelasignacionjurados_proyecto_final_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='modelasignacionjurados',
            old_name='fecha_sustentacion',
            new_name='echa_sustentacion',
        ),
    ]
