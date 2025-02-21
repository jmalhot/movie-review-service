from fastapi import APIRouter
from app.schemas.review import SentimentAnalysis, SentimentResponse
from app.services.sentiment import analyze_sentiment

router = APIRouter()

@router.post("/", response_model=SentimentResponse)
def analyze_review_sentiment(text: SentimentAnalysis):
    result = analyze_sentiment(text.text)
    return result 