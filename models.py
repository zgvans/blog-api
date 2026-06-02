from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """用户模型"""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    articles = db.relationship("Article", backref="author", lazy="dynamic")
    comments = db.relationship("Comment", backref="author", lazy="dynamic")

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M"),
        }


class Article(db.Model):
    """文章模型"""
    __tablename__ = "articles"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    comments = db.relationship(
        "Comment", backref="article", lazy="dynamic", cascade="all, delete-orphan"
    )

    def to_dict(self, brief=True):
        data = {
            "id": self.id,
            "title": self.title,
            "author": self.author.username,
            "author_id": self.user_id,
            "comment_count": self.comments.count(),
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M"),
        }
        if brief:
            # 列表页只显示前 200 字
            data["content"] = (
                self.content[:200] + "..."
                if len(self.content) > 200
                else self.content
            )
        else:
            data["content"] = self.content
        return data


class Comment(db.Model):
    """评论模型"""
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey("articles.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "author": self.author.username,
            "author_id": self.user_id,
            "article_id": self.article_id,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M"),
        }
