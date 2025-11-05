from flask import Flask, request, jsonify
from app.db import get_db, init_db
from app.logic import normalize_title

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.update(test_config or {})

    @app.route("/health")
    def health():
        return {"status": "ok"}, 200

    @app.route("/todos", methods=["GET", "POST"])
    def todos():
        conn = get_db(app.config)
        cur = conn.cursor()
        if request.method == "POST":
            title = normalize_title(request.json.get("title", ""))
            cur.execute("INSERT INTO todos(title) VALUES (%s) RETURNING id, title", (title,))
            row = cur.fetchone()
            conn.commit()
            return jsonify({"id": row[0], "title": row[1]}), 201

        cur.execute("SELECT id, title FROM todos ORDER BY id")
        rows = cur.fetchall()
        return jsonify([{"id": r[0], "title": r[1]} for r in rows])

    with app.app_context():
        init_db(get_db(app.config))
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
