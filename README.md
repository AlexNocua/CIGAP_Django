```markdown
# 🌐 **Plataforma CIGAP**

## 📖 **Descripción del Proyecto**
La Plataforma CIGAP es una solución web desarrollada en Django que facilita la gestión y comunicación dentro de un entorno académico, permitiendo un acceso controlado y organizado para diferentes roles de usuarios como estudiantes, directores y correspondencia dirigida al Comité de Trabajos de Grado. Además, incluye funcionalidades personalizadas como formularios de registro adaptados, manejo de grupos de usuarios y una interfaz intuitiva.

---

## 🌍 **Hostings o Páginas Disponibles**
- **Producción**:  
  👉 [Plataforma CIGAP (Producción)](https://cigap-django-y1zm.onrender.com/)  
  🔗 URL: `https://cigap-django-y1zm.onrender.com/`

Nota: Asegúrate de que tengas las credenciales correspondientes para acceder a cada entorno.

---

## ✨ **Características Principales**
- **🧑‍🎓 Roles de Usuarios**:
  - **Estudiantes**: Cargues de documentos respecto a anteporyectos y proyectos de grado (proyectos finales).
  - **Directores**: Asignación de anteproyectos y proyectos de grado, también evaluación y calificación de los mismos.
  - **Correspondencia**: Proceso general del comite de trabajos de grado junto con correspondecia.
- **🔒 Autenticación**:
  - Modelo personalizado de usuarios basado en `AbstractUser`, reemplazando el campo `username` por `email`.
  - Redirección automática a vistas específicas según el rol del usuario después del inicio de sesión.
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
- **Despliegue**: Render 🚂  
```
