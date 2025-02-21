from transformers import pipeline
from app.core.config import settings

# Initialize the sentiment analysis pipeline
sentiment_analyzer = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english",
    return_all_scores=True
)

def analyze_sentiment(text: str) -> dict:
    try:
        result = sentiment_analyzer(text)[0]
        # Get the sentiment with highest score
        sentiment = max(result, key=lambda x: x["score"])
        return {
            "sentiment": sentiment["label"],
            "confidence": sentiment["score"]
        }
    except Exception as e:
        return {
            "sentiment": "neutral",
            "confidence": 0.5
        } 