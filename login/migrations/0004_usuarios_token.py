# Generated by Django 5.0.6 on 2024-09-30 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_alter_usuarios_nombre_completo'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuarios',
            name='token',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]
