# python
# scripts/create_db.py
from sqlalchemy import create_engine
from app.infrastructure.database.create_bdd import declaracion_bdd as models

DB_URL = "sqlite:///./bdd.db"  # fichero SQLite en el proyecto
engine = create_engine(DB_URL, echo=True, future=True)

# Crea las tablas definidas en models.Base
models.Base.metadata.create_all(engine)

print(f"Base de datos creada en {DB_URL}")