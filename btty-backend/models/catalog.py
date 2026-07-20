from sqlalchemy import Column, Integer, String
from database import Base

class CatalogItem(Base):
    __tablename__ = "catalog_items"
    
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(50), index=True) # ej: 'ROLE', 'PAYMENT_METHOD', 'MODALITY'
    value = Column(String(100))               # ej: 'Psicólogo', 'Transferencia', 'Online'
    code = Column(String(50), unique=True)    # ej: 'ROLE_PSY', 'PAY_CARD'