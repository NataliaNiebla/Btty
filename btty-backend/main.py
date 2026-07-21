from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import importlib
from database import engine, Base # Importamos la conexión y la base
from routers import auth

# Importamos todos los modelos para que SQLAlchemy los reconozca.
for module_name in (
    "models.auth",
    "models.patient",
    "models.session",
    "models.agenda",
    "models.finance",
    "models.audit",
    "models.catalog"
):
    importlib.import_module(module_name)

# 1. Crear las tablas en PostgreSQL (Docker)
# Esto lee todos los archivos de 'models' y crea las tablas si no existen
# Usar la Base importada desde el módulo 'database'
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="BTTY API Backend",
    description="API para la gestión clínica con auditoría y seguridad activa",
    version="1.0.0"
)

# 2. Configuración de CORS (REQ-AUTH)
# Permite que tu frontend en React (localhost:5173) se comunique con este backend
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Rutas de prueba y verificación
@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "Backend de BTTY funcionando correctamente",
        "database": "PostgreSQL (Docker) Conectado"
    }

@app.get("/api/healthcheck")
def health_check():
    # Esta ruta sirve para que el frontend verifique la conexión rápidamente
    return {"status": "ok", "version": "1.0.0"}

# 4. Registro de routers (módulos)
app.include_router(auth.router)
