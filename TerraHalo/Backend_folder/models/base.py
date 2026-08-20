#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SQLAlchemy 基础模块 — db 实例 + 公共 Mixin
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()


class TimestampMixin:
    """自动维护 created_at / updated_at 的 Mixin"""
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class SoftDeleteMixin:
    """软删除 Mixin"""
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
