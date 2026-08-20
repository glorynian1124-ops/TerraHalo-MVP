#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, session
from models import db, MaterialOrder, MaterialSupply
from utils import require_login, get_current_user

orders_bp = Blueprint('orders', __name__)


@orders_bp.route('/orders')
@require_login
def orders_page():
    """我的订单页面"""
    current_user = get_current_user()
    user_orders = []

    # TODO: 订单模型需要调整以支持当前业务逻辑
    # 目前 MaterialOrder 与 MaterialSupply 通过 supply_id 关联
    # 旧逻辑按 buyer_id / seller 区分，新模型待订单系统完善

    return render_template('orders.html', current_user=current_user, user_orders=user_orders)
