# Blog API

一个基于 Flask 的博客后端 API 项目。

## 技术栈

| 组件 | 技术 | 作用 |
|------|------|------|
| Web 框架 | Flask | HTTP 服务与路由 |
| ORM | Flask-SQLAlchemy | 数据库操作 |
| 认证 | Flask-JWT-Extended | JWT Token 鉴权 |
| 密码 | Werkzeug | 密码哈希存储 |
| 数据库 | SQLite（开发）/ MySQL（生产） | 数据持久化 |

## 快速启动

### 方式一：直接用 Python

```bash
pip install -r requirements.txt
python app.py
# 浏览器打开 http://127.0.0.1:5000
```

### 方式二：使用 Docker（推荐）

```bash
# 构建并启动（默认 SQLite）
docker build -t blog-api .
docker run -d -p 5000:5000 --name blog-api blog-api
```

### 方式三：Docker Compose（MySQL 生产模式）

```bash
docker-compose up -d
# 等待 MySQL 就绪后，访问 http://127.0.0.1:5000
```

## API 接口

### 认证
| 方法 | 路径 | 说明 | 需登录 |
|------|------|------|--------|
| POST | /api/auth/register | 注册 | ❌ |
| POST | /api/auth/login | 登录，返回 Token | ❌ |
| GET  | /api/auth/me | 获取当前用户信息 | ✅ |

### 文章
| 方法 | 路径 | 说明 | 需登录 |
|------|------|------|--------|
| GET  | /api/articles | 文章列表（分页+搜索） | ❌ |
| POST | /api/articles | 创建文章 | ✅ |
| GET  | /api/articles/\<id\> | 文章详情 | ❌ |
| PUT  | /api/articles/\<id\> | 更新文章 | ✅（仅作者） |
| DELETE | /api/articles/\<id\> | 删除文章 | ✅（仅作者） |

### 评论
| 方法 | 路径 | 说明 | 需登录 |
|------|------|------|--------|
| GET  | /api/articles/\<id\>/comments | 评论列表 | ❌ |
| POST | /api/articles/\<id\>/comments | 发表评论 | ✅ |
| DELETE | /api/comments/\<id\> | 删除评论 | ✅ |

### 查询参数

**文章列表** `GET /api/articles?page=1&per_page=10&search=关键词`

## 切换到 MySQL

```bash
# 安装 MySQL 驱动
pip install pymysql

# 设置环境变量后启动
set DATABASE_URL=mysql+pymysql://root:你的密码@localhost/blog
python app.py
```

## 项目结构

```
blog-api/
├── app.py              # 应用入口
├── wsgi.py             # gunicorn 生产入口
├── config.py           # 配置
├── models.py           # 数据模型（User / Article / Comment）
├── routes/
│   ├── auth.py         # 认证接口
│   ├── articles.py     # 文章接口
│   └── comments.py     # 评论接口
├── Dockerfile          # Docker 构建
├── docker-compose.yml  # Docker Compose（MySQL 模式）
├── requirements.txt
└── README.md
```
