from fastapi.testclient import TestClient

from finances_statements.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/api/v1/statements")
    assert response.status_code == 404
    assert response.json() == {"detail": "Statements not found"}
