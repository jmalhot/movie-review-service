# Movie Review Service

A robust FastAPI-based microservice for managing movie reviews with automated sentiment analysis. This service provides a RESTful API for creating, reading, updating, and deleting movie reviews while leveraging HuggingFace's transformer models to perform sentiment analysis on review content.

## Table of Contents
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Database Schema](#database-schema)
- [Sentiment Analysis](#sentiment-analysis)
- [Testing](#testing)
- [Logging](#logging)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## Features

### Core Features
- **CRUD Operations**: Complete set of operations for movie reviews
- **Automated Sentiment Analysis**: Real-time sentiment analysis of review content
- **Input Validation**: Comprehensive validation for all user inputs
- **Persistent Storage**: PostgreSQL-based data persistence
- **Logging System**: Detailed logging for monitoring and debugging

### Technical Features
- RESTful API design
- Asynchronous request handling
- Database connection pooling
- Rate limiting support
- Error handling with detailed responses
- Configurable via environment variables

## Technology Stack

- **Framework**: FastAPI 0.109.2
- **Database**: PostgreSQL 14+
- **ORM**: SQLAlchemy 2.0.27
- **ML Model**: HuggingFace Transformers 4.37.2
- **Python Version**: 3.10+

## Prerequisites

- Python 3.10 or higher
- PostgreSQL 14 or higher
- pip (Python package manager)
- Virtual environment (recommended)
- 4GB+ RAM (for ML model)
- Git (for version control)

## Installation

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd movie-review-service
```

### 2. Set Up Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Unix/macOS:
source venv/bin/activate
# On Windows:
.\venv\Scripts\activate
```

### 3. Install Dependencies
```bash
# Install all required packages
pip install -r requirements.txt
```

### 4. PostgreSQL Setup

#### Using Postgres.app (macOS - Recommended)
1. Download Postgres.app from https://postgresapp.com/
2. Move to Applications folder and open
3. Click "Initialize" to start PostgreSQL

#### Using Command Line
```bash
# Create database
psql -U postgres
CREATE DATABASE reviewflow;
CREATE USER myuser WITH PASSWORD 'mypassword';
GRANT ALL PRIVILEGES ON DATABASE reviewflow TO myuser;
```

## Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/reviewflow

# Model Configuration
MODEL_PATH=distilbert-base-uncased-finetuned-sst-2-english

# API Configuration
HOST=0.0.0.0
PORT=8000
WORKERS=4

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60

# Review Validation
MIN_REVIEW_LENGTH=10
MAX_REVIEW_LENGTH=2000
MIN_RATING=1
MAX_RATING=5

# Logging
LOG_LEVEL=INFO
```

## Running the Application

### Development Mode
```bash
# Start the FastAPI server with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode
```bash
# Start the FastAPI server with multiple workers
python main.py
```

The API will be available at:
- API Endpoints: `http://localhost:8000`
- Interactive Documentation: `http://localhost:8000/docs`
- Alternative Documentation: `http://localhost:8000/redoc`

## API Documentation

### Reviews API

#### Create Review
```http
POST /reviews/
Content-Type: application/json

{
    "movie_id": "tt0111161",
    "content": "A masterpiece that defines the genre. The acting was superb and the story compelling.",
    "rating": 5
}
```

Response:
```json
{
    "id": 1,
    "movie_id": "tt0111161",
    "content": "A masterpiece that defines the genre. The acting was superb and the story compelling.",
    "rating": 5,
    "sentiment": "POSITIVE",
    "created_at": "2024-02-29T10:30:00Z"
}
```

#### Get Movie Reviews
```http
GET /reviews/{movie_id}
```

Response:
```json
[
    {
        "id": 1,
        "movie_id": "tt0111161",
        "content": "A masterpiece that defines the genre.",
        "rating": 5,
        "sentiment": "POSITIVE",
        "created_at": "2024-02-29T10:30:00Z"
    }
]
```

#### Update Review
```http
PUT /reviews/{review_id}
Content-Type: application/json

{
    "content": "Updated review content",
    "rating": 4
}
```

#### Delete Review
```http
DELETE /reviews/{review_id}
```

## Database Schema

### Review Table
```sql
CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    movie_id VARCHAR(20) NOT NULL,
    content TEXT NOT NULL,
    rating INTEGER NOT NULL,
    sentiment VARCHAR(20),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

## Sentiment Analysis

The service uses the `distilbert-base-uncased-finetuned-sst-2-english` model for sentiment analysis. This model:
- Is fine-tuned for English language sentiment analysis
- Provides binary classification (POSITIVE/NEGATIVE)
- Returns confidence scores for predictions
- Is optimized for performance

### Model Fine-tuning

A Python script and Jupyter notebook are provided in the `notebooks` directory for fine-tuning the sentiment analysis model:
- Notebook: `notebooks/fine_tune_model.ipynb`

The fine-tuning process includes:
- Loading and preprocessing the IMDB dataset (50K movie reviews)
- Initializing a DistilBERT model for binary classification
- Training with optimized hyperparameters
- Evaluation using accuracy, precision, recall, and F1 score
- Model testing with sample reviews
- Saving the fine-tuned model for production use

#### Running the Fine-tuning Process

1. Install required packages:
```bash
pip install transformers datasets torch numpy pandas sklearn tqdm
```

2. Or use Jupyter Notebook:
```bash
pip install jupyter
jupyter notebook notebooks/fine_tune_model.ipynb
```

#### Fine-tuning Parameters
- Learning rate: 2e-5
- Batch size: 16
- Training epochs: 3
- Max sequence length: 512
- Weight decay: 0.01
- Evaluation strategy: Per epoch
- Random seed: 42

#### Model Output Directory
The fine-tuned model will be saved to `models/fine_tuned_sentiment/`, which can then be used by updating the `MODEL_PATH` in your `.env` file:
```env
MODEL_PATH=./models/fine_tuned_sentiment
```

### Example Sentiment Results
```json
{
    "sentiment": "POSITIVE",
    "confidence": 0.9876
}
```

## Testing

### Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_reviews.py

# Run with coverage report
pytest --cov=app tests/
```

## Logging

The application uses Python's built-in logging module with the following levels:
- DEBUG: Detailed information for debugging
- INFO: General operational events
- WARNING: Unexpected but handled events
- ERROR: Serious issues that need attention
- CRITICAL: System-critical issues

Logs are written to both console and file:
```
logs/
├── app.log
└── error.log
```

## Troubleshooting

### Common Issues

#### Database Connection Failed
```
Error: connection to server at "localhost" (::1), port 5432 failed
```
Solution:
1. Check if PostgreSQL is running
2. Verify database credentials in .env
3. Ensure database exists

#### Model Download Issues
```
Error: Failed to download model
```
Solution:
1. Check internet connection
2. Clear transformers cache:
```bash
rm -rf ~/.cache/huggingface/
```

#### Memory Issues
```
Error: CUDA out of memory
```
Solution:
1. Reduce batch size
2. Use CPU instead of GPU
3. Increase system swap space

## Contributing

### Development Workflow
1. Fork the repository
2. Create a feature branch
```bash
git checkout -b feature/your-feature-name
```
3. Make your changes
4. Run tests
5. Submit pull request

### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Write docstrings for functions
- Keep functions focused and small
