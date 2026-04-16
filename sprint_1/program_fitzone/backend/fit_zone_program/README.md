# Gym Sprint 1 - MVC Base

This project contains a simple MVC base for Sprint 1 of a gym management system.

## Included modules
- `User`
- `Membership`
- `Payment`
- `UserController`
- `MembershipController`
- `PaymentController`

## Structure
```text
config/
models/
controllers/
database/
diagrams/
main.py
```

## Naming rules applied
- Classes in `PascalCase`
- Methods and attributes in `snake_case`
- Tables and columns in `snake_case`
- English used in all code

## How to use
1. Create the database with `database/schema.sql`
2. Install the dependency:
   ```bash
   pip install -r requirements.txt
   ```
3. Update MySQL credentials in `main.py` and `config/database.py` if needed.
4. Run:
   ```bash
   python main.py
   ```

## Important note
Passwords are hashed with SHA-256 to keep the solution simple for the sprint. In a production project, `bcrypt` is recommended.
