from asyncio.log import logger
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy.orm import Session
# from models.audit import AuditLog

# 1. Cargar las variables desde el archivo .env
load_dotenv()

# 2. Leer la URL de la base de datos de forma segura
# Si por alguna razón no lee el .env, usa una URL vacía o por defecto
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
    raise RuntimeError("ERROR: La variable DATABASE_URL no está configurada en el archivo .env")

# 3. Crear el motor de SQLAlchemy y la sesión
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
     
# Función para registrar eventos de auditoría en la base de datos   
def db_log_event(
    db: Session,
    action: str,
    user_id: int | None = None,
    resource_id: str | None = None,
    ip_address: str | None = None,
    user_agent: str | None = None
):
    """ Inserta un registro de auditoría utilizando el esquema existente de audit_logs."""
    from models.audit import AuditLog  # Importar aquí para evitar problemas de importación circular
    try:
        log_entry = AuditLog(
            user_id=user_id,
            action=action,
            resource_id=resource_id,
            ip_address=ip_address,
            user_agent=user_agent
        )
        db.add(log_entry)
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Error al guardar log en BD: {e}")