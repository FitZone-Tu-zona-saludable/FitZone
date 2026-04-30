"""Funciones pequeñas para leer y guardar listas JSON de forma segura."""

import json
import os
import tempfile


def ensure_parent_dir(path):
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)


def load_json_list(path):
    """Carga una lista JSON. Devuelve [] si el archivo no existe, está vacío o es inválido."""
    ensure_parent_dir(path)
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return []

    try:
        with open(path, "r", encoding="utf-8") as handler:
            data = json.load(handler)
    except (json.JSONDecodeError, OSError, TypeError):
        return []

    return data if isinstance(data, list) else []


def save_json_list(path, records):
    """Guarda una lista JSON de forma atómica: escribe en archivo temporal
    y luego lo reemplaza. Nunca deja el archivo destino en estado corrupto."""
    ensure_parent_dir(path)
    dir_name = os.path.dirname(os.path.abspath(path))
    try:
        fd, tmp_path = tempfile.mkstemp(dir=dir_name, suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handler:
                json.dump(records, handler, indent=4, ensure_ascii=False)
            os.replace(tmp_path, path)
        except Exception:
            # Si algo falla, eliminar el temporal para no dejar basura
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
            raise
    except OSError as exc:
        raise RuntimeError(f"Error al guardar '{path}': {exc}") from exc
