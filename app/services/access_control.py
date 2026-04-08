def tiene_permiso(usuario, accion):
    permisos = {
        "admin": ["todo"],
        "usuario": ["ver"],
        "seguridad": ["logs"]
    }

    return accion in permisos.get(usuario.rol, [])