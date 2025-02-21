from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ReviewBase(BaseModel):
    movie_id: str
    user_id: str
    content: str
    rating: int

class ReviewCreate(ReviewBase):
    pass

class ReviewUpdate(BaseModel):
    content: Optional[str] = None
    rating: Optional[int] = None

class Review(ReviewBase):
    id: int
    sentiment: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class SentimentAnalysis(BaseModel):
    text: str

class SentimentResponse(BaseModel):
    sentiment: str
    confidence: float 