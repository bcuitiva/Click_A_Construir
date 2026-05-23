# Click a Construir — v2

Plataforma web para conectar clientes con profesionales de construcción y remodelación.

---

## Cómo correr localmente

```bash
cd flask_app_v2
pip install -r requirements.txt
python app.py
# Abrir: http://127.0.0.1:5000
```

## Usuarios de prueba

| Correo               | Contraseña | Rol          |
|----------------------|------------|--------------|
| laura@example.com    | 1234       | Cliente      |
| carlos@example.com   | 1234       | Profesional  |
| ana@example.com      | 1234       | Profesional  |

---

## Estructura del proyecto

```
flask_app_v2/
├── app.py
├── requirements.txt
├── templates/
│   ├── base.html
│   ├── macros.html
│   ├── login.html
│   ├── cliente/
│   │   ├── inicio.html          ← Carrusel de profesionales
│   │   ├── perfil_profesional.html
│   │   ├── proyectos.html
│   │   ├── proyecto_detalle.html ← Progreso + tareas + avances
│   │   ├── mensajes.html
│   │   └── perfil.html
│   └── profesional/
│       ├── inicio.html           ← Proyectos disponibles con filtros
│       ├── proyecto_disponible.html
│       ├── proyectos.html
│       ├── proyecto_gestion.html ← Tareas + avances + línea de tiempo
│       ├── mensajes.html
│       └── perfil.html
└── static/
    ├── css/main.css
    ├── js/main.js
    └── img/
```

---

## Base de datos Supabase — Tablas y atributos

### `users`
| Columna          | Tipo        | Descripción                        |
|------------------|-------------|------------------------------------|
| id               | uuid PK     | Generado por Supabase Auth         |
| email            | text unique |                                    |
| name             | text        |                                    |
| role             | text        | 'cliente' o 'profesional'          |
| phone            | text        |                                    |
| city             | text        |                                    |
| bio              | text        |                                    |
| specialty        | text        | Solo profesionales                 |
| avatar_url       | text        | URL de Supabase Storage            |
| rating_avg       | numeric     | Promedio calculado                 |
| reviews_count    | int         |                                    |
| created_at       | timestamptz | default now()                      |

### `projects`
| Columna          | Tipo        | Descripción                        |
|------------------|-------------|------------------------------------|
| id               | uuid PK     |                                    |
| name             | text        |                                    |
| description      | text        |                                    |
| client_id        | uuid FK → users |                               |
| professional_id  | uuid FK → users | nullable                     |
| location         | text        |                                    |
| budget           | bigint      | En pesos COP                       |
| status           | text        | 'Pendiente','En progreso','Completado' |
| category         | text        |                                    |
| size             | text        | Ej: "30m²"                         |
| progress         | int         | 0-100                              |
| start_date       | date        |                                    |
| end_date         | date        |                                    |
| created_at       | timestamptz |                                    |

### `tasks`
| Columna          | Tipo        | Descripción                        |
|------------------|-------------|------------------------------------|
| id               | uuid PK     |                                    |
| project_id       | uuid FK → projects |                           |
| text             | text        |                                    |
| done             | boolean     | default false                      |
| completed_at     | timestamptz | nullable                           |
| created_at       | timestamptz |                                    |

### `project_updates`
| Columna          | Tipo        | Descripción                        |
|------------------|-------------|------------------------------------|
| id               | uuid PK     |                                    |
| project_id       | uuid FK → projects |                           |
| author_id        | uuid FK → users |                               |
| text             | text        |                                    |
| created_at       | timestamptz |                                    |

### `messages`
| Columna          | Tipo        | Descripción                        |
|------------------|-------------|------------------------------------|
| id               | uuid PK     |                                    |
| from_id          | uuid FK → users |                               |
| to_id            | uuid FK → users |                               |
| text             | text        |                                    |
| read             | boolean     | default false                      |
| created_at       | timestamptz |                                    |

### `reviews`
| Columna          | Tipo        | Descripción                        |
|------------------|-------------|------------------------------------|
| id               | uuid PK     |                                    |
| professional_id  | uuid FK → users |                               |
| client_id        | uuid FK → users |                               |
| project_id       | uuid FK → projects |                           |
| rating           | numeric     | 0.0 – 5.0                          |
| comment          | text        |                                    |
| created_at       | timestamptz |                                    |

### `quotations`
| Columna          | Tipo        | Descripción                        |
|------------------|-------------|------------------------------------|
| id               | uuid PK     |                                    |
| project_id       | uuid FK → projects |                           |
| professional_id  | uuid FK → users |                               |
| file_url         | text        | Supabase Storage                   |
| message          | text        | nullable                           |
| status           | text        | 'enviada','aceptada','rechazada'    |
| created_at       | timestamptz |                                    |

---

## Migración a Supabase

1. Crear proyecto en https://supabase.com
2. Ejecutar el SQL de las tablas en el SQL Editor
3. Instalar: `pip install supabase`
4. En `app.py` reemplazar los diccionarios en memoria por:
   ```python
   from supabase import create_client
   supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
   # Ejemplo: supabase.table('users').select('*').execute()
   ```
5. Usar Supabase Auth para el manejo de sesiones y contraseñas
