#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
商品有机肥电商模型 — ProductCategory / Product / ProductImage / ProductOrder / ProductOrderItem
"""

from .base import db, TimestampMixin, SoftDeleteMixin


class ProductCategory(db.Model):
    __tablename__ = 'product_category'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False)
    parent_id = db.Column(db.Integer, default=0)
    description = db.Column(db.String(256), nullable=True)
    status = db.Column(db.String(20), nullable=False, default='active')


class Product(TimestampMixin, SoftDeleteMixin, db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    enterprise_id = db.Column(db.Integer, db.ForeignKey('enterprise.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('product_category.id'), nullable=True)
    supplier_name = db.Column(db.String(128), nullable=True)  # 冗余企业名
    product_name = db.Column(db.String(128), nullable=False)
    product_code = db.Column(db.String(32), nullable=True)
    specification = db.Column(db.String(64), nullable=True)
    unit = db.Column(db.String(16), default='bag')
    price = db.Column(db.Numeric(10, 2), nullable=False)
    market_price = db.Column(db.Numeric(10, 2), nullable=True)
    stock_qty = db.Column(db.Integer, nullable=False, default=0)
    min_order_qty = db.Column(db.Integer, default=1)
    delivery_scope = db.Column(db.String(256), nullable=True)
    suitable_crops = db.Column(db.String(256), nullable=True)
    detail_content = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='pending_audit')

    category = db.relationship('ProductCategory', backref='products')
    images = db.relationship('ProductImage', backref='product', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'enterprise_id': self.enterprise_id,
            'supplier_name': self.supplier_name,
            'product_name': self.product_name,
            'product_code': self.product_code,
            'specification': self.specification,
            'unit': self.unit,
            'price': float(self.price) if self.price else None,
            'market_price': float(self.market_price) if self.market_price else None,
            'stock_qty': self.stock_qty,
            'min_order_qty': self.min_order_qty,
            'delivery_scope': self.delivery_scope,
            'suitable_crops': self.suitable_crops,
            'detail_content': self.detail_content,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class ProductImage(db.Model):
    __tablename__ = 'product_image'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    image_url = db.Column(db.String(512), nullable=False)
    sort_no = db.Column(db.Integer, default=0)


class ProductOrder(TimestampMixin, SoftDeleteMixin, db.Model):
    __tablename__ = 'product_order'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_no = db.Column(db.String(32), unique=True, nullable=False)
    buyer_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    buyer_type = db.Column(db.String(20), default='farmer')
    enterprise_id = db.Column(db.Integer, db.ForeignKey('enterprise.id'), nullable=False)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    discount_amount = db.Column(db.Numeric(10, 2), default=0)
    freight_amount = db.Column(db.Numeric(10, 2), default=0)
    payable_amount = db.Column(db.Numeric(10, 2), nullable=False)
    pay_status = db.Column(db.String(20), nullable=False, default='unpaid')
    order_status = db.Column(db.String(20), nullable=False, default='pending')
    receiver_name = db.Column(db.String(64), nullable=True)
    receiver_mobile = db.Column(db.String(20), nullable=True)
    receiver_address = db.Column(db.String(256), nullable=True)
    remark = db.Column(db.String(512), nullable=True)

    buyer = db.relationship('User', backref='product_orders', foreign_keys=[buyer_user_id])
    items = db.relationship('ProductOrderItem', backref='order', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'order_no': self.order_no,
            'buyer_user_id': self.buyer_user_id,
            'enterprise_id': self.enterprise_id,
            'total_amount': float(self.total_amount) if self.total_amount else None,
            'payable_amount': float(self.payable_amount) if self.payable_amount else None,
            'pay_status': self.pay_status,
            'order_status': self.order_status,
            'receiver_name': self.receiver_name,
            'receiver_address': self.receiver_address,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class ProductOrderItem(db.Model):
    __tablename__ = 'product_order_item'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('product_order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    product_name = db.Column(db.String(128), nullable=False)
    specification = db.Column(db.String(64), nullable=True)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)

    product = db.relationship('Product', backref='order_items')
