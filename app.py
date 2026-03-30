from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from functools import wraps

app = Flask(__name__)
app.secret_key = "click_a_construir_secret_key_2024"

# ---------------------------------------------------------------------------
# Datos de ejemplo (en producción esto vendría de una base de datos)
# ---------------------------------------------------------------------------
USERS = {
    "laura@example.com": {"password": "1234", "name": "Laura Rodríguez", "role": "cliente"},
}

PROFESSIONALS = [
    {"id": 1, "name": "Carlos Martínez", "specialty": "Electricista",  "location": "Bogotá Centro", "rating": 4.8, "reviews": 24, "initials": "CM"},
    {"id": 2, "name": "Ana García",       "specialty": "Fontanera",     "location": "Chapinero",     "rating": 4.9, "reviews": 31, "initials": "AG"},
    {"id": 3, "name": "Miguel Hernández", "specialty": "Carpintero",    "location": "Usaquén",       "rating": 4.7, "reviews": 18, "initials": "MH"},
    {"id": 4, "name": "Isabel Fernández", "specialty": "Pintora",       "location": "Candelaria",    "rating": 5.0, "reviews": 42, "initials": "IF"},
    {"id": 5, "name": "David López",      "specialty": "Albañil",       "location": "Kennedy",       "rating": 4.6, "reviews": 15, "initials": "DL"},
    {"id": 6, "name": "Carmen Ruiz",      "specialty": "Decoradora",    "location": "Suba",          "rating": 4.8, "reviews": 27, "initials": "CR"},
]

PROJECTS = [
    {"id": 1, "name": "Renovación de cocina",     "location": "Bogotá Centro", "budget": 15000000, "status": "En progreso"},
    {"id": 2, "name": "Reparación de baño",       "location": "Chapinero",     "budget": 8500000,  "status": "Pendiente"},
    {"id": 3, "name": "Instalación eléctrica",    "location": "Usaquén",       "budget": 12000000, "status": "Completado"},
    {"id": 4, "name": "Pintura de apartamento",   "location": "Candelaria",    "budget": 6000000,  "status": "En progreso"},
    {"id": 5, "name": "Construcción de patio",    "location": "Kennedy",       "budget": 25000000, "status": "Pendiente"},
    {"id": 6, "name": "Remodelación de sala",     "location": "Suba",          "budget": 18000000, "status": "En progreso"},
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated

def format_cop(amount):
    return "$ {:,.0f}".format(amount).replace(",", ".")

app.jinja_env.filters["format_cop"] = format_cop

# ---------------------------------------------------------------------------
# Rutas
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    if "user" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email    = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        user = USERS.get(email)
        if user and user["password"] == password:
            session["user"] = {"email": email, "name": user["name"], "role": user["role"]}
            return redirect(url_for("dashboard"))
        flash("Correo o contraseña incorrectos.", "error")
    return render_template("login.html")

@app.route("/register", methods=["POST"])
def register():
    name             = request.form.get("name", "").strip()
    email            = request.form.get("email", "").strip()
    password         = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")
    role             = request.form.get("role", "cliente")

    if password != confirm_password:
        flash("Las contraseñas no coinciden.", "error")
        return redirect(url_for("login") + "?tab=register")

    if email in USERS:
        flash("Este correo ya está registrado.", "error")
        return redirect(url_for("login") + "?tab=register")

    USERS[email] = {"password": password, "name": name, "role": role}
    session["user"] = {"email": email, "name": name, "role": role}
    return redirect(url_for("dashboard"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/dashboard")
@login_required
def dashboard():
    query = request.args.get("q", "").lower()
    filtered = [p for p in PROFESSIONALS if query in p["name"].lower() or query in p["specialty"].lower()] if query else PROFESSIONALS
    return render_template("dashboard.html", professionals=filtered, active_menu="inicio",
                           user=session["user"], query=query)

@app.route("/proyectos")
@login_required
def proyectos():
    return render_template("dashboard.html", projects=PROJECTS, active_menu="proyectos",
                           user=session["user"])

@app.route("/proyectos/crear", methods=["POST"])
@login_required
def crear_proyecto():
    nuevo = {
        "id":       len(PROJECTS) + 1,
        "name":     request.form.get("name", ""),
        "location": request.form.get("location", ""),
        "budget":   int(request.form.get("budget", 0)),
        "status":   "Pendiente",
    }
    PROJECTS.append(nuevo)
    flash("Proyecto creado exitosamente.", "success")
    return redirect(url_for("proyectos"))

@app.route("/mensajes")
@login_required
def mensajes():
    return render_template("dashboard.html", active_menu="mensajes", user=session["user"])

@app.route("/perfil")
@login_required
def perfil():
    return render_template("dashboard.html", active_menu="perfil", user=session["user"])

# ---------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
