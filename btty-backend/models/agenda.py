from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from database import Base
import enum

class AppointmentStatus(enum.Enum):
    SCHEDULED = "agendada"
    COMPLETED = "completada"
    CANCELLED = "cancelada"
    NO_SHOW = "no_asistio"

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    
    # REQ-AGE-01 y 02
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.SCHEDULED)
    
    # Para la sincronización con Google Calendar (REQ-AGE-02)
    google_event_id = Column(String, nullable=True)
    meet_link = Column(String, nullable=True)
    
    patient = relationship("Patient", back_populates="appointments")