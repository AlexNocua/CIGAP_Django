# 🌐 Plataforma CIGAP

## 📖 Descripción del Proyecto
La **Plataforma CIGAP** es una solución web desarrollada en Django que facilita la gestión y comunicación dentro de un entorno académico. Permite un acceso controlado y organizado para diferentes roles de usuarios, tales como estudiantes, directores y correspondencia dirigida al Comité de Trabajos de Grado. Además, incluye funcionalidades personalizadas como formularios de registro adaptados, manejo de grupos de usuarios y una interfaz intuitiva.

## 🎥 Videos de Uso de la Plataforma  
A continuación, se presentan videos explicativos sobre cómo usar las diferentes funcionalidades de la plataforma según el rol asignado:  

1. ## 🔑 Uso del Administrador  

### 🎥 Video Tutorial  
[Accede al video aquí](https://www.youtube.com/watch?v=Vp9n2EjykiY)  
   👉 **Descripción**: Este video guía al administrador en la gestión de usuarios, configuración de roles y supervisión de la plataforma.

> 📌 **Nota**: Haz click en el hipervinculo para ir al video correspondiente.


---

## 🌍 Hostings o Páginas Disponibles  
- **Producción**:  
  👉 [Plataforma CIGAP (Producción)](https://cigap-django.onrender.com)  
  🔗 URL: `https://cigap-django-a09b.onrender.com`

## 👥 Usuarios Disponibles  
A continuación, se presentan usuarios de prueba según sus roles:  

| Rol              | Correo                     | Contraseña       |  
|-------------------|----------------------------|------------------|  
| 👩‍🎓 **Estudiante**  | aenocua@ucundinamarca.edu.co      | A@lexk14alex    |  
| 👨‍🏫 **Director**     | manuel@ucundinamarca.edu.co        | M@nuEl123      |  
| 📋 **Comité**       | correspondencia@ucundinamarca.edu.co          | 2024Cig@pCorres        |  
| 🔑 **Administrador** | plataformaCIGAPUbate@outlook.com           | CiGAPUb@te2024         |  

> ⚠️ **Nota:** Estos usuarios son solo para fines de demostración.  

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
