# 🌱 沃土之环 (TerraHalo)

> 农业废弃物资源化利用与商品有机肥交易的数字化服务平台

## 项目简介

沃土之环连接四方角色，打造从农业废弃物回收到商品有机肥销售的全链路数字化平台：

| 角色 | 职责 |
| --- | --- |
| 🧑‍🌾 农户/养殖户 | 发布农业废弃物供给（畜禽粪便、秸秆等） |
| 🏭 有机肥生产企业 | 发布采购需求、购买原料、上架商品有机肥 |
| 🚛 司机/承运方 | 接单、运输、到场打卡、签收 |
| 🔧 平台运营 | 审核、匹配供给与需求、调度派单、结算 |

**当前阶段**：MVP 核心闭环已跑通（约 50%）。Flask 后端 API 完整可运行（26 项测试通过）；网页端 `TerraHalo-Web` 已接入真实后端 API（登录/注册、原料市场、有机肥商城、商品下单），数据来自 SQLite/MySQL 数据库。

**架构定位**：一套后端 + 多端前端。Flask 后端是唯一数据源（REST API + SQLAlchemy + MySQL），网页端 / APP / 小程序均为客户端，共享同一套后端 API。

## 🚀 快速进入（网页端主界面）

```bash
start_dev.bat        # 一键启动 后端(:5000) + 网页端(:8000)，并自动打开浏览器
```

**浏览器访问 http://localhost:8000** ← 项目主界面（`TerraHalo-Web` 网页端）

| 入口 | 地址 | 说明 |
| --- | --- | --- |
| 🎯 网页端主界面 | http://localhost:8000 | TerraHalo-Web（推荐） |
| 🔧 管理总控室 | http://localhost:8000/admin.html | admin 角色 |
| 🏭 企业情况 | http://localhost:8000/enterprises.html | admin 角色 |
| ⚙️ 后端 API | http://localhost:5000 | Flask API（其 Jinja 模板为旧界面） |

> ⚠️ 提示：`TerraHalo/Backend_folder/templates` 下的 Jinja 页面为**旧版界面**，不是项目主入口。

## 目录结构

```
.
├── README.md                      # 本文件
├── .gitignore                     # Python/Flask 忽略规则
├── index.html                     # 自动跳转到网页端主界面
├── TerraHalo-Web/                 # 🎯 网页端主界面（对接后端 API）
└── TerraHalo/
    ├── 01_设计文档/                # MVP 功能清单、线框图、数据库设计
    │   ├── 沃土之环_MVP功能清单_页面结构图_数据库核心表设计.md
    │   ├── 沃土之环_页面原型说明书_框架结构图.md
    │   └── 沃土之环_低保真线框图说明.md
    ├── Backend_folder/            # Flask 后端
    │   ├── app.py                 # 应用入口
    │   ├── config.py              # 配置模块
    │   ├── requirements.txt       # Python 依赖
    │   ├── models/                # 数据模型（当前为内存字典）
    │   ├── routes/                # 路由蓝图（main/auth/materials/cart/orders/api）
    │   ├── templates/             # Jinja2 服务端渲染模板
    │   ├── static/                # 静态资源
    │   ├── utils/                 # 工具函数（认证/加密/装饰器）
    │   └── database/              # 数据库设计文档与 SQL 脚本
    ├── Frontend_folder/           # 前端占位页（待替换为小程序/React）
    │   ├── Admin_folder/          # 管理端（Desktop/Mobile/Web）
    │   └── User_folder/           # 用户端（农户/企业/司机）
```

## 快速启动

### 环境要求

- Python 3.8+
- pip

### 一键启动（推荐）

```bash
start_dev.bat
```

自动打开两个终端：Flask 后端（:5000）+ 网页端静态服务器（:8000），浏览器访问 **http://localhost:8000**。

### 手动启动

```bash
# 终端 1：后端
cd TerraHalo/Backend_folder
pip install -r requirements.txt
python app.py            # http://localhost:5000

# 终端 2：网页端静态服务器
cd TerraHalo-Web
python -m http.server 8000   # http://localhost:8000
```

### 测试账号

| 角色 | 用户名 | 密码 |
| --- | --- | --- |
| 🔧 管理员 | admin | admin123 |
| 📦 供应商/农户 | 绿色农场 | 123456 |
| 🏭 企业 | 有机肥厂 | 123456 |
| 🚛 司机 | 司机小李 | 123456 |

## 技术栈

| 层 | 当前 | 说明 |
| --- | --- | --- |
| 后端框架 | Flask 2.3 | REST API + CORS（支持跨端口 cookie） |
| 数据库 | SQLAlchemy + SQLite（开发）/ MySQL 8.0（生产） | 22 张表 schema.sql 就绪 |
| 网页端 | TerraHalo-Web（Tailwind + Lucide + fetch） | 已接入真实后端 API |
| 移动端 | uni-app（TerraHalo/ 工程，后续开发） | 复用同一套后端 API |
| 认证 | Session-cookie（bcrypt 密码哈希） | 网页/APP/小程序共享后端会话 |

## 开发路线（按 MVP 六阶段）

1. ✅ 用户/认证 + 供给发布 + 需求发布 + 后台审核（约 90%）
2. ⬜ 供需匹配 + 派单 + 运输 + 原料订单（后端约 85%，网页端待接入）
3. ✅ 商品上架 + 商品订单 + 基础结算（网页端订单闭环已跑通）
4. ⬜ 数据看板 + 消息通知 + 评价反馈 + 补贴台账（约 40%）

详见 `TerraHalo/01_设计文档/` 中的 MVP 功能清单。
