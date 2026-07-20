import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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