# Generated by Django 5.0.6 on 2024-09-05 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('correspondencia', '0006_alter_modelasignacionjurados_proyecto_final_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelretroalimentaciones',
            name='estado',
            field=models.CharField(choices=[('Aprobado', 'Aprobado'), ('Aprobado_con_correcciones', 'Aprobado con correcciones'), ('Rechazado', 'Rechazado')], default='aprobado', max_length=25),
        ),
    ]
