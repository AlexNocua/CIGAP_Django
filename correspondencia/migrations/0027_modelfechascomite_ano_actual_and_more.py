# Generated by Django 5.0.6 on 2024-10-10 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('correspondencia', '0026_modelfechascomite'),
    ]

    operations = [
        migrations.AddField(
            model_name='modelfechascomite',
            name='ano_actual',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='modelfechascomite',
            name='periodo_academico',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
