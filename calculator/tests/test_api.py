from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_offers_endpoint_exists():
    response = client.post(
        "/calculator/offers",
        json={
            "amount": 300000,
            "term": 12,
            "firstName": "Ivan",
            "lastName": "Ivanov",
            "middleName": "Ivanovich",
            "email": "ivan@example.com",
            "birthdate": "1995-05-15",
            "passportSeries": "1234",
            "passportNumber": "567890",
        },
    )
    assert response.status_code != 404

def test_calc_endpoint_rejects_invalid_request():
    response = client.post(
        "/calculator/calc",
        json={},
    )
    assert response.status_code == 422

def test_unknown_endpoint_returns_404():
    response = client.get("/unknown")
    assert response.status_code == 404