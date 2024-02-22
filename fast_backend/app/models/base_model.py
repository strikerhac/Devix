from sqlalchemy.ext.declarative import declarative_base

from app.core.config import Base


from sqlalchemy import ForeignKey,String,Boolean,Column,Integer,DateTime,func

class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())