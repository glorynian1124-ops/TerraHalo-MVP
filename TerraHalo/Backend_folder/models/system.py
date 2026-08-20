#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用系统模型 — AddressBook / MessageNotice / OperationLog
"""

from .base import db


class AddressBook(db.Model):
    __tablename__ = 'address_book'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    contact_name = db.Column(db.String(64), nullable=False)
    contact_mobile = db.Column(db.String(20), nullable=False)
    province = db.Column(db.String(32), nullable=True)
    city = db.Column(db.String(32), nullable=True)
    district = db.Column(db.String(32), nullable=True)
    detail_address = db.Column(db.String(256), nullable=False)
    lat = db.Column(db.Numeric(10, 6), nullable=True)
    lng = db.Column(db.Numeric(10, 6), nullable=True)
    is_default = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'contact_name': self.contact_name,
            'contact_mobile': self.contact_mobile,
            'province': self.province,
            'city': self.city,
            'district': self.district,
            'detail_address': self.detail_address,
            'is_default': self.is_default,
        }


class MessageNotice(db.Model):
    __tablename__ = 'message_notice'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    biz_type = db.Column(db.String(20), nullable=True)
    biz_id = db.Column(db.Integer, nullable=True)
    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.Text, nullable=True)
    read_status = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)


class OperationLog(db.Model):
    __tablename__ = 'operation_log'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    operator_user_id = db.Column(db.Integer, nullable=False)
    biz_type = db.Column(db.String(20), nullable=True)
    biz_id = db.Column(db.Integer, nullable=True)
    action = db.Column(db.String(32), nullable=False)
    content = db.Column(db.String(512), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
