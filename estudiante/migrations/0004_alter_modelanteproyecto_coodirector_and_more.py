# Generated by Django 5.0.6 on 2024-08-28 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estudiante', '0003_alter_modelanteproyecto_director_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelanteproyecto',
            name='coodirector',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='modelanteproyecto',
            name='director',
            field=models.CharField(max_length=200, null=True),
        ),
    ]