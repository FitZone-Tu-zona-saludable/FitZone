import re

from frontend.services.app_context import (
    auth_service,
    membership_service,
    schedule_service,
    survey_service,
    trainer_service,
    worker_service,
)
from frontend.services.state_service import refresh_current_user


def _extract_years(raw_value):
    if isinstance(raw_value, (int, float)):
        return int(raw_value)
    match = re.search(r"\d+", str(raw_value or ""))
    return int(match.group(0)) if match else 0


def _add_one_hour(hour_text):
    parts = str(hour_text).split(":")
    return f"{(int(parts[0]) + 1) % 24:02d}:{parts[1]}"


def fetch_schedules(filter_date=None, trainer_id=0):
    rows = []
    for schedule in schedule_service.get_schedules():
        if filter_date and schedule.fecha != filter_date:
            continue
        if trainer_id and schedule.id_entrenador != trainer_id:
            continue

        rows.append({
            "id": schedule.id_horario,
            "date": schedule.fecha,
            "time": schedule.hora_inicio,
            "class_name": schedule.tipo,
            "trainer_id": schedule.id_entrenador,
            "capacity": schedule.cupos,
            "enrolled": 0,
        })
    return rows


def save_schedule(data):
    class_name = (data.get("class_name") or "").strip()
    date = (data.get("date") or "").strip()
    time = (data.get("time") or "").strip()
    trainer_id = data.get("trainer_id")
    capacity = int(data.get("capacity", 0))
    schedule_id = data.get("id")

    if not class_name or not date or not time or capacity <= 0:
        return {"success": False, "message": "Debes completar clase, fecha, hora y cupos válidos."}

    if schedule_id:
        updated = schedule_service.update_schedule(
            schedule_id,
            fecha=date,
            hora_inicio=time,
            hora_fin=_add_one_hour(time),
            tipo=class_name,
            cupos=capacity,
            id_entrenador=trainer_id,
        )
        return {
            "success": updated,
            "message": "Horario actualizado correctamente." if updated else "No se pudo actualizar el horario.",
        }

    schedule_service.create_schedule(
        date,
        time,
        _add_one_hour(time),
        class_name,
        capacity,
        id_entrenador=trainer_id,
    )
    return {"success": True, "message": "Horario creado correctamente."}


def delete_schedule(schedule_id):
    deleted = schedule_service.delete_schedule(schedule_id)
    return {
        "success": deleted,
        "message": "Horario eliminado correctamente." if deleted else "No se encontró el horario.",
    }


def fetch_trainers():
    ratings = survey_service.avg_trainer_score()
    rows = []
    for trainer in trainer_service.get_trainers():
        rating = ratings.get((trainer.id_trabajador, trainer.nombre), 0.0)
        rows.append({
            "id": trainer.id_trabajador,
            "name": trainer.nombre,
            "specialty": trainer.especialidad or "General",
            "experience_years": _extract_years(trainer.experiencia),
            "rating": float(rating),
            "available": bool(trainer.disponible),
            "email": trainer.correo,
            "document_id": getattr(trainer, "documento", ""),
        })
    return rows


def assign_trainer(user_id, trainer_id):
    user = auth_service.find_by_id(user_id)
    trainer = trainer_service.get_by_id(trainer_id)

    if not user:
        return {"success": False, "message": "Usuario no autenticado."}
    if not trainer:
        return {"success": False, "message": "Entrenador no encontrado."}
    if not trainer.disponible:
        return {"success": False, "message": "El entrenador no está disponible."}

    result = membership_service.assign_trainer(
        user_id,
        trainer.id_trabajador,
        trainer.nombre,
    )
    refresh_current_user(auth_service)
    return result


def set_trainer_availability(trainer_id, available):
    updated = trainer_service.set_availability(trainer_id, available)
    return {
        "success": updated,
        "message": "Disponibilidad actualizada correctamente." if updated else "No se encontró el entrenador.",
    }


def register_staff(data):
    full_name = (data.get("full_name") or "").strip()
    document_id = (data.get("document_id") or "").strip()
    phone = (data.get("phone") or "").strip()
    email = (data.get("email") or "").strip().lower()
    role = (data.get("role") or "trabajador").strip().lower()
    position = (data.get("position") or "").strip()
    modality = (data.get("modality") or "presencial").strip().lower()
    experience = data.get("experience", 0)

    if not full_name or not position:
        return {"success": False, "message": "Nombre y cargo son obligatorios."}

    for worker in worker_service.get_workers():
        if email and worker.correo.lower() == email:
            return {"success": False, "message": "Ya existe un trabajador con ese correo."}

    experience_text = f"{experience} años" if str(experience).isdigit() else str(experience)

    if role == "empleado":
        worker_service.register_employee(
            full_name,
            position,
            phone,
            email,
            experiencia=experience_text,
            modalidad=modality,
            documento=document_id,
        )
    else:
        worker_service.create_worker(
            full_name,
            position,
            phone,
            email,
            experiencia=experience_text,
            modalidad=modality,
            documento=document_id,
        )

    return {"success": True, "message": "Personal registrado correctamente."}


def fetch_staff():
    rows = []
    for worker in worker_service.get_workers():
        rows.append({
            "id": worker.id_trabajador,
            "full_name": worker.nombre,
            "document_id": getattr(worker, "documento", ""),
            "role": "empleado" if hasattr(worker, "estado_laboral") else "trabajador",
            "position": worker.cargo,
            "modality": worker.modalidad,
            "email": worker.correo,
        })
    return rows
