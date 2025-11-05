import os, time, requests
from app.app import create_app

def test_api_end_to_end(monkeypatch):
    # Point the app to CI Postgres
    db_url = os.environ["DATABASE_URL"]
    app = create_app({"DATABASE_URL": db_url, "TESTING": True})
    from threading import Thread
    t = Thread(target=lambda: app.run(port=5001), daemon=True)
    t.start()

    # Wait for server
    time.sleep(1.2)

    # Health
    r = requests.get("http://127.0.0.1:5001/health")
    assert r.status_code == 200 and r.json()["status"] == "ok"

    # Create todo
    r = requests.post("http://127.0.0.1:5001/todos", json={"title": "  Buy milk  "})
    assert r.status_code == 201
    assert r.json()["title"] == "Buy milk"

    # List todos
    r = requests.get("http://127.0.0.1:5001/todos")
    assert r.status_code == 200
    assert len(r.json()) >= 1
