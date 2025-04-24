from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime
from .database import Base

class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    long_url = Column(String, unique=True, index=True, nullable=False)
    short_url = Column(String, unique=True, index=True, nullable=False)
    visits = Column(Integer, default=0)