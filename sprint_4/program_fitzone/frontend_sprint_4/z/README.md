# 💪 FitZone - Sistema de Gestión de Usuarios

## 📌 Descripción
FitZone es una aplicación de escritorio desarrollada en Python que permite la gestión de usuarios mediante autenticación por roles y operaciones CRUD. El sistema fue construido siguiendo principios de Programación Orientada a Objetos (POO) y buenas prácticas de ingeniería de software.

---

## 🎯 Funcionalidades
- 🔐 Autenticación de usuarios (login)
- 👑 Panel administrador con CRUD completo
- 👤 Panel usuario
- 🛡 Panel seguridad
- 🧪 Pruebas automatizadas con pytest
- ✅ Pruebas con assert
- 📊 Análisis de calidad con SonarQube

---

## 🧱 Arquitectura
El proyecto sigue una arquitectura por capas:

- **models**: entidades del sistema
- **services**: lógica de negocio
- **ui**: interfaz gráfica
- **tests**: pruebas

---

## 🛠 Tecnologías
- Python
- PySide6
- Pytest
- SonarQube
- GitHub

---

## ▶️ Ejecución

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
