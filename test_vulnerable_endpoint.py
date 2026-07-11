from fastapi.testclient import TestClient
from vulnerable_endpoint import app

client = TestClient(app)


def test_run_command():
    response = client.get("/run", params={"cmd": "whoami"})
    assert response.status_code == 200


def test_read_file(tmp_path):
    sample = tmp_path / "sample.txt"
    sample.write_text("hello")
    response = client.get("/read", params={"path": str(sample)})
    assert response.status_code == 200
    assert response.json()["content"] == "hello"
