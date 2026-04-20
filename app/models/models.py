from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base

class Url(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String(2048), nullable=False)
    short_code = Column(String(10), unique=True, nullable=False, index=True)
    clicks = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)