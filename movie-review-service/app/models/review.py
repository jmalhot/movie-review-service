from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.db.database import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(String, index=True)
    user_id = Column(String, index=True)
    content = Column(Text)
    rating = Column(Integer)
    sentiment = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) 