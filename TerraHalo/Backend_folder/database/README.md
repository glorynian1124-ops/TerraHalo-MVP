# 沃土之环 - 数据库设计

## 目录内容

| 文件 | 说明 |
| --- | --- |
| `schema.sql` | MySQL 建表脚本（22 张核心表） |
| `README.md` | 本文件 |

## 当前状态

- **运行时存储**: 内存字典模拟（`models/database.py`），用于快速原型开发
- **目标数据库**: MySQL 8.0+
- **ORM 计划**: SQLAlchemy

## 快速使用

```bash
mysql -u root -p < schema.sql
```

## 表清单（按模块）

| 模块 | 表名 | 说明 |
| --- | --- | --- |
| 用户 | `user` | 用户主表 |
| 用户 | `user_profile` | 用户资料（地址、经纬度） |
| 用户 | `enterprise` | 企业资质 |
| 用户 | `driver` | 司机与车辆信息 |
| 标准库 | `material_category` | 原料品类 |
| 标准库 | `material_grade_rule` | 原料分级规则 |
| 标准库 | `product_category` | 商品分类 |
| 供需 | `material_supply` | 原料供给单 |
| 供需 | `material_supply_image` | 供给图片 |
| 供需 | `material_demand` | 原料需求单 |
| 匹配 | `supply_demand_match` | 供需匹配记录 |
| 调度 | `dispatch_task` | 调度任务 |
| 调度 | `dispatch_task_log` | 任务状态日志 |
| 订单 | `material_order` | 原料订单 |
| 订单 | `material_sign_record` | 签收记录 |
| 结算 | `settlement_bill` | 结算账单 |
| 电商 | `product` | 商品上架 |
| 电商 | `product_image` | 商品图片 |
| 电商 | `product_order` | 商品订单 |
| 电商 | `product_order_item` | 商品订单明细 |
| 通用 | `address_book` | 地址簿 |
| 通用 | `message_notice` | 消息通知 |
| 通用 | `operation_log` | 操作日志 |

## 下一步

1. 引入 SQLAlchemy，实现 ORM 模型类 → 替换 `models/database.py` 中的内存字典
2. 编写 Alembic 迁移脚本
3. 添加种子数据脚本（地区、品类、测试用户）
