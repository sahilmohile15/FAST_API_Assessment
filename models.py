from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from db import Base
    
class Address(Base):
    __tablename__ = "address"
    
    id = Column(Integer, primary_key=True,index=True)
    name = Column(String(80), nullable=False, unique=True,index=True)
    address = Column(String(512), nullable=False)
    address_point = Column(String(100), nullable=False)

    def __repr__(self):
        return 'Address(name=%s)' % (self.name)
    
