# app/repositories/db.py
import uuid
from typing import Any

# Имитация БД в памяти
books_db: dict[str, dict[str, Any]] = {}
authors_db: dict[str, dict[str, Any]] = {}

def generate_id() -> str:
    return str(uuid.uuid4())