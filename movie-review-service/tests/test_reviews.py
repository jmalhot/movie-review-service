from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.database import Base, get_db
from main import app
import pytest

# Use SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_review(test_db):
    response = client.post(
        "/reviews/",
        json={
            "movie_id": "tt0111161",
            "user_id": "user123",
            "content": "Great movie!",
            "rating": 5
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["movie_id"] == "tt0111161"
    assert data["content"] == "Great movie!"
    assert "sentiment" in data

def test_get_movie_reviews(test_db):
    # First create a review
    client.post(
        "/reviews/",
        json={
            "movie_id": "tt0111161",
            "user_id": "user123",
            "content": "Great movie!",
            "rating": 5
        },
    )
    
    response = client.get("/reviews/tt0111161")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["movie_id"] == "tt0111161"

def test_update_review(test_db):
    # First create a review
    create_response = client.post(
        "/reviews/",
        json={
            "movie_id": "tt0111161",
            "user_id": "user123",
            "content": "Great movie!",
            "rating": 5
        },
    )
    review_id = create_response.json()["id"]
    
    response = client.put(
        f"/reviews/{review_id}",
        json={
            "content": "Updated review",
            "rating": 4
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "Updated review"
    assert data["rating"] == 4

def test_delete_review(test_db):
    # First create a review
    create_response = client.post(
        "/reviews/",
        json={
            "movie_id": "tt0111161",
            "user_id": "user123",
            "content": "Great movie!",
            "rating": 5
        },
    )
    review_id = create_response.json()["id"]
    
    response = client.delete(f"/reviews/{review_id}")
    assert response.status_code == 200
    
    # Verify review is deleted
    response = client.get("/reviews/tt0111161")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0 