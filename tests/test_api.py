from fastapi.testclient import TestClient
from app.main import app

client=TestClient(app)

def test_home_and_status():
    assert client.get("/").status_code==200
    assert client.get("/api/status").status_code==200

def test_empty_query_is_rejected():
    response=client.post("/api/search",json={"query":"  ","top_k":5})
    assert response.status_code in (409,422)

def test_invalid_build_directory_is_helpful():
    response=client.post("/api/build",json={"path":"Z:/path/that/does/not/exist"})
    assert response.status_code==400
    assert "directory" in response.json()["detail"].lower()

def test_build_and_search_end_to_end(monkeypatch):
    from pathlib import Path
    monkeypatch.setenv("ACI_OFFLINE_FALLBACK","1")
    root=Path(__file__).resolve().parents[1]/"data"/"sample_code"
    built=client.post("/api/build",json={"path":str(root)})
    assert built.status_code==200
    assert built.json()["chunks_indexed"]>=30
    result=client.post("/api/search",json={"query":"Where is the user authentication token validated?","top_k":5})
    assert result.status_code==200
    assert any("validate_token" in row["symbol_name"] for row in result.json()["results"])
