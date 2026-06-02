"""
博客 API — Flask + SQLAlchemy + JWT 认证

快速启动:
    pip install -r requirements.txt
    python app.py

浏览器打开 http://localhost:5000 查看 API 文档
"""

from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from config import Config
from models import db
from routes.auth import auth_bp
from routes.articles import articles_bp
from routes.comments import comments_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 初始化扩展
    db.init_app(app)
    JWTManager(app)

    # 注册蓝图
    app.register_blueprint(auth_bp)
    app.register_blueprint(articles_bp)
    app.register_blueprint(comments_bp)

    # ── 首页（API 概览） ──
    @app.route("/")
    def index():
        return jsonify({
            "name": "Blog API",
            "version": "1.0.0",
            "description": "一个基于 Flask 的博客后端 API 项目",
            "endpoints": {
                "认证": {
                    "POST /api/auth/register": "用户注册",
                    "POST /api/auth/login": "用户登录（返回 JWT Token）",
                    "GET /api/auth/me": "获取当前用户信息（需 Token）",
                },
                "文章": {
                    "GET /api/articles": "文章列表（支持 ?page=&search=）",
                    "POST /api/articles": "创建文章（需 Token）",
                    "GET /api/articles/<id>": "文章详情",
                    "PUT /api/articles/<id>": "更新文章（需 Token，仅作者）",
                    "DELETE /api/articles/<id>": "删除文章（需 Token，仅作者）",
                },
                "评论": {
                    "GET /api/articles/<id>/comments": "文章评论列表",
                    "POST /api/articles/<id>/comments": "发表评论（需 Token）",
                    "DELETE /api/comments/<id>": "删除评论（需 Token，作者或文章作者）",
                },
            },
            "docs": "访问 /api/articles 查看第一篇文章列表",
        })

    # ── 全局错误处理 ──
    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({"error": str(e.description) if e.description else "请求参数错误"}), 400

    @app.errorhandler(401)
    def unauthorized(e):
        return jsonify({"error": "未登录或 Token 已过期"}), 401

    @app.errorhandler(403)
    def forbidden(e):
        return jsonify({"error": "没有权限执行此操作"}), 403

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": str(e.description) if e.description else "资源不存在"}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"error": "服务器内部错误"}), 500

    return app


if __name__ == "__main__":
    app = create_app()

    # 首次运行自动建表
    with app.app_context():
        db.create_all()

    print("=" * 50)
    print("  Blog API 已启动！")
    print("  地址: http://127.0.0.1:5000")
    print("  首次运行已自动创建数据库表")
    print("=" * 50)
    app.run(debug=True, port=5000)
