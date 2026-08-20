# TerraHalo (沃土之环) — AGENTS.md

> Agricultural waste recycling & organic fertilizer trading platform — Flask backend + uni-app frontend, MVP ~15-20%.

## Project

- **What**: Digital platform connecting farmers, fertilizer producers, drivers, and operators for agricultural waste recycling and organic fertilizer commerce.
- **Stack**: Flask 2.3 + SQLAlchemy + bcrypt + Jinja2 (backend); Vue 2/3 + uview-plus + pinia + uni-app (mobile/miniapp); SQLite (dev) → MySQL 8.0 (prod).
- **Entry points**: `TerraHalo/Backend_folder/app.py` (Flask API), `TerraHalo/TerraHalo/main.js` (uni-app), `TerraHalo/miniapp/main.js` (miniapp variant).

## Commands

```bash
# Backend
cd TerraHalo/Backend_folder
pip install -r requirements.txt   # install deps
python app.py                     # start dev server on :5000
flask db upgrade                  # run Alembic migrations (via Flask-Migrate)

# uni-app (requires HBuilderX or uni-app CLI)
cd TerraHalo/TerraHalo
npm install                       # install deps
# Build/distribute via HBuilderX IDE or uni-app CLI
```

No test suite exists yet.

## Architecture

```
TerraHalo/
├── Backend_folder/          # Flask API + SSR (Jinja2 templates)
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
