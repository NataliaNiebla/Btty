from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime, LargeBinary, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class SessionNote(Base):
    __tablename__ = "session_notes"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    
    # --- Integración con Catálogos (REQ-NOT-01) ---
    # Para diferenciar entre 'Presencial' u 'Online'
    modality_id = Column(Integer, ForeignKey("catalog_items.id"), nullable=False)
    
    # --- Contenido Clínico (REQ-NOT-01 / REQ-AUTH-04) ---
    # Si vas a cifrar, usamos JSONB para la estructura, pero recuerda que la lógica
    # de cifrado de REQ-AUTH-04 se aplicará en el servicio de Python antes de guardar.
    content_soap = Column(JSONB) # {s: "", o: "", a: "", p: ""}
    
    # --- Inteligencia Artificial (REQ-NOT-04 / REQ-NOT-05) ---
    ai_summary = Column(Text)       # Resumen generado por LLM
    sentiment_score = Column(Integer) # Puntaje para el mapa de calor emocional
    
    # --- Trazabilidad y Control (REQ-PAC-06) ---
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_finalized = Column(Boolean, default=False) # Para bloquear edición tras 48hrs
    
    # Relaciones
    patient = relationship("Patient", backref="session_notes")