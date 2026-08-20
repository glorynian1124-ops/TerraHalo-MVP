#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户与组织模型 — User / UserProfile / Enterprise / Driver
"""

from .base import db, TimestampMixin, SoftDeleteMixin


class User(TimestampMixin, SoftDeleteMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True, nullable=False)  # 登录名
    mobile = db.Column(db.String(20), unique=True, nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    wechat_openid = db.Column(db.String(128), unique=True, nullable=True)
    role_type = db.Column(db.String(20), nullable=False, default='farmer')
    real_name = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(128), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    avatar = db.Column(db.String(512), nullable=True)
    company = db.Column(db.String(128), nullable=True)
    address = db.Column(db.String(256), nullable=True)
    balance = db.Column(db.Numeric(12, 2), default=0)
    credit_score = db.Column(db.Integer, default=80)
    is_verified = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), nullable=False, default='normal')
    last_login_at = db.Column(db.DateTime, nullable=True)

    # 关系
    profile = db.relationship('UserProfile', backref='user', uselist=False, lazy=True)
    enterprise = db.relationship('Enterprise', backref='user', uselist=False, lazy=True)
    driver = db.relationship('Driver', backref='user', uselist=False, lazy=True)
    supplies = db.relationship('MaterialSupply', backref='publisher', lazy=True,
                                foreign_keys='MaterialSupply.publisher_user_id')
    addresses = db.relationship('AddressBook', backref='user', lazy=True)
    messages = db.relationship('MessageNotice', backref='user', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'mobile': self.mobile,
            'wechat_openid': self.wechat_openid,
            'role_type': self.role_type,
            'real_name': self.real_name,
            'email': self.email,
            'phone': self.phone,
            'avatar': self.avatar,
            'company': self.company,
            'address': self.address,
            'balance': float(self.balance) if self.balance else 0,
            'credit_score': self.credit_score,
            'is_verified': self.is_verified,
            'status': self.status,
            'last_login_at': self.last_login_at.isoformat() if self.last_login_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class UserProfile(db.Model):
    __tablename__ = 'user_profile'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    avatar = db.Column(db.String(512), nullable=True)
    gender = db.Column(db.SmallInteger, default=0)
    province = db.Column(db.String(32), nullable=True)
    city = db.Column(db.String(32), nullable=True)
    district = db.Column(db.String(32), nullable=True)
    detail_address = db.Column(db.String(256), nullable=True)
    lat = db.Column(db.Numeric(10, 6), nullable=True)
    lng = db.Column(db.Numeric(10, 6), nullable=True)
    village_name = db.Column(db.String(64), nullable=True)
    remark = db.Column(db.String(512), nullable=True)


class Enterprise(TimestampMixin, db.Model):
    __tablename__ = 'enterprise'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    enterprise_name = db.Column(db.String(128), nullable=False)
    enterprise_type = db.Column(db.String(32), nullable=True)
    license_no = db.Column(db.String(64), nullable=True)
    contact_name = db.Column(db.String(64), nullable=True)
    contact_mobile = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(256), nullable=True)
    lat = db.Column(db.Numeric(10, 6), nullable=True)
    lng = db.Column(db.Numeric(10, 6), nullable=True)
    service_radius_km = db.Column(db.Integer, default=50)
    audit_status = db.Column(db.String(20), nullable=False, default='pending')
    audit_remark = db.Column(db.String(512), nullable=True)

    demands = db.relationship('MaterialDemand', backref='enterprise', lazy=True)
    products = db.relationship('Product', backref='enterprise', lazy=True)


class Driver(TimestampMixin, db.Model):
    __tablename__ = 'driver'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    vehicle_type = db.Column(db.String(32), nullable=True)
    vehicle_no = db.Column(db.String(32), nullable=True)
    vehicle_capacity_ton = db.Column(db.Numeric(6, 2), nullable=True)
    id_card_no = db.Column(db.String(32), nullable=True)
    driving_license_url = db.Column(db.String(512), nullable=True)
    audit_status = db.Column(db.String(20), nullable=False, default='pending')

    tasks = db.relationship('DispatchTask', backref='driver', lazy=True)
