#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
订单与结算模型 — MaterialOrder / MaterialSignRecord / SettlementBill
"""

from .base import db, TimestampMixin, SoftDeleteMixin


class MaterialOrder(TimestampMixin, SoftDeleteMixin, db.Model):
    __tablename__ = 'material_order'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_no = db.Column(db.String(32), unique=True, nullable=False)
    supply_id = db.Column(db.Integer, db.ForeignKey('material_supply.id'), nullable=False)
    demand_id = db.Column(db.Integer, db.ForeignKey('material_demand.id'), nullable=False)
    enterprise_id = db.Column(db.Integer, db.ForeignKey('enterprise.id'), nullable=False)
    seller_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('material_category.id'), nullable=False)
    estimated_weight = db.Column(db.Numeric(10, 2), nullable=False)
    actual_weight = db.Column(db.Numeric(10, 2), nullable=True)
    unit_price = db.Column(db.Numeric(10, 2), nullable=True)
    goods_amount = db.Column(db.Numeric(10, 2), nullable=True)
    transport_fee = db.Column(db.Numeric(10, 2), nullable=True)
    platform_service_fee = db.Column(db.Numeric(10, 2), nullable=True)
    subsidy_amount = db.Column(db.Numeric(10, 2), default=0)
    settlement_amount = db.Column(db.Numeric(10, 2), nullable=True)
    status = db.Column(db.String(20), nullable=False, default='pending_confirm')
    completed_at = db.Column(db.DateTime, nullable=True)
    cancel_reason = db.Column(db.String(256), nullable=True)

    supply = db.relationship('MaterialSupply', backref='orders')
    enterprise = db.relationship('Enterprise', backref='material_orders')
    seller = db.relationship('User', backref='sale_orders', foreign_keys=[seller_user_id])
    sign_records = db.relationship('MaterialSignRecord', backref='order', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'order_no': self.order_no,
            'supply_id': self.supply_id,
            'enterprise_id': self.enterprise_id,
            'seller_user_id': self.seller_user_id,
            'driver_id': self.driver_id,
            'estimated_weight': float(self.estimated_weight) if self.estimated_weight else None,
            'actual_weight': float(self.actual_weight) if self.actual_weight else None,
            'unit_price': float(self.unit_price) if self.unit_price else None,
            'goods_amount': float(self.goods_amount) if self.goods_amount else None,
            'transport_fee': float(self.transport_fee) if self.transport_fee else None,
            'platform_service_fee': float(self.platform_service_fee) if self.platform_service_fee else None,
            'subsidy_amount': float(self.subsidy_amount) if self.subsidy_amount else 0,
            'settlement_amount': float(self.settlement_amount) if self.settlement_amount else None,
            'status': self.status,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class MaterialSignRecord(db.Model):
    __tablename__ = 'material_sign_record'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('material_order.id'), nullable=False)
    pickup_photo_url = db.Column(db.String(512), nullable=True)
    delivery_photo_url = db.Column(db.String(512), nullable=True)
    pickup_weight = db.Column(db.Numeric(10, 2), nullable=True)
    delivery_weight = db.Column(db.Numeric(10, 2), nullable=True)
    sign_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sign_time = db.Column(db.DateTime, nullable=True)
    remark = db.Column(db.String(256), nullable=True)


class SettlementBill(TimestampMixin, db.Model):
    __tablename__ = 'settlement_bill'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bill_no = db.Column(db.String(32), unique=True, nullable=False)
    biz_type = db.Column(db.String(20), nullable=False)
    biz_order_id = db.Column(db.Integer, nullable=False)
    payer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    payee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    fee_amount = db.Column(db.Numeric(10, 2), default=0)
    subsidy_amount = db.Column(db.Numeric(10, 2), default=0)
    settle_status = db.Column(db.String(20), nullable=False, default='pending')
    settle_time = db.Column(db.DateTime, nullable=True)
    remark = db.Column(db.String(256), nullable=True)
