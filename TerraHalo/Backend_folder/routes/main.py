#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, session
from models import db, User, MaterialSupply, MaterialCategory
from models.product import Product
from utils import require_login, get_current_user

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def home():
    """后端根路径：提示网页端主界面入口（本服务为 API，前端页面在 TerraHalo-Web）"""
    return (
        '<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
        '<title>沃土之环 - 后端 API 服务</title>'
        '<style>body{margin:0;font-family:-apple-system,"Segoe UI","Microsoft YaHei",sans-serif;'
        'background:linear-gradient(135deg,#155724,#1e7e34);color:#fff;min-height:100vh;'
        'display:flex;align-items:center;justify-content:center;text-align:center}'
        '.b{max-width:580px;padding:40px 24px}h1{font-size:1.6rem;margin:0 0 12px}'
        'p{opacity:.9;line-height:1.7}a{color:#fff;font-weight:700}code{background:rgba(255,255,255,.15);'
        'padding:2px 8px;border-radius:6px}</style></head><body>'
        '<div class="b"><h1>🌱 沃土之环 · 后端 API 服务</h1>'
        '<p>本地址（<code>:5000</code>）是后端 API 接口服务，不提供前端界面。</p>'
        '<p>🎯 网页端主界面请访问：<a href="http://localhost:8000">http://localhost:8000</a><br>'
        '（请先运行根目录 <code>start_dev.bat</code> 一键启动）</p></div></body></html>'
    )


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
