# Generated by Django 5.1 on 2024-11-20 06:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('estudiante', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ModelDocumentos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_documento', models.CharField(max_length=100)),
                ('version', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=500)),
                ('documento', models.BinaryField(blank=True, null=True)),
                ('fecha_cargue', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Documentos',
            },
        ),
        migrations.CreateModel(
            name='ModelFechasComite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ano_actual', models.IntegerField(blank=True, null=True)),
                ('periodo_academico', models.CharField(blank=True, max_length=10, null=True)),
                ('primer_encuentro', models.DateField(blank=True, null=True)),
                ('segundo_encuentro', models.DateField(blank=True, null=True)),
                ('tercer_encuentro', models.DateField(blank=True, null=True)),
                ('cuarto_encuentro', models.DateField(blank=True, null=True)),
                ('extraordinaria', models.DateField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Fechas de Comite',
            },
        ),
        migrations.CreateModel(
            name='ModelInformacionEntregaFinal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doc_proyecto_final_cedido', models.BinaryField(blank=True, null=True)),
                ('fecha_finalizacion', models.DateTimeField(blank=True, null=None)),
                ('anteproyecto', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Informacion_Entrega_Final', to='estudiante.modelanteproyecto')),
                ('fechas_proyecto', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Informacion_Entrega_Final', to='estudiante.modelfechasproyecto')),
                ('proyecto_final', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Informacion_Entrega_Final', to='estudiante.modelproyectofinal')),
            ],
            options={
                'verbose_name_plural': 'Informaciones de Entregas Finales',
            },
        ),
        migrations.CreateModel(
            name='ModelRetroalimentaciones',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('retroalimentacion', models.TextField(max_length=10000)),
                ('fecha_retroalimentacion', models.DateTimeField(blank=True, null=True)),
                ('doc_retroalimentacion', models.BinaryField(blank=True, null=True)),
                ('estado', models.CharField(blank=True, choices=[('Aprobado', 'Aprobado'), ('Rechazado', 'Rechazado')], default='aprobado', max_length=25, null=True)),
                ('revs_dadas', models.IntegerField(blank=True, null=True)),
                ('anteproyecto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Retroalimentaciones', to='estudiante.modelanteproyecto')),
                ('proyecto_final', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Retroalimentaciones', to='estudiante.modelproyectofinal')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Retroalimentaciones', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Retroalimentaciones',
            },
        ),
        migrations.CreateModel(
            name='ModelSolicitudes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_solicitud', models.CharField(choices=[('cambio_nombre', 'Cambio de nombre del proyecto'), ('ajuste_integrantes', 'Ajuste de integrantes del proyecto'), ('cesion_derechos', 'Cesión de derechos del proyecto'), ('otro', 'Otro')], default='otro', max_length=200)),
                ('motivo_solicitud', models.TextField(max_length=10000)),
                ('documento_soporte', models.BinaryField(blank=True, null=True)),
                ('fecha_envio', models.DateTimeField(blank=True, null=True)),
                ('estado', models.BooleanField(default=False)),
                ('anteproyecto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Solicitudes', to='estudiante.modelanteproyecto')),
                ('proyecto_final', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Solicitudes', to='estudiante.modelproyectofinal')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Solicitudes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Solicitudes',
            },
        ),
    ]
