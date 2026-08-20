#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模型层 — 统一导出
过渡期：同时保留旧内存字典（database.py）和新 SQLAlchemy 模型
路由迁移完成后将删除 database.py
"""

# === SQLAlchemy 基础 ===
from .base import db, TimestampMixin, SoftDeleteMixin

# === SQLAlchemy 模型 ===
from .user import User, UserProfile, Enterprise, Driver
from .supply import (
    MaterialCategory, MaterialGradeRule,
    MaterialSupply, MaterialSupplyImage,
    MaterialDemand, SupplyDemandMatch
)
from .order import MaterialOrder, MaterialSignRecord, SettlementBill
from .product import (
    ProductCategory, Product, ProductImage,
    ProductOrder, ProductOrderItem
)
from .logistics import DispatchTask, DispatchTaskLog
from .system import AddressBook, MessageNotice, OperationLog
from .review import Review
from .review import Review

__all__ = [
    # 基础
    "db", "TimestampMixin", "SoftDeleteMixin",
    # SQLAlchemy 模型
    "User", "UserProfile", "Enterprise", "Driver",
    "MaterialCategory", "MaterialGradeRule",
    "MaterialSupply", "MaterialSupplyImage",
    "MaterialDemand", "SupplyDemandMatch",
    "MaterialOrder", "MaterialSignRecord", "SettlementBill",
    "ProductCategory", "Product", "ProductImage",
    "ProductOrder", "ProductOrderItem",
    "DispatchTask", "DispatchTaskLog",
    "AddressBook", "MessageNotice", "OperationLog",
    "Review",
]
