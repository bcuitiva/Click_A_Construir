"""
db.py — Capa de acceso a datos para Click a Construir
Usa Supabase si las variables de entorno están configuradas.
Si no, usa datos en memoria para desarrollo local.
"""
import os
from datetime import datetime

# ─── Intentar conectar Supabase ──────────────────────────────────────────────
try:
    from supabase import create_client, Client
    from dotenv import load_dotenv
    load_dotenv()

    _url = os.environ.get("SUPABASE_URL", "")
    _key = os.environ.get("SUPABASE_KEY", "")
    USE_SUPABASE = bool(_url and _key and not _url.startswith("https://TU-PROYECTO"))
    if USE_SUPABASE:
        supabase: Client = create_client(_url, _key)
        print("✅ Conectado a Supabase")
    else:
        print("⚠️  Usando datos en memoria (configura .env para usar Supabase)")
except Exception as e:
    USE_SUPABASE = False
    print(f"⚠️  Supabase no disponible: {e}")

# ─── Datos en memoria (desarrollo) ───────────────────────────────────────────
_USERS = {
    "laura@example.com":  {"id":"u1","password":"1234","name":"Laura Rodríguez","role":"cliente","phone":"314 555 0101","city":"Bogotá","bio":"Propietaria buscando profesionales confiables.","avatar_url":None,"rating_avg":None,"reviews_count":0},
    "carlos@example.com": {"id":"u2","password":"1234","name":"Carlos Martínez","role":"profesional","phone":"314 555 0202","city":"Bogotá","bio":"Electricista con 10 años de experiencia. Certificado RETIE.","specialty":"Electricista","avatar_url":None,"rating_avg":4.8,"reviews_count":24,"instagram":"","facebook":"","whatsapp":"","website":""},
    "ana@example.com":    {"id":"u3","password":"1234","name":"Ana García","role":"profesional","phone":"314 555 0303","city":"Bogotá","bio":"Fontanera certificada, especialista en remodelaciones.","specialty":"Fontanera","avatar_url":None,"rating_avg":4.9,"reviews_count":31},
    "miguel@example.com": {"id":"u4","password":"1234","name":"Miguel Hernández","role":"profesional","phone":"314 555 0404","city":"Bogotá","bio":"Carpintero con experiencia en muebles a medida.","specialty":"Carpintero","avatar_url":None,"rating_avg":4.7,"reviews_count":18},
    "isabel@example.com": {"id":"u5","password":"1234","name":"Isabel Fernández","role":"profesional","phone":"314 555 0505","city":"Bogotá","bio":"Pintora profesional, acabados de alta calidad.","specialty":"Pintora","avatar_url":None,"rating_avg":5.0,"reviews_count":42},
    "pedro@example.com":  {"id":"u6","password":"1234","name":"Pedro Martín","role":"cliente","phone":"314 555 0606","city":"Medellín","bio":"Cliente frecuente de servicios de remodelación.","avatar_url":None,"rating_avg":None,"reviews_count":0},
}
_PROJECTS = [
    {"id":"p1","name":"Renovación de cocina","client_id":"u1","client_name":"Laura Rodríguez","professional_id":"u2","professional_name":"Carlos Martínez","location":"Bogotá Centro","budget":15000000,"status":"En progreso","description":"Renovación completa de cocina 12m².","start_date":"2026-04-15","end_date":"2026-05-30","category":"Remodelación","size":"12m²","progress":60,"images":[],"created_at":"2026-04-01"},
    {"id":"p2","name":"Reparación de baño","client_id":"u6","client_name":"Pedro Martín","professional_id":None,"professional_name":None,"location":"Chapinero","budget":8500000,"status":"Pendiente","description":"Renovación completa de baño principal 6m².","start_date":"2026-04-01","end_date":"2026-04-20","category":"Reparación","size":"6m²","progress":0,"images":[],"created_at":"2026-03-25"},
    {"id":"p3","name":"Instalación eléctrica completa","client_id":"u1","client_name":"Laura Rodríguez","professional_id":"u2","professional_name":"Carlos Martínez","location":"Usaquén","budget":12000000,"status":"Completado","description":"Revisión y actualización del sistema eléctrico 80m².","start_date":"2026-03-01","end_date":"2026-03-20","category":"Instalación eléctrica","size":"80m²","progress":100,"images":[],"created_at":"2026-02-20"},
]
_TASKS = [
    {"id":"t1","project_id":"p1","text":"Demolición de muebles antiguos","done":True,"completed_at":"2026-04-16"},
    {"id":"t2","project_id":"p1","text":"Instalación de tuberías nuevas","done":True,"completed_at":"2026-04-20"},
    {"id":"t3","project_id":"p1","text":"Instalación de muebles","done":False,"completed_at":None},
    {"id":"t4","project_id":"p1","text":"Colocación de suelo","done":False,"completed_at":None},
    {"id":"t5","project_id":"p1","text":"Pintura y acabados finales","done":False,"completed_at":None},
    {"id":"t6","project_id":"p2","text":"Demolición de azulejos","done":False,"completed_at":None},
    {"id":"t7","project_id":"p2","text":"Impermeabilización","done":False,"completed_at":None},
    {"id":"t8","project_id":"p2","text":"Instalación de azulejos nuevos","done":False,"completed_at":None},
    {"id":"t9","project_id":"p3","text":"Revisión del cuadro eléctrico","done":True,"completed_at":"2026-03-02"},
    {"id":"t10","project_id":"p3","text":"Cambio de cableado","done":True,"completed_at":"2026-03-10"},
    {"id":"t11","project_id":"p3","text":"Instalación enchufes","done":True,"completed_at":"2026-03-15"},
    {"id":"t12","project_id":"p3","text":"Certificación eléctrica","done":True,"completed_at":"2026-03-20"},
]
_UPDATES = [
    {"id":"upd1","project_id":"p1","author_id":"u2","author_name":"Carlos Martínez","text":"Se completó la demolición de los muebles antiguos.","images":[],"created_at":"2026-04-16"},
    {"id":"upd2","project_id":"p1","author_id":"u2","author_name":"Carlos Martínez","text":"Tuberías nuevas instaladas y probadas. Sin fugas detectadas.","images":[],"created_at":"2026-04-20"},
    {"id":"upd3","project_id":"p3","author_id":"u2","author_name":"Carlos Martínez","text":"Revisión completa. 3 puntos con cableado deteriorado.","images":[],"created_at":"2026-03-02"},
    {"id":"upd4","project_id":"p3","author_id":"u2","author_name":"Carlos Martínez","text":"Cableado reemplazado. Proyecto finalizado.","images":[],"created_at":"2026-03-20"},
]
_MESSAGES = [
    {"id":"m1","from_id":"u1","from_name":"Laura Rodríguez","to_id":"u2","to_name":"Carlos Martínez","text":"Hola Carlos, ¿podrías revisar mi instalación eléctrica?","read":True,"created_at":"2026-04-01 09:15"},
    {"id":"m2","from_id":"u2","from_name":"Carlos Martínez","to_id":"u1","to_name":"Laura Rodríguez","text":"¡Hola Laura! Claro, ¿qué día te viene bien?","read":True,"created_at":"2026-04-01 09:30"},
    {"id":"m3","from_id":"u1","from_name":"Laura Rodríguez","to_id":"u2","to_name":"Carlos Martínez","text":"El jueves perfecto, a las 10am.","read":True,"created_at":"2026-04-01 09:45"},
    {"id":"m4","from_id":"u3","from_name":"Ana García","to_id":"u1","to_name":"Laura Rodríguez","text":"Buenos días Laura, vi tu proyecto de baño. ¿Le puedo ayudar?","read":False,"created_at":"2026-04-02 10:00"},
]
_REVIEWS = [
    {"id":"r1","prof_id":"u2","client_name":"Laura Rodríguez","rating":5,"comment":"Excelente trabajo, muy puntual y profesional.","date":"2026-03-10"},
    {"id":"r2","prof_id":"u2","client_name":"Pedro Martín","rating":4.5,"comment":"Buen trabajo, quedé satisfecho.","date":"2026-02-20"},
    {"id":"r3","prof_id":"u3","client_name":"Laura Rodríguez","rating":5,"comment":"Resolvió el problema rápidamente.","date":"2026-03-15"},
]

# ─── Helpers internos ─────────────────────────────────────────────────────────
def _now():
    return datetime.now().strftime("%Y-%m-%d %H:%M")

def _today():
    return datetime.now().strftime("%Y-%m-%d")

def _uid():
    import uuid
    return uuid.uuid4().hex[:12]

# ═════════════════════════════════════════════════════════════════════════════
#  USERS
# ═════════════════════════════════════════════════════════════════════════════
def get_user_by_email(email: str):
    if USE_SUPABASE:
        r = supabase.table("users").select("*").eq("email", email).single().execute()
        return r.data
    return _USERS.get(email)

def get_user_by_id(uid: str):
    if USE_SUPABASE:
        r = supabase.table("users").select("*").eq("id", uid).single().execute()
        return r.data
    return next((u for u in _USERS.values() if u["id"] == uid), None)

def create_user(email, name, role, password_hash):
    """En Supabase, la contraseña la maneja Supabase Auth — aquí solo guardamos el perfil."""
    if USE_SUPABASE:
        r = supabase.table("users").insert({
            "email": email, "name": name, "role": role
        }).execute()
        return r.data[0] if r.data else None
    import uuid
    uid = "u" + str(len(_USERS) + 1)
    _USERS[email] = {"id": uid, "password": password_hash, "name": name, "role": role,
                     "phone": "", "city": "", "bio": "", "avatar_url": None,
                     "rating_avg": None, "reviews_count": 0,
                     "specialty": "" if role == "profesional" else None}
    return _USERS[email]

def update_user_profile(uid, data: dict):
    if USE_SUPABASE:
        r = supabase.table("users").update(data).eq("id", uid).execute()
        return r.data[0] if r.data else None
    for u in _USERS.values():
        if u["id"] == uid:
            u.update(data)
            return u
    return None

def get_all_professionals():
    if USE_SUPABASE:
        r = supabase.table("users").select("*").eq("role", "profesional").execute()
        return r.data or []
    profs = []
    for u in _USERS.values():
        if u.get("role") == "profesional":
            profs.append({**u, "initials": u["name"][:2].upper(),
                          "rating": u.get("rating_avg"), "reviews": u.get("reviews_count", 0),
                          "location": u.get("city", ""), "completed_projects": 0})
    return profs

# ═════════════════════════════════════════════════════════════════════════════
#  PROJECTS
# ═════════════════════════════════════════════════════════════════════════════
def get_projects_by_client(client_id, status_filter="", search=""):
    if USE_SUPABASE:
        q = supabase.table("projects").select(
            "*, tasks(*), project_updates(*), project_images(*)"
        ).eq("client_id", client_id)
        if status_filter:
            q = q.eq("status", status_filter)
        r = q.order("created_at", desc=True).execute()
        projs = r.data or []
        if search:
            projs = [p for p in projs if search.lower() in p["name"].lower()]
        return projs
    projs = [p for p in _PROJECTS if p["client_id"] == client_id]
    if status_filter: projs = [p for p in projs if p["status"] == status_filter]
    if search:        projs = [p for p in projs if search.lower() in p["name"].lower()]
    return projs

def get_projects_by_professional(prof_id, status_filter="", search=""):
    if USE_SUPABASE:
        q = supabase.table("projects").select(
            "*, tasks(*), project_updates(*), project_images(*)"
        ).eq("professional_id", prof_id)
        if status_filter:
            q = q.eq("status", status_filter)
        r = q.order("created_at", desc=True).execute()
        projs = r.data or []
        if search:
            projs = [p for p in projs if search.lower() in p["name"].lower()]
        return projs
    projs = [p for p in _PROJECTS if p.get("professional_id") == prof_id]
    if status_filter: projs = [p for p in projs if p["status"] == status_filter]
    if search:        projs = [p for p in projs if search.lower() in p["name"].lower()]
    return projs

def get_available_projects(category="", city="", max_budget=None, search=""):
    """Proyectos sin profesional asignado."""
    if USE_SUPABASE:
        q = supabase.table("projects").select(
            "*, tasks(*), project_images(*)"
        ).is_("professional_id", "null")
        if category:   q = q.eq("category", category)
        if max_budget: q = q.lte("budget", max_budget)
        r = q.order("created_at", desc=True).execute()
        projs = r.data or []
        if city:   projs = [p for p in projs if city.lower() in (p.get("location","")).lower()]
        if search: projs = [p for p in projs if search.lower() in p["name"].lower()]
        return projs
    projs = [p for p in _PROJECTS if not p.get("professional_id")]
    if category:   projs = [p for p in projs if p.get("category","").lower() == category.lower()]
    if city:       projs = [p for p in projs if city.lower() in p.get("location","").lower()]
    if max_budget: projs = [p for p in projs if p["budget"] <= int(max_budget)]
    if search:     projs = [p for p in projs if search.lower() in p["name"].lower()]
    return projs

def get_project_by_id(proj_id):
    if USE_SUPABASE:
        r = supabase.table("projects").select(
            "*, tasks(*), project_updates(*), project_images(*)"
        ).eq("id", proj_id).single().execute()
        proj = r.data
        if proj:
            # Normalizar imágenes desde project_images
            proj["images"] = [i["url"] for i in (proj.get("project_images") or [])]
            # Normalizar updates con sus imágenes
            for upd in (proj.get("project_updates") or []):
                if isinstance(upd.get("images"), list):
                    pass  # ya es lista de URLs
                else:
                    upd["images"] = []
            proj["updates"] = proj.pop("project_updates", [])
        return proj
    proj = next((p for p in _PROJECTS if p["id"] == proj_id), None)
    if proj:
        proj["tasks"]   = [t for t in _TASKS   if t["project_id"] == proj_id]
        proj["updates"] = [u for u in _UPDATES if u["project_id"] == proj_id]
    return proj

def create_project(data: dict):
    if USE_SUPABASE:
        images = data.pop("images", [])
        r = supabase.table("projects").insert(data).execute()
        proj = r.data[0] if r.data else None
        if proj and images:
            for url in images:
                supabase.table("project_images").insert(
                    {"project_id": proj["id"], "url": url}
                ).execute()
        return proj
    import uuid
    pid = "p" + str(len(_PROJECTS) + 1)
    data["id"] = pid
    _PROJECTS.append(data)
    return data

def update_project(proj_id, data: dict):
    if USE_SUPABASE:
        r = supabase.table("projects").update(data).eq("id", proj_id).execute()
        return r.data[0] if r.data else None
    proj = next((p for p in _PROJECTS if p["id"] == proj_id), None)
    if proj:
        proj.update(data)
    return proj

def add_project_image(proj_id, url):
    if USE_SUPABASE:
        supabase.table("project_images").insert(
            {"project_id": proj_id, "url": url}
        ).execute()
    else:
        proj = next((p for p in _PROJECTS if p["id"] == proj_id), None)
        if proj:
            proj.setdefault("images", []).append(url)

def recalculate_progress(proj_id):
    if USE_SUPABASE:
        r = supabase.table("tasks").select("done").eq("project_id", proj_id).execute()
        tasks = r.data or []
    else:
        tasks = [t for t in _TASKS if t["project_id"] == proj_id]
    total = len(tasks)
    done  = sum(1 for t in tasks if t["done"])
    progress = int(done / total * 100) if total else 0
    update_project(proj_id, {"progress": progress})
    return progress

# ═════════════════════════════════════════════════════════════════════════════
#  TASKS
# ═════════════════════════════════════════════════════════════════════════════
def get_tasks(proj_id):
    if USE_SUPABASE:
        r = supabase.table("tasks").select("*").eq("project_id", proj_id)\
            .order("created_at").execute()
        return r.data or []
    return [t for t in _TASKS if t["project_id"] == proj_id]

def add_task(proj_id, text):
    if USE_SUPABASE:
        r = supabase.table("tasks").insert(
            {"project_id": proj_id, "text": text, "done": False}
        ).execute()
        return r.data[0] if r.data else None
    task = {"id": "t" + _uid(), "project_id": proj_id, "text": text,
            "done": False, "completed_at": None}
    _TASKS.append(task)
    return task

def toggle_task(task_id):
    if USE_SUPABASE:
        r = supabase.table("tasks").select("done").eq("id", task_id).single().execute()
        current = r.data["done"] if r.data else False
        new_done = not current
        supabase.table("tasks").update({
            "done": new_done,
            "completed_at": _today() if new_done else None
        }).eq("id", task_id).execute()
        return new_done
    task = next((t for t in _TASKS if t["id"] == task_id), None)
    if task:
        task["done"] = not task["done"]
        task["completed_at"] = _today() if task["done"] else None
    return task["done"] if task else False

# ═════════════════════════════════════════════════════════════════════════════
#  PROJECT UPDATES (Avances)
# ═════════════════════════════════════════════════════════════════════════════
def get_updates(proj_id):
    if USE_SUPABASE:
        r = supabase.table("project_updates").select("*, users(name, avatar_url)")\
            .eq("project_id", proj_id).order("created_at").execute()
        updates = r.data or []
        for u in updates:
            u["author_name"] = (u.get("users") or {}).get("name", "")
            if not isinstance(u.get("images"), list):
                u["images"] = []
        return updates
    return [u for u in _UPDATES if u["project_id"] == proj_id]

def add_update(proj_id, author_id, author_name, text, image_urls: list):
    if USE_SUPABASE:
        r = supabase.table("project_updates").insert({
            "project_id": proj_id,
            "author_id":  author_id,
            "text":       text,
            "images":     image_urls
        }).execute()
        return r.data[0] if r.data else None
    upd = {"id": "upd" + _uid(), "project_id": proj_id,
           "author_id": author_id, "author_name": author_name,
           "text": text, "images": image_urls, "created_at": _today()}
    _UPDATES.append(upd)
    return upd

# ═════════════════════════════════════════════════════════════════════════════
#  MESSAGES
# ═════════════════════════════════════════════════════════════════════════════
def get_conversations(user_id: str):
    if USE_SUPABASE:
        r = supabase.table("messages").select(
            "*, from:from_id(id,name,avatar_url), to:to_id(id,name,avatar_url)"
        ).or_(f"from_id.eq.{user_id},to_id.eq.{user_id}")\
         .order("created_at").execute()
        msgs = r.data or []
    else:
        msgs = [m for m in _MESSAGES if m["from_id"] == user_id or m["to_id"] == user_id]

    conv_map = {}
    for msg in msgs:
        if USE_SUPABASE:
            other = msg["to"] if msg["from_id"] == user_id else msg["from"]
            other_id   = other["id"]
            other_name = other["name"]
            other_av   = other.get("avatar_url")
            other_init = other_name[:2].upper()
        else:
            if msg["from_id"] == user_id:
                other_id, other_name = msg["to_id"], msg["to_name"]
            else:
                other_id, other_name = msg["from_id"], msg["from_name"]
            other_u  = get_user_by_id(other_id)
            other_av = other_u.get("avatar_url") if other_u else None
            other_init = other_name[:2].upper()

        if other_id not in conv_map:
            conv_map[other_id] = {
                "other_id": other_id, "other_name": other_name,
                "other_initials": other_init, "other_avatar": other_av,
                "messages": [], "unread": 0
            }
        conv_map[other_id]["messages"].append(msg)
        is_unread = not msg["read"] and (
            msg["to_id"] == user_id if not USE_SUPABASE
            else msg["to_id"] == user_id
        )
        if is_unread:
            conv_map[other_id]["unread"] += 1

    convs = list(conv_map.values())
    for c in convs:
        last = c["messages"][-1]
        c["last_message"] = last["text"]
        c["last_time"]    = last.get("created_at", "")
    convs.sort(key=lambda x: x["last_time"], reverse=True)
    return convs

def get_unread_count(user_id: str):
    if USE_SUPABASE:
        r = supabase.table("messages").select("id", count="exact")\
            .eq("to_id", user_id).eq("read", False).execute()
        return r.count or 0
    return sum(1 for m in _MESSAGES if m["to_id"] == user_id and not m["read"])

def send_message(from_id, from_name, to_id, to_name, text,
                 attachment_url=None, attachment_type=None):
    if USE_SUPABASE:
        supabase.table("messages").insert({
            "from_id":         from_id,
            "to_id":           to_id,
            "text":            text,
            "read":            False,
            "attachment_url":  attachment_url,
            "attachment_type": attachment_type,
        }).execute()
    else:
        _MESSAGES.append({
            "id":              "m" + _uid(),
            "from_id":         from_id,
            "from_name":       from_name,
            "to_id":           to_id,
            "to_name":         to_name,
            "text":            text,
            "read":            False,
            "attachment_url":  attachment_url,
            "attachment_type": attachment_type,
            "created_at":      _now()
        })

def mark_messages_read(from_id, to_id):
    if USE_SUPABASE:
        supabase.table("messages").update({"read": True})\
            .eq("from_id", from_id).eq("to_id", to_id).execute()
    else:
        for m in _MESSAGES:
            if m["from_id"] == from_id and m["to_id"] == to_id:
                m["read"] = True

# ═════════════════════════════════════════════════════════════════════════════
#  REVIEWS
# ═════════════════════════════════════════════════════════════════════════════
def get_reviews_for_professional(prof_id):
    if USE_SUPABASE:
        r = supabase.table("reviews").select(
            "*, client:client_id(name, avatar_url)"
        ).eq("professional_id", prof_id).order("created_at", desc=True).execute()
        reviews = r.data or []
        for rev in reviews:
            rev["client_name"] = (rev.get("client") or {}).get("name", "")
            rev["client_avatar"] = (rev.get("client") or {}).get("avatar_url")
        return reviews
    return [r for r in _REVIEWS if r["prof_id"] == prof_id]

def create_review(professional_id, client_id, client_name, project_id, rating, comment):
    if USE_SUPABASE:
        supabase.table("reviews").insert({
            "professional_id": professional_id,
            "client_id": client_id,
            "project_id": project_id,
            "rating": rating,
            "comment": comment
        }).execute()
        # Recalcular promedio
        r = supabase.table("reviews").select("rating")\
            .eq("professional_id", professional_id).execute()
        ratings = [x["rating"] for x in (r.data or [])]
        avg = round(sum(ratings) / len(ratings), 1) if ratings else 0
        supabase.table("users").update({
            "rating_avg": avg, "reviews_count": len(ratings)
        }).eq("id", professional_id).execute()
    else:
        _REVIEWS.append({
            "id": "r" + _uid(), "prof_id": professional_id,
            "client_name": client_name, "rating": rating,
            "comment": comment, "date": _today()
        })

# ═════════════════════════════════════════════════════════════════════════════
#  STORAGE — subida de imágenes
# ═════════════════════════════════════════════════════════════════════════════
def upload_image_to_storage(file_bytes: bytes, filename: str, bucket: str = "project-images") -> str:
    """Sube imagen a Supabase Storage y retorna la URL pública."""
    if USE_SUPABASE:
        path = f"{_uid()}/{filename}"
        supabase.storage.from_(bucket).upload(
            path, file_bytes, {"content-type": "image/jpeg"}
        )
        url = supabase.storage.from_(bucket).get_public_url(path)
        return url
    return None  # En local se usa save_upload() de app.py
