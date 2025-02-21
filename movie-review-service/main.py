from fastapi import FastAPI
from app.db.database import engine
from app.models import review
from app.api import reviews, sentiment
from app.middleware.rate_limit import rate_limit_middleware
from app.core.logging import logger

# Create database tables
review.Base.metadata.create_all(bind=engine)

app = FastAPI(title="ReviewFlow API")

# Add middleware
app.middleware("http")(rate_limit_middleware)

# Include routers
app.include_router(reviews.router, prefix="/reviews", tags=["reviews"])
app.include_router(sentiment.router, prefix="/analyze", tags=["sentiment"])

@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to ReviewFlow API"} 