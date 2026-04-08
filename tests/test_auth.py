from app.services.auth_service import AuthService


# 🔐 PRUEBA 1: LOGIN CORRECTO
def test_login_correcto():
    auth = AuthService()
    auth.registrar_usuario("Romel", "romel@mail.com", "1234")

    usuario = auth.login("romel@mail.com", "1234")

    assert usuario is not None


# ❌ PRUEBA 2: LOGIN INCORRECTO
def test_login_incorrecto():
    auth = AuthService()
    auth.registrar_usuario("Romel", "romel@mail.com", "1234")

    usuario = auth.login("romel@mail.com", "9999")

    assert usuario is None


# 🧾 PRUEBA 3: LOGS
def test_logs():
    auth = AuthService()
    auth.registrar_usuario("Romel", "romel@mail.com", "1234")

    auth.login("romel@mail.com", "1234")

    with open("logs.txt", "r") as f:
        contenido = f.read()

    assert "ACCESO EXITOSO" in contenido
