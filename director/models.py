from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.


# class Director(AbstractUser):
#     nombres = models.CharField(max_length=100, verbose_name='Nombres')
#     apellidos = models.CharField(max_length=100, verbose_name='Apellidos')
#     email = models.EmailField(
#         max_length=100, unique=True, verbose_name='Correo')
#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
#     # Campos relacionados
#     groups = models.ManyToManyField(
#         'auth.Group',
#         related_name='Directores',
#         blank=True,
#         help_text='Grupos a los que pertenece este usuario.',
#         verbose_name='grupos'
#     )
#     user_permissions = models.ManyToManyField(
#         'auth.Permission',
#         related_name='Directores',
#         blank=True,
#         help_text='Permisos específicos para este usuario.',
#         verbose_name='permisos'
#     )
