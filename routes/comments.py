from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Article, Comment

comments_bp = Blueprint("comments", __name__, url_prefix="/api")


@comments_bp.route("/articles/<int:article_id>/comments", methods=["GET"])
def list_comments(article_id):
    """获取文章的所有评论"""
    article = Article.query.get_or_404(article_id, description="文章不存在")

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)
    page = max(1, page)
    per_page = min(max(1, per_page), 50)

    pagination = (
        Comment.query.filter_by(article_id=article_id)
        .order_by(Comment.created_at.asc())
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return jsonify({
        "comments": [c.to_dict() for c in pagination.items],
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": pagination.total,
            "pages": pagination.pages,
            "has_next": pagination.has_next,
            "has_prev": pagination.has_prev,
        },
    })


@comments_bp.route("/articles/<int:article_id>/comments", methods=["POST"])
@jwt_required()
def create_comment(article_id):
    """发表评论（需登录）"""
    article = Article.query.get_or_404(article_id, description="文章不存在")

    data = request.get_json()
    if not data or not data.get("content", "").strip():
        return jsonify({"error": "评论内容不能为空"}), 400

    content = data["content"].strip()
    if len(content) > 1000:
        return jsonify({"error": "评论不能超过 1000 字"}), 400

    comment = Comment(
        content=content,
        user_id=int(get_jwt_identity()),
        article_id=article_id,
    )
    db.session.add(comment)
    db.session.commit()

    return jsonify({"message": "评论成功", "comment": comment.to_dict()}), 201


@comments_bp.route("/comments/<int:comment_id>", methods=["DELETE"])
@jwt_required()
def delete_comment(comment_id):
    """删除评论（作者或文章作者可操作）"""
    comment = Comment.query.get_or_404(comment_id, description="评论不存在")
    current_user_id = int(get_jwt_identity())

    if comment.user_id != current_user_id and comment.article.user_id != current_user_id:
        return jsonify({"error": "无权删除此评论"}), 403

    db.session.delete(comment)
    db.session.commit()
    return jsonify({"message": "删除成功"})
