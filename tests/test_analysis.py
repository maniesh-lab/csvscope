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

def post_csv(name, data, column=None):
    params = {"column": column} if column else {}
    return client.post("/api/v1/analysis/analyze", params=params, files={"file": (name, data, "text/csv")})


def test_uppercase_extension_is_accepted():
    assert post_csv("DATA.CSV", b"a\n1\n2\n").status_code == 200


def test_empty_file_returns_400():
    response = post_csv("empty.csv", b"")
    assert response.status_code == 400
    assert "empty" in response.json()["detail"]


def test_headers_only_returns_400():
    assert post_csv("headers.csv", b"a,b\n").status_code == 400


def test_malformed_csv_returns_400():
    response = post_csv("bad.csv", b'a,b\n1,2\n"unterminated,3\n4,5,6,7\n')
    assert response.status_code == 400


def test_latin1_file_is_read():
    data = "name,price\ncafé,4.5\nnaïve,3\n".encode("latin-1")
    response = post_csv("latin.csv", data)
    assert response.status_code == 200
    assert response.json()["rows"] == 2


def test_unknown_column_explains_missing_chart():
    response = post_csv("data.csv", b"a,b\n1,2\n3,4\n", column="nope")
    body = response.json()
    assert response.status_code == 200
    assert body["chart"] is None
    assert "not found" in body["message"]


def test_text_column_explains_missing_chart():
    response = post_csv("data.csv", b"name,age\nbob,3\nann,4\n", column="name")
    body = response.json()
    assert body["chart"] is None
    assert "isn't numeric" in body["message"]


def test_numeric_column_gets_chart():
    body = post_csv("data.csv", b"name,age\nbob,3\nann,4\n", column="age").json()
    assert body["chart"]
    assert body["message"] is None
