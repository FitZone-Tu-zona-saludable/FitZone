# FitZone MVC en Python

Proyecto base en **Python + MVC + POO** construido a partir del diagrama UML y la descripción funcional del sistema de FitZone.

## Estructura

```text
fitzone_mvc/
├── app/
│   ├── config/
│   │   └── database.py
│   ├── controllers/
│   ├── models/
│   ├── repositories/
│   ├── services/
│   └── utils/
├── data/
│   └── fitzone.db
├── main.py
└── README.md
```

## Patrón aplicado

- **Models**: entidades y enums del dominio (`User`, `MembershipPlan`, `UserMembership`, `Payment`, `AccessLog`).
- **Repositories**: acceso a datos con `sqlite3`.
- **Services**: validaciones y reglas del negocio.
- **Controllers**: punto de entrada para cada caso de uso.

## Casos ya implementados

- Registro de usuario
- Inicio y cierre de sesión
- Gestión básica de usuarios
- Listado de planes activos
- Asignación de membresía a usuario
- Registro de pago validando usuario, membresía y monto
- Bitácora de accesos

## Reglas de negocio cubiertas

- No permite correos duplicados.
- La contraseña se cifra con `pbkdf2_hmac`.
- El login registra éxito o fallo en `AccessLog`.
- `UserMembership` actúa como entidad puente entre `User` y `MembershipPlan`.
- Un pago pertenece a un usuario y a una membresía específica del usuario.
- El monto del pago debe coincidir con el precio del plan asociado.

## Ejecutar

```bash
python main.py
```

## Siguiente paso recomendado

Convertir estos controladores en una API real con **Flask** o **FastAPI**, manteniendo la misma separación MVC.
