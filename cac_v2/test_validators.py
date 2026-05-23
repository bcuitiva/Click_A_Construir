"""
test_validators.py — Pruebas unitarias para Click a Construir
Ejecutar con:  python -m pytest test_validators.py -v
O sin pytest:  python test_validators.py
"""
import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from validators import (
    validate_name,
    validate_email,
    validate_password,
    validate_passwords_match,
    validate_role,
    validate_register,
    validate_project,
)


# ══════════════════════════════════════════════════════════════════════════════
#  NOMBRE
# ══════════════════════════════════════════════════════════════════════════════
class TestValidateName(unittest.TestCase):

    # ── Casos válidos ──────────────────────────────────────────────────────
    def test_nombre_valido_simple(self):
        self.assertEqual(validate_name("Juan Pérez"), [])

    def test_nombre_valido_con_tilde(self):
        self.assertEqual(validate_name("María José García"), [])

    def test_nombre_valido_con_enye(self):
        self.assertEqual(validate_name("Nuño Ordóñez"), [])

    def test_nombre_valido_con_guion(self):
        self.assertEqual(validate_name("Ana-María López"), [])

    def test_nombre_valido_con_apostrofe(self):
        self.assertEqual(validate_name("O'Brien Martínez"), [])

    # ── Casos inválidos ────────────────────────────────────────────────────
    def test_nombre_vacio(self):
        errores = validate_name("")
        self.assertTrue(len(errores) > 0)

    def test_nombre_solo_espacios(self):
        errores = validate_name("   ")
        self.assertTrue(len(errores) > 0)

    def test_nombre_muy_corto(self):
        errores = validate_name("Jo")
        self.assertIn(True, ["al menos" in e for e in errores])

    def test_nombre_con_numeros(self):
        errores = validate_name("Juan123 Pérez")
        self.assertTrue(len(errores) > 0)

    def test_nombre_con_simbolos(self):
        errores = validate_name("Juan@# Pérez")
        self.assertTrue(len(errores) > 0)

    def test_nombre_sin_apellido(self):
        """Solo una palabra — falta el apellido."""
        errores = validate_name("Juan")
        self.assertTrue(any("completo" in e for e in errores))

    def test_nombre_muy_largo(self):
        errores = validate_name("A" * 61 + " B" * 5)
        self.assertTrue(len(errores) > 0)


# ══════════════════════════════════════════════════════════════════════════════
#  EMAIL
# ══════════════════════════════════════════════════════════════════════════════
class TestValidateEmail(unittest.TestCase):

    # ── Casos válidos ──────────────────────────────────────────────────────
    def test_email_valido(self):
        self.assertEqual(validate_email("usuario@gmail.com"), [])

    def test_email_valido_con_punto(self):
        self.assertEqual(validate_email("nombre.apellido@empresa.co"), [])

    def test_email_valido_con_guion(self):
        self.assertEqual(validate_email("mi-correo@dominio.org"), [])

    def test_email_valido_con_plus(self):
        self.assertEqual(validate_email("user+tag@mail.com"), [])

    # ── Casos inválidos ────────────────────────────────────────────────────
    def test_email_vacio(self):
        self.assertTrue(len(validate_email("")) > 0)

    def test_email_sin_arroba(self):
        self.assertTrue(len(validate_email("usuariogmail.com")) > 0)

    def test_email_sin_dominio(self):
        self.assertTrue(len(validate_email("usuario@")) > 0)

    def test_email_sin_extension(self):
        self.assertTrue(len(validate_email("usuario@dominio")) > 0)

    def test_email_con_espacios(self):
        self.assertTrue(len(validate_email("usua rio@gmail.com")) > 0)

    def test_email_doble_arroba(self):
        self.assertTrue(len(validate_email("user@@gmail.com")) > 0)


# ══════════════════════════════════════════════════════════════════════════════
#  CONTRASEÑA
# ══════════════════════════════════════════════════════════════════════════════
class TestValidatePassword(unittest.TestCase):

    # ── Casos válidos ──────────────────────────────────────────────────────
    def test_password_valida_basica(self):
        self.assertEqual(validate_password("Segura1@"), [])

    def test_password_valida_larga(self):
        self.assertEqual(validate_password("MiContraseña123!"), [])

    def test_password_valida_con_varios_simbolos(self):
        self.assertEqual(validate_password("P@ss#2024word"), [])

    # ── Casos inválidos ────────────────────────────────────────────────────
    def test_password_vacia(self):
        self.assertTrue(len(validate_password("")) > 0)

    def test_password_muy_corta(self):
        errores = validate_password("Ab1@")
        self.assertTrue(any("8" in e for e in errores))

    def test_password_sin_mayuscula(self):
        errores = validate_password("segura1@clave")
        self.assertTrue(any("mayúscula" in e for e in errores))

    def test_password_sin_minuscula(self):
        errores = validate_password("SEGURA1@CLAVE")
        self.assertTrue(any("minúscula" in e for e in errores))

    def test_password_sin_numero(self):
        errores = validate_password("Segura@Clave")
        self.assertTrue(any("número" in e for e in errores))

    def test_password_sin_simbolo(self):
        errores = validate_password("Segura1Clave")
        self.assertTrue(any("símbolo" in e for e in errores))

    def test_password_solo_numeros(self):
        errores = validate_password("12345678")
        self.assertTrue(len(errores) >= 3)

    def test_password_comun_sin_cumplir_reglas(self):
        """'password' es una contraseña típica y débil."""
        errores = validate_password("password")
        self.assertTrue(len(errores) > 0)


# ══════════════════════════════════════════════════════════════════════════════
#  COINCIDENCIA DE CONTRASEÑAS
# ══════════════════════════════════════════════════════════════════════════════
class TestPasswordsMatch(unittest.TestCase):

    def test_passwords_iguales(self):
        self.assertEqual(validate_passwords_match("Segura1@", "Segura1@"), [])

    def test_passwords_diferentes(self):
        errores = validate_passwords_match("Segura1@", "Diferente1@")
        self.assertTrue(len(errores) > 0)

    def test_passwords_diferencia_mayuscula(self):
        errores = validate_passwords_match("Segura1@", "segura1@")
        self.assertTrue(len(errores) > 0)


# ══════════════════════════════════════════════════════════════════════════════
#  ROL
# ══════════════════════════════════════════════════════════════════════════════
class TestValidateRole(unittest.TestCase):

    def test_rol_cliente(self):
        self.assertEqual(validate_role("cliente"), [])

    def test_rol_profesional(self):
        self.assertEqual(validate_role("profesional"), [])

    def test_rol_invalido(self):
        self.assertTrue(len(validate_role("admin")) > 0)

    def test_rol_vacio(self):
        self.assertTrue(len(validate_role("")) > 0)

    def test_rol_con_mayusculas(self):
        """El rol debe llegar en minúsculas desde el frontend."""
        self.assertTrue(len(validate_role("Cliente")) > 0)


# ══════════════════════════════════════════════════════════════════════════════
#  REGISTRO COMPLETO
# ══════════════════════════════════════════════════════════════════════════════
class TestValidateRegister(unittest.TestCase):

    def _datos_validos(self):
        return {
            "name":     "Laura Rodríguez",
            "email":    "laura@example.com",
            "password": "Segura1@",
            "confirm":  "Segura1@",
            "role":     "cliente",
        }

    def test_registro_valido(self):
        d = self._datos_validos()
        self.assertEqual(validate_register(**d), [])

    def test_registro_nombre_invalido(self):
        d = self._datos_validos()
        d["name"] = "Laura123"
        self.assertTrue(len(validate_register(**d)) > 0)

    def test_registro_email_invalido(self):
        d = self._datos_validos()
        d["email"] = "no-es-un-correo"
        self.assertTrue(len(validate_register(**d)) > 0)

    def test_registro_password_debil(self):
        d = self._datos_validos()
        d["password"] = "1234"
        d["confirm"]  = "1234"
        errores = validate_register(**d)
        self.assertTrue(len(errores) >= 3)

    def test_registro_passwords_no_coinciden(self):
        d = self._datos_validos()
        d["confirm"] = "OtraClave1@"
        self.assertTrue(len(validate_register(**d)) > 0)

    def test_registro_rol_invalido(self):
        d = self._datos_validos()
        d["role"] = "superadmin"
        self.assertTrue(len(validate_register(**d)) > 0)

    def test_registro_todos_campos_vacios(self):
        errores = validate_register("", "", "", "", "")
        self.assertTrue(len(errores) >= 4)


# ══════════════════════════════════════════════════════════════════════════════
#  PROYECTO
# ══════════════════════════════════════════════════════════════════════════════
class TestValidateProject(unittest.TestCase):

    def test_proyecto_valido(self):
        errores = validate_project(
            name="Renovación de cocina",
            location="Bogotá Centro",
            budget="15000000",
            start_date="2026-05-01",
            end_date="2026-06-30",
        )
        self.assertEqual(errores, [])

    def test_nombre_muy_corto(self):
        errores = validate_project("Ab", "Bogotá", "500000", "2026-05-01", "2026-06-01")
        self.assertTrue(len(errores) > 0)

    def test_presupuesto_cero(self):
        errores = validate_project("Remodelación", "Bogotá", "0", "2026-05-01", "2026-06-01")
        self.assertTrue(any("mayor" in e for e in errores))

    def test_presupuesto_negativo(self):
        errores = validate_project("Remodelación", "Bogotá", "-500", "2026-05-01", "2026-06-01")
        self.assertTrue(len(errores) > 0)

    def test_presupuesto_texto(self):
        errores = validate_project("Remodelación", "Bogotá", "abc", "2026-05-01", "2026-06-01")
        self.assertTrue(any("número" in e for e in errores))

    def test_fecha_inicio_posterior_a_fin(self):
        errores = validate_project(
            "Remodelación", "Bogotá", "5000000",
            start_date="2026-08-01",
            end_date="2026-06-01",
        )
        self.assertTrue(any("inicio" in e for e in errores))

    def test_ubicacion_vacia(self):
        errores = validate_project("Remodelación", "", "5000000", "2026-05-01", "2026-06-01")
        self.assertTrue(len(errores) > 0)


# ══════════════════════════════════════════════════════════════════════════════
#  RUNNER
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    loader  = unittest.TestLoader()
    suite   = unittest.TestSuite()

    clases = [
        TestValidateName,
        TestValidateEmail,
        TestValidatePassword,
        TestPasswordsMatch,
        TestValidateRole,
        TestValidateRegister,
        TestValidateProject,
    ]
    for cls in clases:
        suite.addTests(loader.loadTestsFromTestCase(cls))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    total   = result.testsRun
    passed  = total - len(result.failures) - len(result.errors)
    print(f"\n{'='*55}")
    print(f"  RESULTADO: {passed}/{total} pruebas pasaron")
    if result.failures or result.errors:
        print(f"  ❌ Fallidas: {len(result.failures)}  |  Errores: {len(result.errors)}")
    else:
        print("  ✅ Todas las pruebas pasaron exitosamente")
    print(f"{'='*55}")

    sys.exit(0 if result.wasSuccessful() else 1)
