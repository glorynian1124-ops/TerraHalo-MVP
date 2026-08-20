#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, session
from models import db, MaterialSupply, MaterialCategory
from utils import require_login, require_role, get_current_user

materials_bp = Blueprint('materials', __name__)


@materials_bp.route('/materials')
def materials_page():
    """原料市场页面"""
    current_user = get_current_user()
    categories = MaterialCategory.query.filter_by(status='active').order_by(MaterialCategory.sort_no).all()
    return render_template('materials.html', current_user=current_user, categories=categories)


@materials_bp.route('/materials/<int:material_id>')
def material_detail(material_id):
    """原料详情页面"""
    current_user = get_current_user()
    material = MaterialSupply.query.get(material_id)
    return render_template('material_detail.html', current_user=current_user, material=material)


@materials_bp.route('/my-materials')
@require_login
@require_role('supplier')
def my_materials_page():
    """供应商的原料管理页面"""
    current_user = get_current_user()
    user_materials = MaterialSupply.query.filter_by(
        publisher_user_id=current_user.id,
        is_deleted=False
    ).order_by(MaterialSupply.created_at.desc()).all()

    categories = MaterialCategory.query.filter_by(status='active').order_by(MaterialCategory.sort_no).all()

    return render_template('my_materials.html', current_user=current_user,
                           user_materials=user_materials, categories=categories)
