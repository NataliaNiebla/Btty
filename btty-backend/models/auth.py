from sqlalchemy import Column, ForeignKey, Integer, String, Enum, DateTime, Boolean
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String) # REQ-AUTH-06
    role_id = Column(Integer, ForeignKey("catalog_items.id"))
    is_2fa_enabled = Column(Boolean, default=False) # REQ-AUTH-03
    secret_2fa = Column(String, nullable=True)