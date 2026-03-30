# Click a Construir — Flask App

Versión funcional en Python/Flask del diseño Figma "Design minimal SaaS UI".

## Estructura

```
flask_app/
├── app.py                  ← Servidor Flask (rutas, lógica)
├── requirements.txt
├── templates/
│   ├── base.html           ← Layout base (Jinja2)
│   ├── login.html          ← Página de login / registro
│   └── dashboard.html      ← Dashboard principal
└── static/
    ├── css/main.css        ← Estilos completos
    ├── js/main.js          ← Tabs, modal, role-selector
    └── img/
        ├── logo_login.png
        └── logo_dashboard.png
```

## Cómo correr

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Iniciar el servidor
python app.py

# 3. Abrir en el navegador
http://127.0.0.1:5000
```

## Credenciales de prueba

| Correo               | Contraseña |
|----------------------|------------|
| laura@example.com    | 1234       |

## Páginas disponibles

| Ruta              | Descripción                      |
|-------------------|----------------------------------|
| `/login`          | Login + registro con tabs        |
| `/dashboard`      | Inicio: listado de profesionales |
| `/proyectos`      | Mis proyectos con estados        |
| `/mensajes`       | Bandeja de mensajes (placeholder)|
| `/perfil`         | Perfil del usuario               |
| `/logout`         | Cierre de sesión                 |

## Próximos pasos sugeridos

- Conectar base de datos (SQLite + SQLAlchemy)
- Hash de contraseñas (bcrypt)
- Autenticación por token (Flask-Login)
- API REST para el frontend
