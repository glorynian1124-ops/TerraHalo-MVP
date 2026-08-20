#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
供需模型 — MaterialCategory / MaterialGradeRule / MaterialSupply / MaterialSupplyImage / MaterialDemand / SupplyDemandMatch
"""

from .base import db, TimestampMixin, SoftDeleteMixin


class MaterialCategory(db.Model):
    __tablename__ = 'material_category'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False)
    parent_id = db.Column(db.Integer, default=0)
    code = db.Column(db.String(32), nullable=True)
    description = db.Column(db.String(256), nullable=True)
    status = db.Column(db.String(20), nullable=False, default='active')
    sort_no = db.Column(db.Integer, default=0)


class MaterialGradeRule(db.Model):
    __tablename__ = 'material_grade_rule'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_id = db.Column(db.Integer, db.ForeignKey('material_category.id'), nullable=False)
    grade_name = db.Column(db.String(64), nullable=False)
    moisture_min = db.Column(db.Numeric(5, 2), nullable=True)
    moisture_max = db.Column(db.Numeric(5, 2), nullable=True)
    impurity_desc = db.Column(db.String(256), nullable=True)
    price_reference_min = db.Column(db.Numeric(10, 2), nullable=True)
    price_reference_max = db.Column(db.Numeric(10, 2), nullable=True)
    transport_note = db.Column(db.String(256), nullable=True)
    status = db.Column(db.String(20), nullable=False, default='active')

    category = db.relationship('MaterialCategory', backref='grade_rules')


class MaterialSupply(TimestampMixin, SoftDeleteMixin, db.Model):
    __tablename__ = 'material_supply'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    supply_no = db.Column(db.String(32), unique=True, nullable=False)
    publisher_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    publisher_type = db.Column(db.String(20), default='farmer')
    category_id = db.Column(db.Integer, db.ForeignKey('material_category.id'), nullable=True)
    # 兼容旧字段
    type = db.Column(db.String(64), nullable=True)            # 原料类型名
    price = db.Column(db.Numeric(10, 2), nullable=True)       # 单价
    description = db.Column(db.String(512), nullable=True)     # 描述
    rating = db.Column(db.Float, default=0)                    # 评分
    review_count = db.Column(db.Integer, default=0)            # 评价数
    is_available = db.Column(db.Boolean, default=True)         # 是否上架
    supplier_name = db.Column(db.String(64), nullable=True)    # 冗余供应商名
    quantity = db.Column(db.Numeric(10, 2), nullable=True)     # 兼容旧 quantity
    location = db.Column(db.String(128), nullable=True)        # 兼容旧 location
    organic_matter = db.Column(db.String(32), nullable=True)   # 有机质含量
    moisture = db.Column(db.String(32), nullable=True)         # 含水率
    # MVP 标准字段
    estimated_weight = db.Column(db.Numeric(10, 2), nullable=True)
    weight_unit = db.Column(db.String(8), default='kg')
    estimated_volume = db.Column(db.Numeric(10, 2), nullable=True)
    moisture_range = db.Column(db.String(32), nullable=True)
    impurity_desc = db.Column(db.String(256), nullable=True)
    packaging_type = db.Column(db.String(32), nullable=True)
    loadable_flag = db.Column(db.Boolean, default=True)
    available_start_time = db.Column(db.DateTime, nullable=True)
    available_end_time = db.Column(db.DateTime, nullable=True)
    province = db.Column(db.String(32), nullable=True)
    city = db.Column(db.String(32), nullable=True)
    district = db.Column(db.String(32), nullable=True)
    detail_address = db.Column(db.String(256), nullable=True)
    lat = db.Column(db.Numeric(10, 6), nullable=True)
    lng = db.Column(db.Numeric(10, 6), nullable=True)
    status = db.Column(db.String(20), nullable=False, default='pending_audit')
    audit_status = db.Column(db.String(20), nullable=False, default='pending')
    audit_user_id = db.Column(db.Integer, nullable=True)
    audit_time = db.Column(db.DateTime, nullable=True)
    remark = db.Column(db.String(512), nullable=True)

    category = db.relationship('MaterialCategory', backref='supplies')
    images = db.relationship('MaterialSupplyImage', backref='supply', lazy=True)
    matches = db.relationship('SupplyDemandMatch', backref='supply', lazy=True,
                               foreign_keys='SupplyDemandMatch.supply_id')

    def to_dict(self):
        return {
            'id': self.id,
            'supply_no': self.supply_no,
            'supplier_id': self.publisher_user_id,
            'supplier_name': self.supplier_name,
            'publisher_user_id': self.publisher_user_id,
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else None,
            'type': self.type,
            'quantity': float(self.quantity) if self.quantity else None,
            'location': self.location,
            'price': float(self.price) if self.price else None,
            'description': self.description,
            'moisture': self.moisture,
            'organic_matter': self.organic_matter,
            'is_available': self.is_available,
            'rating': self.rating,
            'review_count': self.review_count,
            # MVP 标准字段
            'estimated_weight': float(self.estimated_weight) if self.estimated_weight else None,
            'weight_unit': self.weight_unit,
            'estimated_volume': float(self.estimated_volume) if self.estimated_volume else None,
            'moisture_range': self.moisture_range,
            'impurity_desc': self.impurity_desc,
            'packaging_type': self.packaging_type,
            'loadable_flag': self.loadable_flag,
            'available_start_time': self.available_start_time.isoformat() if self.available_start_time else None,
            'available_end_time': self.available_end_time.isoformat() if self.available_end_time else None,
            'province': self.province,
            'city': self.city,
            'district': self.district,
            'detail_address': self.detail_address,
            'lat': float(self.lat) if self.lat else None,
            'lng': float(self.lng) if self.lng else None,
            'status': self.status,
            'audit_status': self.audit_status,
            'remark': self.remark,
            'images': [img.image_url for img in (self.images or [])],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }


class MaterialSupplyImage(db.Model):
    __tablename__ = 'material_supply_image'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    supply_id = db.Column(db.Integer, db.ForeignKey('material_supply.id'), nullable=False)
    image_url = db.Column(db.String(512), nullable=False)
    sort_no = db.Column(db.Integer, default=0)


class MaterialDemand(TimestampMixin, SoftDeleteMixin, db.Model):
    __tablename__ = 'material_demand'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    demand_no = db.Column(db.String(32), unique=True, nullable=False)
    enterprise_id = db.Column(db.Integer, db.ForeignKey('enterprise.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('material_category.id'), nullable=True)
    category_name = db.Column(db.String(64), nullable=True)  # 品类名，用于匹配供给.type
    target_weight = db.Column(db.Numeric(10, 2), nullable=False)
    min_weight = db.Column(db.Numeric(10, 2), nullable=True)
    quality_requirement = db.Column(db.String(256), nullable=True)
    purchase_radius_km = db.Column(db.Integer, default=50)
    expected_price_min = db.Column(db.Numeric(10, 2), nullable=True)
    expected_price_max = db.Column(db.Numeric(10, 2), nullable=True)
    delivery_requirement = db.Column(db.String(256), nullable=True)
    expected_start_time = db.Column(db.DateTime, nullable=True)
    expected_end_time = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='pending_audit')
    remark = db.Column(db.String(512), nullable=True)

    category = db.relationship('MaterialCategory', backref='demands')
    matches = db.relationship('SupplyDemandMatch', backref='demand', lazy=True,
                               foreign_keys='SupplyDemandMatch.demand_id')


class SupplyDemandMatch(TimestampMixin, db.Model):
    __tablename__ = 'supply_demand_match'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    supply_id = db.Column(db.Integer, db.ForeignKey('material_supply.id'), nullable=False)
    demand_id = db.Column(db.Integer, db.ForeignKey('material_demand.id'), nullable=False)
    match_score = db.Column(db.Numeric(5, 2), nullable=True)
    match_type = db.Column(db.String(20), default='auto')
    distance_km = db.Column(db.Numeric(8, 2), nullable=True)
    status = db.Column(db.String(20), nullable=False, default='pending')
    operator_user_id = db.Column(db.Integer, nullable=True)
    remark = db.Column(db.String(512), nullable=True)

    tasks = db.relationship('DispatchTask', backref='match', lazy=True)
