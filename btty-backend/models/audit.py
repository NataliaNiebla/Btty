from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from datetime import datetime
from sqlalchemy.sql import func
from database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # REQ-AUTH-05: Timestamp inalterable y datos de acceso
    action = Column(String(100)) # ej: "LECTURA_EXPEDIENTE"
    resource_id = Column(String) # ID del paciente consultado
    ip_address = Column(String(45))
    user_agent = Column(Text)
    
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Importante: NO crear endpoints de DELETE para esta tabla.