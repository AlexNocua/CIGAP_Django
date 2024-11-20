# 🌐 **Plataforma CIGAP**

## 📖 **Descripción del Proyecto**
La Plataforma CIGAP es una solución web desarrollada en Django que facilita la gestión y comunicación dentro de un entorno académico, permitiendo un acceso controlado y organizado para diferentes roles de usuarios como estudiantes, directores y correspondencia dirijida al cmomté de trabajos de grado. Además, incluye funcionalidades personalizadas como formularios de registro adaptados, manejo de grupos de usuarios y una interfaz intuitiva.

---

---

## 🌍 **Hostings o Páginas Disponibles**
- **Producción**:  
  👉 [Plataforma CIGAP (Producción)]
  🔗 URL: `[https://plataforma-cigap.railway.app](https://cigap-django-y1zm.onrender.com/)`


Nota: Asegúrate de que tengas las credenciales correspondientes para acceder a cada entorno.

---
## ✨ **Características Principales**
- **🧑‍🎓 Roles de Usuarios**:
  - **Estudiantes**: Registro personalizado con campos específicos y agrupación automática en el grupo *Estudiantes*.
  - **Directores**: Acceso a funcionalidades específicas mediante vistas protegidas.
  - **Correspondencia**: Gestión de comunicación interna.
- **🔒 Autenticación**:
  - Modelo personalizado de usuarios basado en `AbstractUser`, reemplazando el campo `username` por `email`.
  - Redirección automática a vistas específicas según el rol del usuario después del inicio de sesión.
- **📝 Formularios Personalizados**:
  - Formulario de registro con campos específicos como `primer_nombre`, `segundo_nombre`, `primer_apellido`, `segundo_apellido` y contraseñas (`password1`, `password2`).
  - Formulario exclusivo para subir imágenes.
- **⚙️ Gestión de Migraciones**:
  - Mantenimiento de integridad en migraciones para modelos complejos como `Estudiante` y `Usuarios`.
- **🔐 Seguridad**:
  - Uso de middleware como `login_required` para proteger vistas.
  - Reducción de conflictos en accesores inversos y modelos relacionados.

---

## 💻 **Tecnologías Utilizadas**
- **Backend**: Django Framework 🐍
- **Base de Datos**: SQLite y Postgres 🛢️
- **Frontend**: Bootstrap para diseño responsivo 🎨
- **Despliegue**: render 🚂



## ⚙️ **Configuraciones Importantes**

### 🛠️ **Ajustes en `settings.py`**
- Definir el modelo de usuario personalizado:
  ```python
  AUTH_USER_MODEL = 'estudiantes.Estudiantes'
