from ctypes import pythonapi
from pyexpat.errors import messages
from django.shortcuts import redirect, render
from django.urls import reverse
import win32com.client as win32
from datetime import datetime, timedelta

from login.models import Usuarios


def recuperar_cuenta(request):
    # Inicializa el entorno COM
    pythonapi.CoInitialize()

    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user = Usuarios.objects.get(email=email)
            token = get_random_string(length=32)
            user.token = token
            user.save()

            recovery_link = request.build_absolute_uri(
                reverse("login:recuperar_cuenta_confirm", args=[token])
            )

            # Configurar Outlook
            outlook = win32.Dispatch("outlook.application")

            # Configurar los detalles del correo
            asunto = "Recuperación de cuenta"
            cuerpo_html = f"""
            <div style="font-family: 'Saira', sans-serif; border-radius: 10px; padding: 20px; background-color: #002412; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1); max-width: 600px; margin: 0 auto;">
                <div style="background: #ffffff; border-radius: 12px;">
                    <header style="width: 100%; display: flex; background: #ffffff; padding: 0; border-radius: 10px 10px 0 0; align-items: center; justify-content: center;">
                        <img src="https://upload.wikimedia.org/wikipedia/commons/1/11/Logo_Universidad_de_Cundinamarca.png" alt="Logo Universidad de Cundinamarca" style="margin: 0 auto; padding: 8px; z-index: 0; max-width: 100%; max-height: 165px;">
                    </header>
                    <h1 style="width: 100%; background-color: #002412; margin: 0; padding: 12px 0; text-align: center; color: #ffffff; margin-bottom: 20px;">Plataforma CIGAP Ubaté</h1>
                    <h2 style="color: #000000;padding: 0 12px;">Recuperación de contraseña para <span style="font-weight: bold;">{email}</span></h2>
                    <p style="padding: 0 12px; color: #666666;">Hola <span style="color: #007A3D; font-weight: bold;">{user.nombres}</span>, has solicitado la recuperación de tu contraseña para la cuenta creada con el correo <span style="color: #007A3D; font-weight: bold;">{email}</span>.</p>
                    <p style="padding: 0 12px; color: #666666;">Para restablecer tu contraseña, haz clic en el siguiente enlace: <a href="{recovery_link}" style="color: #007A3D; text-decoration: none;">Recuperar cuenta</a></p>
                    <p style="padding: 0 12px; color: #666666;">Recuerda que la protección de tus datos es importante, puedes cambiar tu contraseña accediendo a la plataforma.</p>
                    <h3 style="padding: 0 12px; color: #000000;">Estaremos en contacto.</h3>
                    <div style="width: 100%; background: #3C3C3B; padding: 0; border-radius: 0 0 10px 10px;">
                        <div style="padding: 8px;">
                            <h2 style="color: #fff; margin-bottom: 5px; font-weight: 600; text-align: center;">Respuesta automática de la plataforma <br> CIGAP</h2>
                            <p style="color: #fff; margin-top: 5px; text-align: center; font-size: 12px;">No responder a este correo.</p>
                        </div>
                    </div>
                </div>
            </div>
            """

            # Crear y enviar el mensaje
            mail = outlook.CreateItem(0)
            mail.To = email
            mail.Subject = asunto
            mail.HTMLBody = cuerpo_html

            # Enviar el correo
            mail.Send()

            messages.success(
                request,
                "Se ha enviado un enlace de recuperación a tu correo electrónico.",
            )
            return redirect("login:loginapps")

        except Usuarios.DoesNotExist:
            messages.error(request, "No existe un usuario con ese correo electrónico.")

        except Exception as e:
            messages.error(
                request,
                f"Hubo un error al enviar el correo de recuperación: {str(e)}. Por favor, intenta nuevamente.",
            )
            return render(request, "recuperar_cuenta.html")

    return render(request, "recuperar_cuenta.html")


# Función para enviar correos recordatorios
def enviar_recordatorios(email, user, fecha_finalizacion):
    outlook = win32.Dispatch("outlook.application")

    # Calcular fechas de recordatorio
    seis_meses_antes = fecha_finalizacion - timedelta(days=180)
    cuatro_meses_antes = fecha_finalizacion - timedelta(days=120)
    dos_meses_antes = fecha_finalizacion - timedelta(days=60)

    # Configurar detalles de los correos
    recordatorios = [
        {
            "fecha": seis_meses_antes,
            "asunto": "Recordatorio: Seis meses para la finalización del proyecto",
            "cuerpo": f"""
            <div style="font-family: 'Saira', sans-serif; border-radius: 10px; padding: 20px; background-color: #002412; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1); max-width: 600px; margin: 0 auto;">
                <div style="background: #ffffff; border-radius: 12px;">
                    <header style="width: 100%; display: flex; background: #ffffff; padding: 0; border-radius: 10px 10px 0 0; align-items: center; justify-content: center;">
                        <img src="https://upload.wikimedia.org/wikipedia/commons/1/11/Logo_Universidad_de_Cundinamarca.png" alt="Logo Universidad de Cundinamarca" style="margin: 0 auto; padding: 8px; z-index: 0; max-width: 100%; max-height: 165px;">
                    </header>
                    <h1 style="width: 100%; background-color: #002412; margin: 0; padding: 12px 0; text-align: center; color: #ffffff; margin-bottom: 20px;">Plataforma CIGAP Ubaté</h1>
                    <h2 style="color: #000000;padding: 0 12px;">Estimado/a <span style="font-weight: bold;">{email}</span>,</h2>
                    <p style="padding: 0 12px; color: #666666;">Por medio de la presente, le informamos que faltan seis meses para la fecha de finalización de su proyecto.</p>
                    <p style="padding: 0 12px; color: #666666;">Fecha de finalización: <strong>{fecha_finalizacion.strftime('%Y-%m-%d')}</strong></p>
                    <p style="padding: 0 12px; color: #666666;">Le exhortamos a aprovechar este tiempo para avanzar en su trabajo.</p>
                    <h3 style="padding: 0 12px; color: #000000;">Quedamos a su disposición para cualquier consulta.</h3>
                    <div style="width: 100%; background: #3C3C3B; padding: 0; border-radius: 0 0 10px 10px;">
                        <div style="padding: 8px;">
                            <h2 style="color: #fff; margin-bottom: 5px; font-weight: 600; text-align: center;">Respuesta automática de la plataforma <br> CIGAP</h2>
                            <p style="color: #fff; margin-top: 5px; text-align: center; font-size: 12px;">No responder a este correo.</p>
                        </div>
                    </div>
                </div>
            </div>
            """,
        },
        {
            "fecha": cuatro_meses_antes,
            "asunto": "Recordatorio: Cuatro meses para la finalización del proyecto",
            "cuerpo": f"""
            <div style="font-family: 'Saira', sans-serif; border-radius: 10px; padding: 20px; background-color: #002412; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1); max-width: 600px; margin: 0 auto;">
                <div style="background: #ffffff; border-radius: 12px;">
                    <header style="width: 100%; display: flex; background: #ffffff; padding: 0; border-radius: 10px 10px 0 0; align-items: center; justify-content: center;">
                        <img src="https://upload.wikimedia.org/wikipedia/commons/1/11/Logo_Universidad_de_Cundinamarca.png" alt="Logo Universidad de Cundinamarca" style="margin: 0 auto; padding: 8px; z-index: 0; max-width: 100%; max-height: 165px;">
                    </header>
                    <h1 style="width: 100%; background-color: #002412; margin: 0; padding: 12px 0; text-align: center; color: #ffffff; margin-bottom: 20px;">Plataforma CIGAP Ubaté</h1>
                    <h2 style="color: #000000;padding: 0 12px;">Estimado/a <span style="font-weight: bold;">{email}</span>,</h2>
                    <p style="padding: 0 12px; color: #666666;">Le informamos que faltan cuatro meses para la fecha de finalización de su proyecto.</p>
                    <p style="padding: 0 12px; color: #666666;">Fecha de finalización: <strong>{fecha_finalizacion.strftime('%Y-%m-%d')}</strong></p>
                    <p style="padding: 0 12px; color: #666666;">Le sugerimos planificar su tiempo de manera adecuada.</p>
                    <h3 style="padding: 0 12px; color: #000000;">Quedamos a su disposición para cualquier consulta.</h3>
                    <div style="width: 100%; background: #3C3C3B; padding: 0; border-radius: 0 0 10px 10px;">
                        <div style="padding: 8px;">
                            <h2 style="color: #fff; margin-bottom: 5px; font-weight: 600; text-align: center;">Respuesta automática de la plataforma <br> CIGAP</h2>
                            <p style="color: #fff; margin-top: 5px; text-align: center; font-size: 12px;">No responder a este correo.</p>
                        </div>
                    </div>
                </div>
            </div>
            """,
        },
        {
            "fecha": dos_meses_antes,
            "asunto": "Recordatorio: Dos meses para la finalización del proyecto",
            "cuerpo": f"""
            <div style="font-family: 'Saira', sans-serif; border-radius: 10px; padding: 20px; background-color: #002412; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1); max-width: 600px; margin: 0 auto;">
                <div style="background: #ffffff; border-radius: 12px;">
                    <header style="width: 100%; display: flex; background: #ffffff; padding: 0; border-radius: 10px 10px 0 0; align-items: center; justify-content: center;">
                        <img src="https://upload.wikimedia.org/wikipedia/commons/1/11/Logo_Universidad_de_Cundinamarca.png" alt="Logo Universidad de Cundinamarca" style="margin: 0 auto; padding: 8px; z-index: 0; max-width: 100%; max-height: 165px;">
                    </header>
                    <h1 style="width: 100%; background-color: #002412; margin: 0; padding: 12px 0; text-align: center; color: #ffffff; margin-bottom: 20px;">Plataforma CIGAP Ubaté</h1>
                    <h2 style="color: #000000;padding: 0 12px;">Estimado/a <span style="font-weight: bold;">{email}</span>,</h2>
                    <p style="padding: 0 12px; color: #666666;">Le recordamos que faltan dos meses para la fecha de finalización de su proyecto.</p>
                    <p style="padding: 0 12px; color: #666666;">Fecha de finalización: <strong>{fecha_finalizacion.strftime('%Y-%m-%d')}</strong></p>
                    <p style="padding: 0 12px; color: #666666;">Esta es la última oportunidad para realizar los ajustes necesarios.</p>
                    <h3 style="padding: 0 12px; color: #000000;">Quedamos a su disposición para cualquier consulta.</h3>
                    <div style="width: 100%; background: #3C3C3B; padding: 0; border-radius: 0 0 10px 10px;">
                        <div style="padding: 8px;">
                            <h2 style="color: #fff; margin-bottom: 5px; font-weight: 600; text-align: center;">Respuesta automática de la plataforma <br> CIGAP</h2>
                            <p style="color: #fff; margin-top: 5px; text-align: center; font-size: 12px;">No responder a este correo.</p>
                        </div>
                    </div>
                </div>
            </div>
            """,
        },
    ]

    # Enviar correos
    for recordatorio in recordatorios:
        if datetime.now() < recordatorio["fecha"]:
            mail = outlook.CreateItem(0)
            mail.To = email
            mail.Subject = recordatorio["asunto"]
            mail.HTMLBody = recordatorio["cuerpo"]
            mail.Send()


# Uso de la función
# Suponiendo que tienes la fecha de finalización del proyecto y el usuario
email = "ejemplo@dominio.com"
user = type(
    "User", (object,), {"nombres": "Juan"}
)  # Simulación de un objeto de usuario
fecha_finalizacion = datetime(2024, 11, 30)  # Fecha de finalización del proyecto
enviar_recordatorios(email, user, fecha_finalizacion)
