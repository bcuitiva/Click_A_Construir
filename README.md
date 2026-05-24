# Click a Construir

Plataforma web que conecta clientes con profesionales de construcción y remodelación en Colombia. Desarrollada como proyecto académico para la asignatura **Ingeniería de Software II** — Universidad de Cundinamarca, 6.º semestre.

---

## Descripción

Click a Construir permite a los clientes publicar proyectos de construcción o remodelación y encontrar profesionales calificados, mientras que los profesionales pueden explorar proyectos disponibles, gestionar su trabajo y mantener comunicación directa con los clientes. Todo desde una plataforma web accesible y fácil de usar.

---

## Tecnologías utilizadas

| Capa | Tecnología |
|---|---|
| Backend | Python 3.14 + Flask |
| Plantillas | Jinja2 |
| Frontend | HTML5, CSS3, JavaScript vanilla |
| Base de datos | Supabase (PostgreSQL) |
| Autenticación | Supabase Auth (bcrypt internamente) |
| Almacenamiento | Supabase Storage |
| Control de versiones | Git + GitHub |

---

## Estructura del proyecto

```
cac_v2/
├── app.py                          # Servidor Flask — rutas y lógica
├── db.py                           # Capa de acceso a datos (Supabase o memoria)
├── validators.py                   # Validaciones de entrada
├── test_validators.py              # 55 pruebas unitarias
├── requirements.txt
├── .env.example                    # Plantilla de variables de entorno
├── static/
│   ├── css/main.css                # Estilos globales
│   ├── js/
│   │   ├── main.js                 # Tabs, modal, carrusel
│   │   └── chat.js                 # Lógica del chat y adjuntos
│   └── img/
│       ├── logo_login.png
│       └── logo_dashboard.png
└── templates/
    ├── base.html                   # Layout base
    ├── macros.html                 # Sidebar, topbar y avatar reutilizables
    ├── chat_macro.html             # Componente de chat
    ├── login.html                  # Inicio de sesión y registro
    ├── confirm.html                # Confirmación de correo
    ├── forgot_password.html        # Solicitar recuperación de contraseña
    ├── reset_password.html         # Crear nueva contraseña
    ├── cliente/
    │   ├── inicio.html             # Carrusel de profesionales con filtros
    │   ├── proyectos.html          # Lista de proyectos con barra de progreso
    │   ├── proyecto_detalle.html   # Detalle, tareas, avances y galería
    │   ├── perfil.html             # Perfil propio con modal de edición
    │   ├── perfil_profesional.html # Perfil público de un profesional
    │   └── mensajes.html           # Chat con adjuntos
    └── profesional/
        ├── inicio.html             # Proyectos disponibles con filtros
        ├── proyectos.html          # Mis proyectos activos
        ├── proyecto_gestion.html   # Gestión: tareas, avances e imágenes
        ├── proyecto_disponible.html# Detalle de proyecto disponible
        ├── perfil.html             # Perfil con redes sociales y modal de edición
        └── mensajes.html           # Chat con adjuntos
```

---

## Funcionalidades

### Autenticación
- Registro con validación de nombre, correo, contraseña segura y rol
- Contraseña con mínimo 8 caracteres, mayúscula, minúscula, número y símbolo
- Confirmación de correo electrónico vía Supabase Auth
- Recuperación de contraseña con enlace seguro por correo
- Indicador visual de fortaleza de contraseña en tiempo real
- Sesiones manejadas con Flask + Supabase Auth

### Dashboard Cliente
- Carrusel horizontal de profesionales con filtros por especialidad, ciudad y calificación
- Barra de búsqueda con filtros avanzados
- Publicación de proyectos con categoría, ubicación, presupuesto, fechas e imágenes
- Formato automático del presupuesto en pesos colombianos al escribir
- Lista de proyectos con barra de progreso en tiempo real
- Detalle de proyecto: tareas, avances del profesional con fotos y línea de tiempo
- Vista del perfil público de profesionales con calificación en estrellas y reseñas

### Dashboard Profesional
- Exploración de proyectos disponibles con filtros por categoría, ciudad y presupuesto máximo
- Gestión de proyectos asignados: cambiar estado, agregar y completar tareas
- Publicación de avances con texto e imágenes (línea de tiempo)
- Subida de fotos del proyecto

### Mensajes
- Chat en tiempo real tipo Facebook/Instagram
- Conversaciones organizadas en lista con preview del último mensaje
- Envío de texto, imágenes y archivos PDF
- Vista previa del adjunto antes de enviar
- Contador de mensajes no leídos en sidebar y topbar

### Perfiles
- Vista previa del perfil completo como lo ve el público
- Edición a través de modal (sin exponer el formulario directamente)
- Foto de perfil con preview antes de subir
- Profesional: especialidad, bio, calificación promedio en estrellas, reseñas de clientes y redes sociales (Instagram, Facebook, WhatsApp, sitio web)
- Cliente: bio, datos de contacto y proyectos publicados

### Seguridad
- Contraseñas encriptadas con bcrypt a través de Supabase Auth
- Sesiones Flask firmadas con HMAC-SHA1
- Row Level Security (RLS) en todas las tablas de Supabase
- Políticas de acceso por rol (cliente / profesional)
- Validación de entradas en backend (`validators.py`)

---

## Instalación y ejecución local

### Requisitos previos
- Python 3.10 o superior
- Cuenta en [Supabase](https://supabase.com) (gratuita)

### Pasos

**1. Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/click-a-construir.git
cd click-a-construir/cac_v2
```

**2. Instalar dependencias**
```bash
pip install -r requirements.txt
```

**3. Configurar variables de entorno**

Copia el archivo de ejemplo y llena tus datos:
```bash
cp .env.example .env
```

Edita `.env`:
```
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=tu-anon-public-key
FLASK_SECRET=una-clave-secreta-larga
```

**4. Configurar Supabase**

En tu proyecto de Supabase:
- Ve a **SQL Editor** y ejecuta el archivo `supabase_schema.sql` para crear las tablas, triggers y políticas RLS
- Ve a **Storage** y crea dos buckets públicos: `avatars` y `project-images`
- Ve a **Authentication → URL Configuration** y agrega `http://localhost:5000` como Site URL y `http://localhost:5000/**` en Redirect URLs

**5. Ejecutar la aplicación**
```bash
python app.py
```

Abre [http://localhost:5000](http://localhost:5000) en tu navegador.

---

## Pruebas unitarias

El proyecto incluye 55 pruebas unitarias en `test_validators.py` que cubren las validaciones de todos los campos del sistema.

```bash
python test_validators.py
```

Resultado esperado:
```
=======================================================
  RESULTADO: 55/55 pruebas pasaron
  ✅ Todas las pruebas pasaron exitosamente
=======================================================
```

### Cobertura de pruebas

| Módulo | Casos probados |
|---|---|
| `validate_name` | Nombre válido, sin apellido, con números, con símbolos, muy corto, muy largo |
| `validate_email` | Correo válido, sin @, sin dominio, con espacios, doble @ |
| `validate_password` | Contraseña válida, sin mayúscula, sin minúscula, sin número, sin símbolo, muy corta |
| `validate_passwords_match` | Iguales, diferentes, diferencia por mayúscula |
| `validate_role` | Cliente, profesional, rol inválido, vacío |
| `validate_register` | Registro completo válido e inválido con distintas combinaciones |
| `validate_project` | Proyecto válido, nombre corto, presupuesto cero/negativo/texto, fechas invertidas |

---

## Base de datos

El esquema completo se encuentra en `supabase_schema.sql` e incluye 8 tablas:

| Tabla | Descripción |
|---|---|
| `users` | Perfiles de clientes y profesionales |
| `projects` | Proyectos publicados con estado y progreso |
| `tasks` | Tareas de cada proyecto |
| `project_updates` | Avances publicados por el profesional |
| `project_images` | Imágenes adjuntas a cada proyecto |
| `messages` | Mensajes entre usuarios con soporte de adjuntos |
| `reviews` | Calificaciones y comentarios de clientes a profesionales |
| `quotations` | Cotizaciones enviadas por profesionales |

---

## Modo de desarrollo sin Supabase

Si no tienes las credenciales de Supabase configuradas, la app detecta automáticamente que no hay conexión y opera con datos de ejemplo en memoria. Esto permite desarrollar y probar sin necesidad de internet o base de datos.

---

## Autores
ELKIN YAMITH ALMONACID LOPEZ
BRAYAN DAVID CUITIVA UMBARILA
JUAN CAMILO GARCIA QUEVEDO
BRAYAN YAIR MENDEZ RODRIGUEZ

Proyecto desarrollado para la asignatura Ingeniería de Software II  
Universidad de Cundinamarca — 2026
