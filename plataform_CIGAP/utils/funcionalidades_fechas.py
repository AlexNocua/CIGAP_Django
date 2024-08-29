import datetime
import pytz


# configuracion de la sona horaria de la aplicacion basada en la ciudad de bogota colombia
def fecha_actual():
    bogota_zone = pytz.timezone('America/Bogota')
    bogota_time = datetime.datetime.now(bogota_zone)
    bogota_timestr = bogota_time.strftime('%Y-%m-%d %H:%M:%S')
    fecha_actual = bogota_timestr
    return fecha_actual


print(fecha_actual())
