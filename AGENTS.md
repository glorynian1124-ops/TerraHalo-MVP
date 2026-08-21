# TerraHalo (沃土之环) — AGENTS.md

> 农业废弃物资源化利用与商品有机肥交易平台 — Flask 后端 + **TerraHalo-Web 网页端（主界面）** + uni-app（移动端后续）
> ⚠️ **项目主界面 = TerraHalo-Web 网页端（http://localhost:8000）**，通过根目录 `start_dev.bat` 一键启动。后端 `:5000` 的 Jinja 模板为旧界面，非主入口。

## Project

- **What**: Digital platform connecting farmers, fertilizer producers, drivers, and operators for agricultural waste recycling and organic fertilizer commerce.
- **Stack**: Flask 2.3 + SQLAlchemy + bcrypt + Jinja2 (backend); Vue 2/3 + uview-plus + pinia + uni-app (mobile/miniapp); SQLite (dev) → MySQL 8.0 (prod).
- **Entry points**:
  - 🎯 **网页端主界面（推荐）**: `TerraHalo-Web/` → 运行 `start_dev.bat` 后访问 **http://localhost:8000**
  - 后端 API: `TerraHalo/Backend_folder/app.py`（端口 5000，供网页端调用；其 Jinja 模板为旧界面）
  - 移动端（后续）: `TerraHalo/TerraHalo/main.js` (uni-app)

## Commands（快速启动）

```bash
# 🎯 一键启动（推荐）—— 打开网页端主界面
start_dev.bat
# 自动启动 后端(:5000) + 网页端(:8000)，并在浏览器打开 http://localhost:8000

# 手动启动
cd TerraHalo-Web
python -m http.server 8000        # 网页端 → http://localhost:8000
cd ../TerraHalo/Backend_folder
pip install -r requirements.txt
python app.py                     # 后端 API → :5000

# 测试账号
# 管理员 admin/admin123 | 企业 有机肥厂/123456 | 供应商 绿色农场/123456 | 司机 司机小李/123456
```

测试：`cd TerraHalo/Backend_folder && python -m pytest tests`（26 项通过）

## Architecture

```
TerraHalo-Web/              # 🎯 网页端主界面（Tailwind + 原生 JS，对接后端 API）
│   ├── index.html          # 首页
│   ├── login.html          # 登录/注册
│   ├── materials.html      # 原料市场
│   ├── shop.html           # 有机肥商城
│   ├── enterprise.html     # 企业工作台（企业登录后）
│   ├── driver.html         # 司机任务中心
│   ├── admin.html          # 管理总控室（admin 角色）
│   ├── enterprises.html    # 企业情况总览（admin 角色）
│   └── assets/js/api.js    # 统一 API 客户端
TerraHalo/
├── Backend_folder/          # Flask API（网页端数据源）
│   ├── app.py               # create_app(), seed_data(), __main__
│   ├── config.py            # Config classes (dev/prod/test), env vars
│   ├── models/              # SQLAlchemy ORM: user, supply, order, product, logistics, system
│   │   ├── base.py          # db instance + TimestampMixin + SoftDeleteMixin
│   ├── routes/              # Blueprints: main, auth, materials, cart, orders, api, enterprise, driver, admin
│   ├── utils/               # helpers (auth decorators, password hash, matcher)
│   ├── database/            # schema.sql (22 MySQL tables), docs
│   ├── migrations/          # Alembic/Flask-Migrate
│   └── templates/           # Jinja2 SSR pages (index, login, admin, enterprise, driver, …)
├── TerraHalo/               # uni-app cross-platform app (iOS/Android/H5/WeChat)
│   ├── pages/               # Vue SFC pages: index, login, materials, orders, publish, shop, …
│   ├── api/                 # HTTP client modules (auth, cart, materials, orders, …)
│   ├── store/               # Pinia state management
│   └── uni_modules/         # uni-ui components library
├── miniapp/                 # uni-app miniapp variant (mirrors TerraHalo/ structure)
├── Frontend_folder/         # Static HTML placeholders (Admin + User ends)
└── 01_设计文档/             # Design docs: MVP feature list, wireframes, DB schema
```

### Key backend modules

| Module | Role |
|---|---|
| `models/user.py` | User, UserProfile, Enterprise, Driver |
| `models/supply.py` | MaterialCategory, MaterialSupply, MaterialDemand, SupplyDemandMatch |
| `models/order.py` | MaterialOrder, MaterialSignRecord, SettlementBill |
| `models/product.py` | ProductCategory, Product, ProductOrder (e-commerce) |
| `models/logistics.py` | DispatchTask, DispatchTaskLog |
| `models/system.py` | AddressBook, MessageNotice, OperationLog |
| `routes/api.py` | REST API endpoints (largest route file) |
| `routes/enterprise.py` | Enterprise-facing pages + APIs |
| `routes/driver.py` | Driver-facing pages + APIs |
| `routes/admin.py` | Admin pages + APIs |
| `utils/helpers.py` | Auth decorators, password hashing (bcrypt + SHA-256 compat), current_user |
| `utils/matcher.py` | Supply-demand matching algorithm |

### Auth flow
Session-based: login → `session['user_id']` set → `get_current_user()` reads it → `require_login`/`require_role` decorators guard routes. API responses return Chinese error messages with JSON.

## Conventions

- **Python files**: shebang `#!/usr/bin/env python3`, encoding `# -*- coding: utf-8 -*-`, docstring describing module.
- **Blueprint pattern**: Every route module defines a `<name>_bp = Blueprint(...)` and exports via `routes/__init__.py`.
- **ORM models**: Use `db.Model` + `TimestampMixin` + `SoftDeleteMixin` (from `models/base.py`). Mixins provide `created_at`, `updated_at`, `is_deleted`.
- **Password hashing**: `hash_password()` uses bcrypt; `verify_password()` returns `(is_valid, needs_rehash)` for SHA-256 → bcrypt migration.
- **Error format**: `{"error": "中文错误信息"}` with appropriate HTTP status codes.
- **Database**: Defaults to SQLite (`terrahalo.db` in `Backend_folder/`); set `DATABASE_URL` env var for MySQL.
- **Config**: `FLASK_ENV` env var selects config class (`development`/`production`/`testing`), SECRET_KEY from env with dev fallback.
- **No tests** — test infrastructure not yet set up.

## Notes

- Transition from in-memory dicts to SQLAlchemy ORM is complete — old `database.py` reference in docs is stale.
- The `TerraHalo/TerraHalo/` uni-app is based on the `hello-uniapp` template; `miniapp/` is a simplified copy.
- Seed data is created idempotently on first run (checks for `admin` user).
- Environment: Windows (paths use backslashes), Python 3.8+, PowerShell for shell commands.
