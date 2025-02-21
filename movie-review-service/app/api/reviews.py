from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.models.review import Review
from app.schemas.review import ReviewCreate, ReviewUpdate, Review as ReviewSchema
from app.services.sentiment import analyze_sentiment
from app.core.config import settings
from app.core.logging import logger
from pydantic import ValidationError

router = APIRouter()

def validate_review_content(content: str):
    if len(content) < settings.MIN_REVIEW_LENGTH:
        raise HTTPException(
            status_code=400,
            detail=f"Review content must be at least {settings.MIN_REVIEW_LENGTH} characters"
        )
    if len(content) > settings.MAX_REVIEW_LENGTH:
        raise HTTPException(
            status_code=400,
            detail=f"Review content cannot exceed {settings.MAX_REVIEW_LENGTH} characters"
        )

def validate_rating(rating: int):
    if rating < settings.MIN_RATING or rating > settings.MAX_RATING:
        raise HTTPException(
            status_code=400,
            detail=f"Rating must be between {settings.MIN_RATING} and {settings.MAX_RATING}"
        )

@router.post("/", response_model=ReviewSchema)
async def create_review(review: ReviewCreate, request: Request, db: Session = Depends(get_db)):
    logger.info(f"Creating new review for movie {review.movie_id}")
    
    try:
        # Validate review
        validate_review_content(review.content)
        validate_rating(review.rating)
        
        # Create review
        db_review = Review(**review.dict())
        
        # Analyze sentiment
        sentiment_result = analyze_sentiment(review.content)
        db_review.sentiment = sentiment_result["sentiment"]
        
        db.add(db_review)
        db.commit()
        db.refresh(db_review)
        
        logger.info(f"Review created successfully for movie {review.movie_id}")
        return db_review
        
    except ValidationError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating review: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{movie_id}", response_model=List[ReviewSchema])
async def get_movie_reviews(movie_id: str, db: Session = Depends(get_db)):
    logger.info(f"Fetching reviews for movie {movie_id}")
    
    # Get from database
    reviews = db.query(Review).filter(Review.movie_id == movie_id).all()
    
    logger.info(f"Found {len(reviews)} reviews for movie {movie_id}")
    return reviews

@router.put("/{review_id}", response_model=ReviewSchema)
async def update_review(
    review_id: int,
    review: ReviewUpdate,
    request: Request,
    db: Session = Depends(get_db)
):
    logger.info(f"Updating review {review_id}")
    
    try:
        db_review = db.query(Review).filter(Review.id == review_id).first()
        if not db_review:
            raise HTTPException(status_code=404, detail="Review not found")
        
        update_data = review.dict(exclude_unset=True)
        
        if "content" in update_data:
            validate_review_content(update_data["content"])
            sentiment_result = analyze_sentiment(update_data["content"])
            update_data["sentiment"] = sentiment_result["sentiment"]
            
        if "rating" in update_data:
            validate_rating(update_data["rating"])
        
        for key, value in update_data.items():
            setattr(db_review, key, value)
        
        db.commit()
        db.refresh(db_review)
        
        logger.info(f"Review {review_id} updated successfully")
        return db_review
        
    except Exception as e:
        logger.error(f"Error updating review {review_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/{review_id}")
async def delete_review(review_id: int, request: Request, db: Session = Depends(get_db)):
    logger.info(f"Deleting review {review_id}")
    
    try:
        db_review = db.query(Review).filter(Review.id == review_id).first()
        if not db_review:
            raise HTTPException(status_code=404, detail="Review not found")
        
        db.delete(db_review)
        db.commit()
        
        logger.info(f"Review {review_id} deleted successfully")
        return {"message": "Review deleted successfully"}
        
    except Exception as e:
        logger.error(f"Error deleting review {review_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error") 