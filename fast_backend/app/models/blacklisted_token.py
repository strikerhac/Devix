from sqlalchemy import Column, String
from .base_model import BaseModel


class BlacklistedToken(BaseModel):
    __tablename__ = "blacklisted_token"

    token = Column(String(5500), unique=True, index=True)
    email = Column(String(255), index=True,nullable=True)
