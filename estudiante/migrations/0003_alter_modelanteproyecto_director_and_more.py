# Generated by Django 5.0.6 on 2024-08-28 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estudiante', '0002_modelanteproyecto_enviado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelanteproyecto',
            name='director',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='modelanteproyecto',
            name='nombre_integrante2',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
