
import pytz
from datetime import datetime, timedelta


# configuracion de la sona horaria de la aplicacion basada en la ciudad de bogota colombia
def fecha_actual():
    bogota_zone = pytz.timezone('America/Bogota')
    bogota_time = datetime.now(bogota_zone)
    bogota_timestr = bogota_time.strftime('%Y-%m-%d %H:%M:%S')
    return bogota_timestr


def fecha_maxima_respuesta(fecha):
    if not isinstance(fecha, datetime):

        fecha_inicial = datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S")
    else:
        fecha_inicial = fecha

    dias_a_sumar = 10
    dias_agregados = 0

    while dias_agregados < dias_a_sumar:
        fecha_inicial += timedelta(days=1)
        if fecha_inicial.weekday() < 5:
            dias_agregados += 1

    fecha_final = fecha_inicial
    return fecha_final

# print(fecha_actual())
