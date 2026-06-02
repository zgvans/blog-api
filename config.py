import os

class Config:
    """应用配置"""
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "jwt-secret-change-in-production!!")

    # 默认使用 SQLite（零配置可运行）
    # 生产环境可通过环境变量 DATABASE_URL 切换到 MySQL
    # 示例: DATABASE_URL=mysql+pymysql://root:password@localhost/blog
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///blog.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = 7 * 24 * 3600  # token 有效期 7 天
