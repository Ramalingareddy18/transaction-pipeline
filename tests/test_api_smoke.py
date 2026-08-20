from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200, response.text
    payload = response.json()
    assert payload.get("status") == "ok"


def test_transactions_endpoint_returns_data():
    response = client.get("/transactions?limit=2")
    assert response.status_code == 200, response.text
    payload = response.json()
    assert isinstance(payload, list)
    assert len(payload) > 0
    first = payload[0]
    assert "transaction_id" in first
    assert "amount" in first

