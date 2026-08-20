#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调度物流模型 — DispatchTask / DispatchTaskLog
"""

from .base import db, TimestampMixin


class DispatchTask(TimestampMixin, db.Model):
    __tablename__ = 'dispatch_task'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_no = db.Column(db.String(32), unique=True, nullable=False)
    match_id = db.Column(db.Integer, db.ForeignKey('supply_demand_match.id'), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'), nullable=False)
    vehicle_no = db.Column(db.String(32), nullable=True)
    pickup_address = db.Column(db.String(256), nullable=False)
    pickup_lat = db.Column(db.Numeric(10, 6), nullable=True)
    pickup_lng = db.Column(db.Numeric(10, 6), nullable=True)
    delivery_address = db.Column(db.String(256), nullable=False)
    delivery_lat = db.Column(db.Numeric(10, 6), nullable=True)
    delivery_lng = db.Column(db.Numeric(10, 6), nullable=True)
    planned_pickup_time = db.Column(db.DateTime, nullable=True)
    actual_pickup_time = db.Column(db.DateTime, nullable=True)
    actual_arrival_time = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='pending_assign')
    route_distance_km = db.Column(db.Numeric(8, 2), nullable=True)
    transport_fee = db.Column(db.Numeric(10, 2), nullable=True)
    remark = db.Column(db.String(512), nullable=True)

    logs = db.relationship('DispatchTaskLog', backref='task', lazy=True,
                            order_by='DispatchTaskLog.created_at')

    def to_dict(self):
        return {
            'id': self.id,
            'task_no': self.task_no,
            'match_id': self.match_id,
            'driver_id': self.driver_id,
            'vehicle_no': self.vehicle_no,
            'pickup_address': self.pickup_address,
            'delivery_address': self.delivery_address,
            'status': self.status,
            'transport_fee': float(self.transport_fee) if self.transport_fee else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class DispatchTaskLog(db.Model):
    __tablename__ = 'dispatch_task_log'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_id = db.Column(db.Integer, db.ForeignKey('dispatch_task.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    operator_user_id = db.Column(db.Integer, nullable=False)
    operator_role = db.Column(db.String(20), nullable=False)
    content = db.Column(db.String(512), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
