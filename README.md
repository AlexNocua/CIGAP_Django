# 🌐 Plataforma CIGAP

## 📖 Descripción del Proyecto
La **Plataforma CIGAP** es una solución web desarrollada en Django que facilita la gestión y comunicación dentro de un entorno académico. Permite un acceso controlado y organizado para diferentes roles de usuarios, tales como estudiantes, directores y correspondencia dirigida al Comité de Trabajos de Grado. Además, incluye funcionalidades personalizadas como formularios de registro adaptados, manejo de grupos de usuarios y una interfaz intuitiva.

---

## 🌍 Hostings o Páginas Disponibles
- **Producción**:  
  👉 [Plataforma CIGAP (Producción)](https://cigap-django-y1zm.onrender.com/)  
  🔗 URL: `https://cigap-django-y1zm.onrender.com/`

**Nota**: Asegúrate de contar con las credenciales correspondientes para acceder a cada entorno.

---

## ✨ Características Principales
### 🧑‍🎓 Roles de Usuarios
- **Estudiantes**:  
  Permite la carga de documentos relacionados con anteproyectos y proyectos de grado (proyectos finales).  
- **Directores**:  
  Incluye la asignación de anteproyectos y proyectos de grado, además de funcionalidades para evaluar y calificar.  
- **Correspondencia**:  
  Gestiona procesos generales del Comité de Trabajos de Grado junto con la correspondencia.

### 🔒 Autenticación
- Modelo personalizado de usuarios basado en `AbstractUser`, utilizando el campo `email` en lugar de `username`.
- Redirección automática a vistas específicas según el rol del usuario tras el inicio de sesión.

### ⚙️ Gestión de Migraciones
- Garantiza la integridad en migraciones para modelos complejos, como `Estudiante` y `Usuarios`.

### 🔐 Seguridad
- Implementación de middleware como `login_required` para proteger las vistas.
- Resolución de conflictos en accesores inversos y modelos relacionados.

---

## 💻 Tecnologías Utilizadas
- **Backend**: Django Framework 🐍  
- **Base de Datos**: SQLite y PostgreSQL 🛢️  
- **Frontend**: Bootstrap para diseño responsivo 🎨  
- **Despliegue**: Render 🚂
