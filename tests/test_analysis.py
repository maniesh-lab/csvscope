from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_analyze_valid_csv():
    with open("tests/sample.csv", "rb") as f:
        response = client.post(
            "/api/v1/analysis/analyze",
            files={"file": ("sample.csv", f, "text/csv")}
        )
    assert response.status_code == 200
    data = response.json()
    assert "filename" in data
    assert "stats" in data
    assert "chart" in data


def test_analyze_rejects_non_csv():
    response = client.post(
        "/api/v1/analysis/analyze",
        files={"file": ("notes.txt", b"hello", "text/plain")}
    )
    assert response.status_code == 400