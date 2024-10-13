import os
from dotenv import load_dotenv

from plataform_CIGAP.settings import base_dir

print(base_dir())
# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Lista de variables de entorno a verificar
env_vars = [
    "SECRET_KEY",
    "ALLOWED_HOSTS",
    "DEBUG",
    "DATABASE_URL",
    "SUPERUSER_USERNAME",
    "APP_PASSWORD",
    "SUPERUSER_PASSWORD",
]

print(os.getenv("DATABASE_URL"))
print(os.getenv("ALLOWED_HOSTS"))
# Verificar y imprimir la existencia de cada variable de entorno
for var in env_vars:
    value = os.getenv(var)
    print(f"{var} exists: {bool(value)}")
