"""
validators.py — Validaciones de entrada para Click a Construir
Usadas tanto en app.py (backend) como en las pruebas unitarias.
"""
import re


# ─── Constantes ───────────────────────────────────────────────────────────────
NAME_MIN       = 3
NAME_MAX       = 60
PASSWORD_MIN   = 8
PASSWORD_MAX   = 72   # límite de bcrypt


# ─── Nombre ───────────────────────────────────────────────────────────────────
# Solo letras (incluye tildes/ñ), espacios y guiones. Mínimo dos palabras.
_NAME_RE = re.compile(r"^[A-Za-zÁÉÍÓÚáéíóúÑñÜüÀàÈè\s\-']+$")

def validate_name(name: str) -> list[str]:
    """Retorna lista de errores (vacía = válido)."""
    errors = []
    name = name.strip()
    if not name:
        errors.append("El nombre es obligatorio.")
        return errors
    if len(name) < NAME_MIN:
        errors.append(f"El nombre debe tener al menos {NAME_MIN} caracteres.")
    if len(name) > NAME_MAX:
        errors.append(f"El nombre no puede superar {NAME_MAX} caracteres.")
    if not _NAME_RE.match(name):
        errors.append("El nombre solo puede contener letras, espacios y guiones. No se permiten números ni símbolos.")
    parts = [p for p in name.split() if p]
    if len(parts) < 2:
        errors.append("Ingresa tu nombre completo (nombre y apellido).")
    return errors


# ─── Email ────────────────────────────────────────────────────────────────────
_EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]{2,}$")

def validate_email(email: str) -> list[str]:
    errors = []
    email = email.strip()
    if not email:
        errors.append("El correo es obligatorio.")
        return errors
    if not _EMAIL_RE.match(email):
        errors.append("El correo electrónico no tiene un formato válido.")
    if len(email) > 254:
        errors.append("El correo es demasiado largo.")
    return errors


# ─── Contraseña ───────────────────────────────────────────────────────────────
def validate_password(password: str) -> list[str]:
    """
    Reglas:
    - Mínimo 8 caracteres
    - Al menos una letra mayúscula
    - Al menos una letra minúscula
    - Al menos un número
    - Al menos un símbolo especial (!@#$%^&*...)
    """
    errors = []
    if not password:
        errors.append("La contraseña es obligatoria.")
        return errors
    if len(password) < PASSWORD_MIN:
        errors.append(f"La contraseña debe tener al menos {PASSWORD_MIN} caracteres.")
    if len(password) > PASSWORD_MAX:
        errors.append(f"La contraseña no puede superar {PASSWORD_MAX} caracteres.")
    if not re.search(r"[A-Z]", password):
        errors.append("La contraseña debe tener al menos una letra mayúscula.")
    if not re.search(r"[a-z]", password):
        errors.append("La contraseña debe tener al menos una letra minúscula.")
    if not re.search(r"\d", password):
        errors.append("La contraseña debe tener al menos un número.")
    if not re.search(r"[!@#$%^&*()\-_=+\[\]{};:'\",.<>?/\\|`~]", password):
        errors.append("La contraseña debe tener al menos un símbolo especial (ej: @, #, !, $).")
    return errors


def validate_passwords_match(password: str, confirm: str) -> list[str]:
    if password != confirm:
        return ["Las contraseñas no coinciden."]
    return []


# ─── Rol ──────────────────────────────────────────────────────────────────────
def validate_role(role: str) -> list[str]:
    if role not in ("cliente", "profesional"):
        return ["El tipo de cuenta no es válido."]
    return []


# ─── Función principal de registro ───────────────────────────────────────────
def validate_register(name: str, email: str, password: str,
                       confirm: str, role: str) -> list[str]:
    """Valida todos los campos de registro. Retorna lista de errores."""
    errors = []
    errors.extend(validate_name(name))
    errors.extend(validate_email(email))
    errors.extend(validate_password(password))
    errors.extend(validate_passwords_match(password, confirm))
    errors.extend(validate_role(role))
    return errors


# ─── Validaciones de proyecto ─────────────────────────────────────────────────
def validate_project(name: str, location: str, budget: str,
                     start_date: str, end_date: str) -> list[str]:
    errors = []
    if not name or len(name.strip()) < 3:
        errors.append("El nombre del proyecto debe tener al menos 3 caracteres.")
    if not location or len(location.strip()) < 3:
        errors.append("La ubicación es obligatoria.")
    try:
        b = int(budget)
        if b <= 0:
            errors.append("El presupuesto debe ser mayor a cero.")
        if b > 10_000_000_000:
            errors.append("El presupuesto parece demasiado alto. Verifica el valor.")
    except (ValueError, TypeError):
        errors.append("El presupuesto debe ser un número válido.")
    if start_date and end_date and start_date > end_date:
        errors.append("La fecha de inicio no puede ser posterior a la fecha de fin.")
    return errors
