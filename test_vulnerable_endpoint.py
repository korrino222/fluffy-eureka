from fastapi.testclient import TestClient
from vulnerable_endpoint import app

client = TestClient(app)


def test_run_command():
    response = client.get("/run", params={"cmd": "whoami"})
    assert response.status_code == 200


def test_run_command_rejects_disallowed():
    response = client.get("/run", params={"cmd": "rm -rf /"})
    assert response.status_code == 400


def test_read_file(tmp_path, monkeypatch):
    import vulnerable_endpoint
    monkeypatch.setattr(vulnerable_endpoint, "SAFE_BASE", str(tmp_path))
    sample = tmp_path / "sample.txt"
    sample.write_text("hello")
    response = client.get("/read", params={"path": "sample.txt"})
    assert response.status_code == 200
    assert response.json()["content"] == "hello"


def test_read_file_rejects_traversal(tmp_path, monkeypatch):
    import vulnerable_endpoint
    monkeypatch.setattr(vulnerable_endpoint, "SAFE_BASE", str(tmp_path))
    response = client.get("/read", params={"path": "../../etc/passwd"})
    assert response.status_code == 400
