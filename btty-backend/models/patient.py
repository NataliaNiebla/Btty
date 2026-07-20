from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from database import Base

class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # --- Datos de Identificación (REQ-PAC-01) ---
    nombre = Column(String(100), nullable=False)
    apellido_paterno = Column(String(100), nullable=False)
    apellido_materno = Column(String(100), nullable=True)
    telefono = Column(String(20))
    direccion = Column(String(255))
    
    # --- Integración con Catálogos (NUEVO) ---
    # En lugar de texto, guardamos el ID del catálogo
    estado_civil_id = Column(Integer, ForeignKey("catalog_items.id"), nullable=True)
    genero_id = Column(Integer, ForeignKey("catalog_items.id"), nullable=True)
    
    # --- Datos Numéricos ---
    numero_hijos = Column(Integer, default=0)
    
    # --- Datos Complejos (REQ-PAC-01, 02, 03, 04) ---
    # Usamos JSONB para que la IA (CopilotKit) analice patrones después
    emergency_contact = Column(JSONB)  # {name: "", phone: "", relation: ""}
    family_context = Column(JSONB)     # Estructura familiar, nombres de padres
    occupation_data = Column(JSONB)    # Hobbies, trabajo actual, nivel de estudios
    clinical_profile = Column(JSONB)   # Motivo de consulta, medicinas, metas
    
    # --- Relaciones (Opcional, ayuda a las consultas) ---
    user = relationship("User")
    appointments = relationship("Appointment", back_populates="patient")