from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Article

articles_bp = Blueprint("articles", __name__, url_prefix="/api/articles")


@articles_bp.route("", methods=["GET"])
def list_articles():
    """获取文章列表（支持分页和搜索）"""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    search = request.args.get("search", "").strip()

    # 参数边界校验
    page = max(1, page)
    per_page = min(max(1, per_page), 50)

    query = Article.query
    if search:
        query = query.filter(
            Article.title.contains(search) | Article.content.contains(search)
        )

    pagination = (
        query.order_by(Article.created_at.desc())
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return jsonify({
        "articles": [a.to_dict(brief=True) for a in pagination.items],
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": pagination.total,
            "pages": pagination.pages,
            "has_next": pagination.has_next,
            "has_prev": pagination.has_prev,
        },
    })


@articles_bp.route("", methods=["POST"])
@jwt_required()
def create_article():
    """创建文章（需登录）"""
    data = request.get_json()

    if not data or not data.get("title") or not data.get("content"):
        return jsonify({"error": "标题和内容不能为空"}), 400

    title = data["title"].strip()
    content = data["content"].strip()

    if not title:
        return jsonify({"error": "标题不能为空"}), 400
    if len(title) > 200:
        return jsonify({"error": "标题不能超过 200 字"}), 400
    if not content:
        return jsonify({"error": "内容不能为空"}), 400

    article = Article(
        title=title,
        content=content,
        user_id=int(get_jwt_identity()),
    )
    db.session.add(article)
    db.session.commit()

    return jsonify({"message": "文章发布成功", "article": article.to_dict(brief=False)}), 201


@articles_bp.route("/<int:article_id>", methods=["GET"])
def get_article(article_id):
    """获取单篇文章详情"""
    article = Article.query.get_or_404(article_id, description="文章不存在")
    return jsonify({"article": article.to_dict(brief=False)})


@articles_bp.route("/<int:article_id>", methods=["PUT"])
@jwt_required()
def update_article(article_id):
    """更新文章（仅作者可操作）"""
    article = Article.query.get_or_404(article_id, description="文章不存在")

    if article.user_id != int(get_jwt_identity()):
        return jsonify({"error": "无权修改他人的文章"}), 403

    data = request.get_json()
    if not data:
        return jsonify({"error": "请求体不能为空"}), 400

    if "title" in data:
        title = data["title"].strip()
        if not title:
            return jsonify({"error": "标题不能为空"}), 400
        if len(title) > 200:
            return jsonify({"error": "标题不能超过 200 字"}), 400
        article.title = title

    if "content" in data:
        content = data["content"].strip()
        if not content:
            return jsonify({"error": "内容不能为空"}), 400
        article.content = content

    db.session.commit()
    return jsonify({"message": "更新成功", "article": article.to_dict(brief=False)})


@articles_bp.route("/<int:article_id>", methods=["DELETE"])
@jwt_required()
def delete_article(article_id):
    """删除文章（仅作者可操作）"""
    article = Article.query.get_or_404(article_id, description="文章不存在")

    if article.user_id != int(get_jwt_identity()):
        return jsonify({"error": "无权删除他人的文章"}), 403

    db.session.delete(article)
    db.session.commit()
    return jsonify({"message": "删除成功"})
