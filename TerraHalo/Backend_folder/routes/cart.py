#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, session
from models import db, MaterialSupply
from utils import require_login, get_current_user

cart_bp = Blueprint('cart', __name__)

# 临时购物车存储（session 级别，后续迁移到 CartItem 表）
# 格式: session['cart'] = [{"material_id": int, "quantity": int}, ...]


@cart_bp.route('/cart')
@require_login
def cart_page():
    """购物车页面"""
    current_user = get_current_user()
    cart_data = session.get('cart', [])
    cart_items = []
    total_price = 0

    for item in cart_data:
        material = MaterialSupply.query.get(item['material_id'])
        if material and material.is_available:
            item_total = float(material.price or 0) * item['quantity']
            cart_items.append({
                'material_id': material.id,
                'type': material.type,
                'quantity': item['quantity'],
                'price': float(material.price or 0),
                'supplier_id': material.publisher_user_id,
                'supplier_name': material.supplier_name,
            })
            total_price += item_total

    return render_template('cart.html', current_user=current_user,
                           cart_items=cart_items, total_price=total_price)
