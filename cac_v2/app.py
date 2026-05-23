"""
Click a Construir — Flask App v3
Usa db.py como capa de acceso a datos (Supabase o memoria)
"""
from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
from datetime import datetime
import os, uuid
from dotenv import load_dotenv
load_dotenv()

import db          # capa de datos
import validators  # validaciones de entrada

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "cac_dev_secret_2024")

UPLOAD_FOLDER = os.path.join(app.static_folder, "img", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED = {"png", "jpg", "jpeg", "gif", "webp"}

# ─── Helpers ─────────────────────────────────────────────────────────────────
def allowed(f):
    return "." in f and f.rsplit(".", 1)[1].lower() in ALLOWED

def save_file(file, is_avatar=False):
    """Guarda localmente si no hay Supabase, o sube a Storage."""
    if not file or not file.filename or not allowed(file.filename):
        return None
    bucket = "avatars" if is_avatar else "project-images"
    if db.USE_SUPABASE:
        data = file.read()
        return db.upload_image_to_storage(data, file.filename, bucket)
    ext   = file.filename.rsplit(".", 1)[1].lower()
    fname = f"{uuid.uuid4().hex}.{ext}"
    file.save(os.path.join(UPLOAD_FOLDER, fname))
    return url_for("static", filename=f"img/uploads/{fname}")

def login_required(f):
    @wraps(f)
    def deco(*a, **kw):
        if "user" not in session:
            return redirect(url_for("login"))
        return f(*a, **kw)
    return deco

def format_cop(n):
    try: return "$ {:,.0f}".format(int(n)).replace(",", ".")
    except: return str(n)

app.jinja_env.filters["format_cop"] = format_cop

def _sess():
    return session["user"]

# ─── AUTH ─────────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return redirect(url_for("dashboard") if "user" in session else url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        pw    = request.form.get("password", "")

        if db.USE_SUPABASE:
            # Supabase Auth
            try:
                resp = db.supabase.auth.sign_in_with_password({"email": email, "password": pw})
                uid  = resp.user.id
                user = db.get_user_by_id(uid)
                if user:
                    session["user"] = {"id": uid, "email": email,
                                       "name": user["name"], "role": user["role"],
                                       "avatar": user.get("avatar_url")}
                    return redirect(url_for("dashboard"))
            except Exception:
                flash("Correo o contraseña incorrectos.", "error")
        else:
            user = db.get_user_by_email(email)
            if user and user.get("password") == pw:
                session["user"] = {"id": user["id"], "email": email,
                                   "name": user["name"], "role": user["role"],
                                   "avatar": user.get("avatar_url")}
                return redirect(url_for("dashboard"))
            flash("Correo o contraseña incorrectos.", "error")

    return render_template("login.html", tab=request.args.get("tab", "login"))

@app.route("/register", methods=["POST"])
def register():
    name    = request.form.get("name", "").strip()
    email   = request.form.get("email", "").strip().lower()
    pw      = request.form.get("password", "")
    confirm = request.form.get("confirm_password", "")
    role    = request.form.get("role", "cliente")

    # ── Validar todos los campos ──────────────────────────────────────
    errors = validators.validate_register(name, email, pw, confirm, role)
    if errors:
        for e in errors:
            flash(e, "error")
        return redirect(url_for("login") + "?tab=register")

    if db.USE_SUPABASE:
        try:
            resp = db.supabase.auth.sign_up({
                "email": email,
                "password": pw,
                "options": {"data": {"name": name, "role": role}}
            })

            # Si email confirmations está ON, resp.user existe pero no hay sesión activa
            if resp.user is None:
                flash("Te enviamos un correo de confirmación. Confírmalo y luego inicia sesión.", "success")
                return redirect(url_for("login"))

            uid = resp.user.id

            # El trigger handle_new_user() ya insertó la fila en public.users.
            # Solo actualizamos nombre y rol por si el trigger tardó.
            try:
                db.supabase.table("users").update({
                    "name": name, "role": role, "email": email
                }).eq("id", uid).execute()
            except Exception:
                pass  # No es crítico si falla, el trigger ya creó la fila

            session["user"] = {"id": uid, "email": email, "name": name, "role": role, "avatar": None}
            return redirect(url_for("dashboard"))

        except Exception as e:
            msg = str(e)
            if "already registered" in msg or "already exists" in msg or "User already registered" in msg:
                flash("Este correo ya está registrado.", "error")
            elif "rate limit" in msg.lower():
                flash("Demasiados intentos. Espera unos minutos e intenta de nuevo.", "error")
            else:
                flash(f"Error al registrarse: {msg}", "error")
            return redirect(url_for("login") + "?tab=register")
    else:
        if db.get_user_by_email(email):
            flash("Este correo ya está registrado.", "error")
            return redirect(url_for("login") + "?tab=register")
        user = db.create_user(email, name, role, pw)
        session["user"] = {"id": user["id"], "email": email, "name": name, "role": role, "avatar": None}
        return redirect(url_for("dashboard"))

@app.route("/logout")
def logout():
    if db.USE_SUPABASE:
        try: db.supabase.auth.sign_out()
        except: pass
    session.clear()
    return redirect(url_for("login"))

@app.route("/confirm")
def confirm_email():
    """
    Supabase redirige aquí tras confirmar el correo.
    El token viene en el fragmento (#) de la URL — el navegador
    lo procesa con JS y lo manda al backend como parámetros normales.
    """
    return render_template("confirm.html")

@app.route("/confirm/callback", methods=["POST"])
def confirm_callback():
    """Recibe el token de Supabase desde el JS y crea la sesión Flask."""
    access_token  = request.form.get("access_token")
    refresh_token = request.form.get("refresh_token")
    if not access_token:
        flash("El enlace de confirmación no es válido o ya expiró.", "error")
        return redirect(url_for("login"))
    if db.USE_SUPABASE:
        try:
            resp = db.supabase.auth.set_session(access_token, refresh_token)
            user_auth = resp.user
            if user_auth:
                uid   = user_auth.id
                email = user_auth.email
                # Buscar perfil en public.users
                profile = db.get_user_by_id(uid)
                name  = profile["name"]  if profile else (user_auth.user_metadata.get("name") or email)
                role  = profile["role"]  if profile else (user_auth.user_metadata.get("role") or "cliente")
                avatar = profile.get("avatar_url") if profile else None
                session["user"] = {"id": uid, "email": email,
                                   "name": name, "role": role, "avatar": avatar}
                flash("¡Correo confirmado! Bienvenido a Click a Construir.", "success")
                return redirect(url_for("dashboard"))
        except Exception as e:
            flash(f"Error al confirmar: {e}", "error")
    return redirect(url_for("login"))

@app.route("/reset-password")
def reset_password_page():
    """Página donde el usuario escribe su nueva contraseña tras el email de recuperación."""
    return render_template("reset_password.html")

@app.route("/reset-password/update", methods=["POST"])
def reset_password_update():
    access_token = request.form.get("access_token")
    new_password = request.form.get("new_password", "")
    confirm_pw   = request.form.get("confirm_password", "")

    errors = validators.validate_password(new_password)
    errors += validators.validate_passwords_match(new_password, confirm_pw)
    if errors:
        for e in errors:
            flash(e, "error")
        return redirect(url_for("reset_password_page"))

    if db.USE_SUPABASE and access_token:
        try:
            db.supabase.auth.set_session(access_token, "")
            db.supabase.auth.update_user({"password": new_password})
            flash("Contraseña actualizada exitosamente. Inicia sesión.", "success")
            return redirect(url_for("login"))
        except Exception as e:
            flash(f"Error al actualizar: {e}", "error")
    return redirect(url_for("reset_password_page"))

@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        errors = validators.validate_email(email)
        if errors:
            flash(errors[0], "error")
            return redirect(url_for("forgot_password"))
        if db.USE_SUPABASE:
            try:
                db.supabase.auth.reset_password_email(
                    email,
                    {"redirect_to": "http://localhost:5000/reset-password"}
                )
            except Exception:
                pass  # No revelar si el correo existe o no
        flash("Si ese correo está registrado, recibirás un enlace para recuperar tu contraseña.", "success")
        return redirect(url_for("login"))
    return render_template("forgot_password.html")

@app.route("/dashboard")
@login_required
def dashboard():
    return redirect(url_for("pro_inicio") if _sess()["role"] == "profesional" else url_for("cli_inicio"))

# ─── CLIENTE ──────────────────────────────────────────────────────────────────
@app.route("/cliente/inicio")
@login_required
def cli_inicio():
    q          = request.args.get("q", "").lower()
    specialty  = request.args.get("specialty", "")
    city       = request.args.get("city", "")
    min_rating = request.args.get("min_rating", "")

    profs = db.get_all_professionals()

    # Normalizar campos de Supabase para que el template funcione
    def normalize_prof(p):
        p = dict(p)
        p.setdefault("rating",   p.get("rating_avg") or 0)
        p.setdefault("reviews",  p.get("reviews_count") or 0)
        p.setdefault("location", p.get("city") or "—")
        p.setdefault("avatar",   p.get("avatar_url"))
        parts = p.get("name","").split()
        p["initials"] = (parts[0][0]+parts[-1][0]).upper() if len(parts)>=2 else p.get("name","?")[:2].upper()
        return p

    profs = [normalize_prof(p) for p in profs]
    if q:          profs = [p for p in profs if q in p["name"].lower() or q in (p.get("specialty") or "").lower()]
    if specialty:  profs = [p for p in profs if (p.get("specialty") or "").lower() == specialty.lower()]
    if city:       profs = [p for p in profs if city.lower() in (p.get("location") or "").lower()]
    if min_rating: profs = [p for p in profs if (p.get("rating") or 0) >= float(min_rating)]

    specialties = sorted(set(p.get("specialty","") for p in profs if p.get("specialty")))
    unread = db.get_unread_count(_sess()["id"])
    return render_template("cliente/inicio.html",
        professionals=profs, q=q, specialty=specialty, city=city,
        min_rating=min_rating, specialties=specialties,
        user=_sess(), active_menu="inicio", unread=unread)

@app.route("/cliente/profesional/<prof_id>")
@login_required
def cli_perfil_profesional(prof_id):
    prof      = db.get_user_by_id(prof_id)
    if not prof:
        flash("Profesional no encontrado.", "error")
        return redirect(url_for("cli_inicio"))

    # Normalizar campos: Supabase usa rating_avg/reviews_count/city/avatar_url
    # el template espera rating/reviews/location/initials/avatar
    prof = dict(prof)  # copia para no modificar el original
    prof.setdefault("rating",    prof.get("rating_avg") or 0)
    prof.setdefault("reviews",   prof.get("reviews_count") or 0)
    prof.setdefault("location",  prof.get("city") or "—")
    prof.setdefault("avatar",    prof.get("avatar_url"))
    prof.setdefault("phone",     prof.get("phone") or "—")
    prof.setdefault("completed_projects", 0)
    prof.setdefault("bio",       prof.get("bio") or "Sin descripción.")
    prof.setdefault("specialty", prof.get("specialty") or "—")
    # Iniciales desde el nombre
    parts = prof.get("name", "").split()
    prof["initials"] = (parts[0][0] + parts[-1][0]).upper() if len(parts) >= 2 else prof.get("name","?")[:2].upper()

    reviews   = db.get_reviews_for_professional(prof_id)
    completed = db.get_projects_by_professional(prof_id, status_filter="Completado")
    # Contar proyectos completados reales
    prof["completed_projects"] = len(completed)

    unread    = db.get_unread_count(_sess()["id"])
    return render_template("cliente/perfil_profesional.html",
        prof=prof, reviews=reviews, completed=completed,
        user=_sess(), active_menu="inicio", unread=unread)

@app.route("/cliente/proyectos")
@login_required
def cli_proyectos():
    uid      = _sess()["id"]
    q        = request.args.get("q", "")
    status_f = request.args.get("status", "")
    projs    = db.get_projects_by_client(uid, status_filter=status_f, search=q)
    unread   = db.get_unread_count(uid)
    return render_template("cliente/proyectos.html",
        projects=projs, q=q, status_f=status_f,
        user=_sess(), active_menu="proyectos", unread=unread)

@app.route("/cliente/proyecto/<proj_id>")
@login_required
def cli_proyecto_detalle(proj_id):
    proj = db.get_project_by_id(proj_id)
    if not proj: return redirect(url_for("cli_proyectos"))
    unread = db.get_unread_count(_sess()["id"])
    return render_template("cliente/proyecto_detalle.html",
        proj=proj, user=_sess(), active_menu="proyectos", unread=unread)

@app.route("/cliente/proyectos/crear", methods=["POST"])
@login_required
def cli_crear_proyecto():
    uid = _sess()["id"]
    name       = request.form.get("name", "")
    location   = request.form.get("location", "")
    budget     = request.form.get("budget", "0").replace(".", "").replace(",", "").strip() or "0"
    start_date = request.form.get("start_date", "")
    end_date   = request.form.get("end_date", "")

    errors = validators.validate_project(name, location, budget, start_date, end_date)
    if errors:
        for e in errors:
            flash(e, "error")
        return redirect(url_for("cli_proyectos"))

    images = []
    for f in request.files.getlist("images"):
        url = save_file(f)
        if url: images.append(url)

    db.create_project({
        "name":        name,
        "client_id":   uid,
        "client_name": _sess()["name"],
        "location":    location,
        "budget":      int(budget),
        "status":      "Pendiente",
        "description": request.form.get("description", ""),
        "start_date":  start_date,
        "end_date":    end_date,
        "category":    request.form.get("category", ""),
        "size":        request.form.get("size", ""),
        "progress":    0,
        "images":      images,
        "created_at":  datetime.now().strftime("%Y-%m-%d"),
    })
    flash("Proyecto publicado exitosamente.", "success")
    return redirect(url_for("cli_proyectos"))

@app.route("/cliente/mensajes")
@login_required
def cli_mensajes():
    uid   = _sess()["id"]
    convs = db.get_conversations(uid)
    open_id   = request.args.get("with")
    open_conv = next((c for c in convs if c["other_id"] == open_id), None) if open_id else None

    # Si se llega con ?with=ID pero no hay conversación previa,
    # crear una conversación vacía para poder escribir el primer mensaje
    if open_id and not open_conv:
        other = db.get_user_by_id(open_id)
        if other:
            parts = other.get("name","").split()
            initials = (parts[0][0]+parts[-1][0]).upper() if len(parts)>=2 else other.get("name","?")[:2].upper()
            open_conv = {
                "other_id":       open_id,
                "other_name":     other.get("name",""),
                "other_initials": initials,
                "other_avatar":   other.get("avatar_url"),
                "messages":       [],
                "unread":         0,
                "last_message":   "",
                "last_time":      "",
            }

    if open_conv and open_id and open_conv["messages"]:
        db.mark_messages_read(open_id, uid)
    unread = db.get_unread_count(uid)
    return render_template("cliente/mensajes.html",
        convs=convs, open_conv=open_conv, open_id=open_id,
        user=_sess(), active_menu="mensajes", unread=unread)

@app.route("/cliente/mensajes/enviar", methods=["POST"])
@login_required
def cli_enviar_mensaje():
    u     = _sess()
    to_id = request.form.get("to_id")
    text  = request.form.get("text", "").strip()

    attachment_url  = None
    attachment_type = None
    adjunto = request.files.get("adjunto")
    if adjunto and adjunto.filename:
        ext = adjunto.filename.rsplit(".", 1)[-1].lower() if "." in adjunto.filename else ""
        if ext in {"png", "jpg", "jpeg", "gif", "webp"}:
            attachment_type = "image"
        elif ext == "pdf":
            attachment_type = "pdf"
        else:
            attachment_type = "file"
        attachment_url = save_file(adjunto)

    if (text or attachment_url) and to_id:
        to_u = db.get_user_by_id(to_id)
        if to_u:
            db.send_message(u["id"], u["name"], to_id, to_u["name"],
                            text or "", attachment_url, attachment_type)
    return redirect(url_for("cli_mensajes", **{"with": to_id}))

@app.route("/cliente/perfil", methods=["GET", "POST"])
@login_required
def cli_perfil():
    uid = _sess()["id"]
    if request.method == "POST":
        data = {
            "name":  request.form.get("name", _sess()["name"]),
            "phone": request.form.get("phone", ""),
            "city":  request.form.get("city", ""),
            "bio":   request.form.get("bio", ""),
        }
        av = request.files.get("avatar")
        if av and av.filename:
            url = save_file(av, is_avatar=True)
            if url:
                data["avatar_url"] = url
        db.update_user_profile(uid, data)
        # Refrescar sesión completa desde la BD
        updated = db.get_user_by_id(uid)
        if updated:
            session["user"]["name"]   = updated.get("name", data["name"])
            session["user"]["avatar"] = updated.get("avatar_url")
        else:
            session["user"]["name"]   = data["name"]
            session["user"]["avatar"] = data.get("avatar_url", session["user"].get("avatar"))
        session.modified = True
        flash("Perfil actualizado.", "success")
        return redirect(url_for("cli_perfil"))

    user_data = db.get_user_by_id(uid)
    my_projs  = db.get_projects_by_client(uid)
    unread    = db.get_unread_count(uid)
    return render_template("cliente/perfil.html",
        user=_sess(), user_data=user_data,
        my_projects=my_projs, active_menu="perfil", unread=unread)

# ─── PROFESIONAL ──────────────────────────────────────────────────────────────
@app.route("/profesional/inicio")
@login_required
def pro_inicio():
    q          = request.args.get("q", "")
    category   = request.args.get("category", "")
    city       = request.args.get("city", "")
    max_budget = request.args.get("max_budget", "")

    avail      = db.get_available_projects(
        category=category, city=city,
        max_budget=int(max_budget) if max_budget else None,
        search=q
    )
    # Categorías para filtro
    all_projs  = db.get_available_projects()
    categories = sorted(set(p.get("category","") for p in all_projs if p.get("category")))
    unread     = db.get_unread_count(_sess()["id"])
    return render_template("profesional/inicio.html",
        projects=avail, q=q, category=category, city=city, max_budget=max_budget,
        categories=categories, user=_sess(), active_menu="inicio", unread=unread)

@app.route("/profesional/proyecto-disponible/<proj_id>")
@login_required
def pro_proyecto_detalle(proj_id):
    proj  = db.get_project_by_id(proj_id)
    if not proj: return redirect(url_for("pro_inicio"))
    unread = db.get_unread_count(_sess()["id"])
    return render_template("profesional/proyecto_disponible.html",
        proj=proj, user=_sess(), active_menu="inicio", unread=unread)

@app.route("/profesional/proyectos")
@login_required
def pro_proyectos():
    uid      = _sess()["id"]
    q        = request.args.get("q", "")
    status_f = request.args.get("status", "")
    mine     = db.get_projects_by_professional(uid, status_filter=status_f, search=q)
    unread   = db.get_unread_count(uid)
    return render_template("profesional/proyectos.html",
        projects=mine, q=q, status_f=status_f,
        user=_sess(), active_menu="proyectos", unread=unread)

@app.route("/profesional/proyecto/<proj_id>", methods=["GET", "POST"])
@login_required
def pro_proyecto_gestion(proj_id):
    proj = db.get_project_by_id(proj_id)
    if not proj: return redirect(url_for("pro_proyectos"))

    if request.method == "POST":
        action = request.form.get("action")

        if action == "add_update":
            text = request.form.get("update_text", "").strip()
            if text:
                imgs = []
                for f in request.files.getlist("update_images"):
                    url = save_file(f)
                    if url: imgs.append(url)
                db.add_update(proj_id, _sess()["id"], _sess()["name"], text, imgs)

        elif action == "toggle_task":
            db.toggle_task(request.form.get("task_id"))

        elif action == "add_task":
            txt = request.form.get("task_text", "").strip()
            if txt: db.add_task(proj_id, txt)

        elif action == "update_status":
            db.update_project(proj_id, {"status": request.form.get("status")})

        elif action == "add_project_image":
            for f in request.files.getlist("project_images"):
                url = save_file(f)
                if url: db.add_project_image(proj_id, url)

        db.recalculate_progress(proj_id)
        return redirect(url_for("pro_proyecto_gestion", proj_id=proj_id))

    # Recargar con datos frescos
    proj   = db.get_project_by_id(proj_id)
    tasks  = db.get_tasks(proj_id)
    updates = db.get_updates(proj_id)
    proj["tasks"]   = tasks
    proj["updates"] = updates
    unread = db.get_unread_count(_sess()["id"])
    return render_template("profesional/proyecto_gestion.html",
        proj=proj, user=_sess(), active_menu="proyectos", unread=unread)

@app.route("/profesional/mensajes")
@login_required
def pro_mensajes():
    uid   = _sess()["id"]
    convs = db.get_conversations(uid)
    open_id   = request.args.get("with")
    open_conv = next((c for c in convs if c["other_id"] == open_id), None) if open_id else None

    # Si se llega con ?with=ID pero no hay conversación previa,
    # crear una conversación vacía para poder escribir el primer mensaje
    if open_id and not open_conv:
        other = db.get_user_by_id(open_id)
        if other:
            parts = other.get("name","").split()
            initials = (parts[0][0]+parts[-1][0]).upper() if len(parts)>=2 else other.get("name","?")[:2].upper()
            open_conv = {
                "other_id":       open_id,
                "other_name":     other.get("name",""),
                "other_initials": initials,
                "other_avatar":   other.get("avatar_url"),
                "messages":       [],
                "unread":         0,
                "last_message":   "",
                "last_time":      "",
            }

    if open_conv and open_id and open_conv["messages"]:
        db.mark_messages_read(open_id, uid)
    unread = db.get_unread_count(uid)
    return render_template("profesional/mensajes.html",
        convs=convs, open_conv=open_conv, open_id=open_id,
        user=_sess(), active_menu="mensajes", unread=unread)

@app.route("/profesional/mensajes/enviar", methods=["POST"])
@login_required
def pro_enviar_mensaje():
    u     = _sess()
    to_id = request.form.get("to_id")
    text  = request.form.get("text", "").strip()

    attachment_url  = None
    attachment_type = None
    adjunto = request.files.get("adjunto")
    if adjunto and adjunto.filename:
        ext = adjunto.filename.rsplit(".", 1)[-1].lower() if "." in adjunto.filename else ""
        if ext in {"png", "jpg", "jpeg", "gif", "webp"}:
            attachment_type = "image"
        elif ext == "pdf":
            attachment_type = "pdf"
        else:
            attachment_type = "file"
        attachment_url = save_file(adjunto)

    if (text or attachment_url) and to_id:
        to_u = db.get_user_by_id(to_id)
        if to_u:
            db.send_message(u["id"], u["name"], to_id, to_u["name"],
                            text or "", attachment_url, attachment_type)
    return redirect(url_for("pro_mensajes", **{"with": to_id}))

@app.route("/profesional/perfil", methods=["GET", "POST"])
@login_required
def pro_perfil():
    uid = _sess()["id"]
    if request.method == "POST":
        data = {
            "name":      request.form.get("name", _sess()["name"]),
            "phone":     request.form.get("phone", ""),
            "city":      request.form.get("city", ""),
            "bio":       request.form.get("bio", ""),
            "specialty": request.form.get("specialty", ""),
            "instagram": request.form.get("instagram", "").strip(),
            "facebook":  request.form.get("facebook", "").strip(),
            "whatsapp":  request.form.get("whatsapp", "").strip(),
            "website":   request.form.get("website", "").strip(),
        }
        av = request.files.get("avatar")
        if av and av.filename:
            url = save_file(av, is_avatar=True)
            if url:
                data["avatar_url"] = url
        db.update_user_profile(uid, data)
        # Refrescar sesión completa desde la BD
        updated = db.get_user_by_id(uid)
        if updated:
            session["user"]["name"]   = updated.get("name", data["name"])
            session["user"]["avatar"] = updated.get("avatar_url")
        else:
            session["user"]["name"]   = data["name"]
            session["user"]["avatar"] = data.get("avatar_url", session["user"].get("avatar"))
        session.modified = True
        flash("Perfil actualizado.", "success")
        return redirect(url_for("pro_perfil"))

    user_data  = db.get_user_by_id(uid)
    my_reviews = db.get_reviews_for_professional(uid)
    completed  = db.get_projects_by_professional(uid, status_filter="Completado")
    unread     = db.get_unread_count(uid)
    return render_template("profesional/perfil.html",
        user=_sess(), user_data=user_data,
        my_reviews=my_reviews, completed_projects=completed,
        active_menu="perfil", unread=unread)

# ─── Reseñas ──────────────────────────────────────────────────────────────────
@app.route("/cliente/calificar/<prof_id>", methods=["POST"])
@login_required
def cli_calificar(prof_id):
    rating  = float(request.form.get("rating", 5))
    comment = request.form.get("comment", "").strip()
    proj_id = request.form.get("project_id", "")
    db.create_review(prof_id, _sess()["id"], _sess()["name"], proj_id, rating, comment)
    flash("¡Gracias por tu calificación!", "success")
    return redirect(url_for("cli_perfil_profesional", prof_id=prof_id))

if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "true").lower() == "true"
    app.run(debug=debug)
