# Generated by Django 5.0.6 on 2024-08-30 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_usuarios_nombre_completo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuarios',
            name='nombre_completo',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
