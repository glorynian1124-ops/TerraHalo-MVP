#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""评价模型 — Review"""

from .base import db, TimestampMixin


class Review(TimestampMixin, db.Model):
    __tablename__ = 'review'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reviewee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_id = db.Column(db.Integer, nullable=True)
    order_type = db.Column(db.String(20), default='material')  # 'material' or 'product'
    rating = db.Column(db.Integer, nullable=False)  # 1-5
    content = db.Column(db.String(512), nullable=True)

    reviewer = db.relationship('User', foreign_keys=[reviewer_id], backref='reviews_given')
    reviewee = db.relationship('User', foreign_keys=[reviewee_id], backref='reviews_received')

    def to_dict(self):
        return {
            'id': self.id,
            'reviewer_id': self.reviewer_id,
            'reviewee_id': self.reviewee_id,
            'order_id': self.order_id,
            'order_type': self.order_type,
            'rating': self.rating,
            'content': self.content,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
