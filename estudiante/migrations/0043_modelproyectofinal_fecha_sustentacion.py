# Generated by Django 5.0.6 on 2024-10-10 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estudiante', '0042_modelobjetivosespecificos_documento_correcciones_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='modelproyectofinal',
            name='fecha_sustentacion',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]