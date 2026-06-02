"""WSGI 入口 — gunicorn 启动时自动建表"""
from app import create_app
from models import db

app = create_app()

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
