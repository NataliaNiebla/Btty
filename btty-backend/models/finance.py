from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    appointment_id = Column(Integer, ForeignKey("appointments.id")) # REQ-FIN-01
    
    # --- Datos Monetarios ---
    amount = Column(Float, nullable=False)
    discount_applied = Column(Float, default=0.0) # REQ-FIN-02 (Becas)
    
    # --- Integración con Catálogos (NUEVO) ---
    # Sustituimos el Enum por la relación al catálogo
    payment_method_id = Column(Integer, ForeignKey("catalog_items.id"), nullable=False)
    
    # --- Control y Facturación (REQ-FIN-03) ---
    invoice_number = Column(String, unique=True, nullable=True) 
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones para facilitar consultas
    patient = relationship("Patient")
    appointment = relationship("Appointment")