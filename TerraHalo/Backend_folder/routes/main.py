#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, session
from models import db, User, MaterialSupply, MaterialCategory
from models.product import Product
from utils import require_login, get_current_user

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def home():
    """首页"""
    current_user = get_current_user()
    materials_list = MaterialSupply.query.filter_by(is_available=True, is_deleted=False)\
                                         .filter(MaterialSupply.audit_status == 'approved')\
                                         .order_by(MaterialSupply.created_at.desc())\
                                         .limit(8).all()

    categories = MaterialCategory.query.filter_by(status='active').order_by(MaterialCategory.sort_no).all()

    return render_template('index.html', current_user=current_user,
                           materials=materials_list, categories=categories)


@main_bp.route('/shop')
def shop():
    """有机肥商城"""
    current_user = get_current_user()
    return render_template('shop.html', current_user=current_user)


@main_bp.route('/product/<int:product_id>')
def product_detail(product_id):
    """商品详情"""
    current_user = get_current_user()
    product = Product.query.get(product_id)
    return render_template('product_detail.html', current_user=current_user, product=product)


@main_bp.route('/profile')
@require_login
def profile():
    """个人中心页面"""
    current_user = get_current_user()
    user_id = current_user.id

    if current_user.role_type == 'supplier':
        user_materials = MaterialSupply.query.filter_by(
            publisher_user_id=user_id, is_deleted=False
        ).order_by(MaterialSupply.created_at.desc()).all()
        user_orders = []
    else:
        user_orders = []
        user_materials = []

    return render_template('profile.html', current_user=current_user,
                           user_orders=user_orders, user_materials=user_materials)
