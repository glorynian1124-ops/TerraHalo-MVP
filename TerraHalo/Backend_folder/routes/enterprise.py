#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
企业端路由 — 采购需求 / 匹配确认 / 收运任务 / 商品管理
"""

import uuid
from datetime import datetime, timezone
from flask import Blueprint, render_template, request, jsonify, session
from models import (
    db, User, Enterprise,
    MaterialDemand, MaterialSupply, SupplyDemandMatch,
    DispatchTask, DispatchTaskLog,
    Product, ProductCategory
)
from utils import require_login, require_role, get_current_user
from utils.matcher import auto_match, get_matches_for_demand

enterprise_bp = Blueprint('enterprise', __name__, url_prefix='/enterprise')

CATEGORY_NAMES = ['畜禽粪便', '农作物秸秆', '厨余垃圾', '工业副产品', '绿肥植物']


# ============================================================
# 页面路由
# ============================================================

@enterprise_bp.route('/dashboard')
@require_login
@require_role('enterprise')
def dashboard():
    """企业工作台"""
    user = get_current_user()
    # 统计
    demand_count = MaterialDemand.query.filter_by(enterprise_id=user.id, is_deleted=False).count()
    active_demand_count = MaterialDemand.query.filter_by(
        enterprise_id=user.id, is_deleted=False
    ).filter(MaterialDemand.status.in_(['active', 'matching'])).count()
    task_count = DispatchTask.query.join(SupplyDemandMatch).join(
        MaterialDemand, SupplyDemandMatch.demand_id == MaterialDemand.id
    ).filter(MaterialDemand.enterprise_id == user.id).count()
    product_count = Product.query.filter_by(enterprise_id=user.id, is_deleted=False).count()

    stats = {
        'demand_count': demand_count,
        'active_demand_count': active_demand_count,
        'task_count': task_count,
        'product_count': product_count,
    }
    return render_template('enterprise/dashboard.html', current_user=user, stats=stats)


@enterprise_bp.route('/demands')
@require_login
@require_role('enterprise')
def demands_page():
    """采购需求管理页"""
    user = get_current_user()
    return render_template('enterprise/demands.html', current_user=user,
                           category_names=CATEGORY_NAMES)


@enterprise_bp.route('/matches')
@require_login
@require_role('enterprise')
def matches_page():
    """匹配结果页"""
    user = get_current_user()
    return render_template('enterprise/matches.html', current_user=user)


@enterprise_bp.route('/tasks')
@require_login
@require_role('enterprise')
def tasks_page():
    """收运任务页"""
    user = get_current_user()
    return render_template('enterprise/tasks.html', current_user=user)


@enterprise_bp.route('/products')
@require_login
@require_role('enterprise')
def products_page():
    """商品管理页"""
    user = get_current_user()
    return render_template('enterprise/products.html', current_user=user)


# ============================================================
# 采购需求 API
# ============================================================

@enterprise_bp.route('/api/demands', methods=['GET'])
@require_login
@require_role('enterprise')
def get_demands_api():
    """获取企业采购需求列表"""
    user = get_current_user()
    status_filter = request.args.get('status')

    query = MaterialDemand.query.filter_by(enterprise_id=user.id, is_deleted=False)
    if status_filter:
        query = query.filter(MaterialDemand.status == status_filter)

    demands = query.order_by(MaterialDemand.created_at.desc()).all()
    return jsonify([{
        'id': d.id,
        'demand_no': d.demand_no,
        'category_name': d.category_name,
        'target_weight': float(d.target_weight) if d.target_weight else None,
        'min_weight': float(d.min_weight) if d.min_weight else None,
        'expected_price_min': float(d.expected_price_min) if d.expected_price_min else None,
        'expected_price_max': float(d.expected_price_max) if d.expected_price_max else None,
        'purchase_radius_km': d.purchase_radius_km,
        'quality_requirement': d.quality_requirement,
        'status': d.status,
        'remark': d.remark,
        'created_at': d.created_at.isoformat() if d.created_at else None,
    } for d in demands])


@enterprise_bp.route('/api/demands', methods=['POST'])
@require_login
@require_role('enterprise')
def create_demand_api():
    """创建采购需求（创建后自动触发匹配）"""
    user = get_current_user()
    data = request.json

    required = ['category_name', 'target_weight']
    for field in required:
        if not data.get(field):
            return jsonify({"error": f"缺少字段: {field}"}), 400

    demand = MaterialDemand(
        demand_no=f'MD{datetime.now().strftime("%Y%m%d%H%M%S")}{uuid.uuid4().hex[:6].upper()}',
        enterprise_id=user.id,
        category_name=data['category_name'],
        target_weight=float(data['target_weight']),
        min_weight=float(data.get('min_weight', 0)),
        expected_price_min=float(data['expected_price_min']) if data.get('expected_price_min') else None,
        expected_price_max=float(data['expected_price_max']) if data.get('expected_price_max') else None,
        purchase_radius_km=int(data.get('purchase_radius_km', 50)),
        quality_requirement=data.get('quality_requirement', ''),
        status='active',
        remark=data.get('remark', ''),
    )
    db.session.add(demand)
    db.session.commit()

    # 自动匹配
    matches = auto_match(demand.id)

    return jsonify({
        "message": "需求发布成功",
        "demand_id": demand.id,
        "demand_no": demand.demand_no,
        "matches_count": len(matches)
    })


@enterprise_bp.route('/api/demands/<int:demand_id>', methods=['PUT'])
@require_login
@require_role('enterprise')
def update_demand_api(demand_id):
    """编辑采购需求"""
    user = get_current_user()
    demand = MaterialDemand.query.get(demand_id)
    if not demand or demand.enterprise_id != user.id:
        return jsonify({"error": "需求不存在"}), 404
    if demand.status not in ('active', 'matching', 'pending_audit'):
        return jsonify({"error": "当前状态不可编辑"}), 400

    data = request.json
    if data.get('category_name'):
        demand.category_name = data['category_name']
    if data.get('target_weight'):
        demand.target_weight = float(data['target_weight'])
    if data.get('min_weight') is not None:
        demand.min_weight = float(data['min_weight'])
    if data.get('expected_price_min') is not None:
        demand.expected_price_min = float(data['expected_price_min'])
    if data.get('expected_price_max') is not None:
        demand.expected_price_max = float(data['expected_price_max'])
    if data.get('purchase_radius_km') is not None:
        demand.purchase_radius_km = int(data['purchase_radius_km'])
    if data.get('quality_requirement') is not None:
        demand.quality_requirement = data['quality_requirement']
    if data.get('remark') is not None:
        demand.remark = data['remark']

    db.session.commit()

    # 重新匹配
    matches = auto_match(demand.id)

    return jsonify({
        "message": "需求已更新",
        "matches_count": len(matches)
    })


@enterprise_bp.route('/api/demands/<int:demand_id>/close', methods=['POST'])
@require_login
@require_role('enterprise')
def close_demand_api(demand_id):
    """关闭采购需求"""
    user = get_current_user()
    demand = MaterialDemand.query.get(demand_id)
    if not demand or demand.enterprise_id != user.id:
        return jsonify({"error": "需求不存在"}), 404

    demand.status = 'closed'
    db.session.commit()
    return jsonify({"message": "需求已关闭"})


# ============================================================
# 匹配 API
# ============================================================

@enterprise_bp.route('/api/demands/<int:demand_id>/matches', methods=['GET'])
@require_login
@require_role('enterprise')
def get_matches_api(demand_id):
    """查看某需求的匹配结果"""
    user = get_current_user()
    demand = MaterialDemand.query.get(demand_id)
    if not demand or demand.enterprise_id != user.id:
        return jsonify({"error": "需求不存在"}), 404

    return jsonify({
        'demand_id': demand.id,
        'demand_no': demand.demand_no,
        'category_name': demand.category_name,
        'matches': get_matches_for_demand(demand_id)
    })


@enterprise_bp.route('/api/matches/<int:match_id>/confirm', methods=['POST'])
@require_login
@require_role('enterprise')
def confirm_match_api(match_id):
    """企业确认匹配 → 生成收运任务"""
    user = get_current_user()
    match = SupplyDemandMatch.query.get(match_id)
    if not match:
        return jsonify({"error": "匹配记录不存在"}), 404

    demand = MaterialDemand.query.get(match.demand_id)
    if not demand or demand.enterprise_id != user.id:
        return jsonify({"error": "无权操作"}), 403
    if match.status != 'pending':
        return jsonify({"error": "该匹配已处理"}), 400

    supply = MaterialSupply.query.get(match.supply_id)
    if not supply or not supply.is_available:
        return jsonify({"error": "供给已失效"}), 400

    # 确认匹配
    match.status = 'confirmed'
    demand.status = 'matched'

    # 生成调度任务
    task = DispatchTask(
        task_no=f'DT{datetime.now().strftime("%Y%m%d%H%M%S")}{uuid.uuid4().hex[:6].upper()}',
        match_id=match.id,
        driver_id=0,  # 待派单
        pickup_address=supply.location or supply.detail_address or '',
        delivery_address=user.address or '',
        transport_fee=0,
        status='pending_assign',
    )
    db.session.add(task)

    # 记录日志
    log = DispatchTaskLog(
        task_id=0,  # flush 后更新
        status='pending_assign',
        operator_user_id=user.id,
        operator_role='enterprise',
        content=f'企业确认匹配，生成收运任务'
    )
    db.session.add(log)
    db.session.flush()
    log.task_id = task.id

    db.session.commit()

    return jsonify({
        "message": "匹配已确认，收运任务已生成",
        "match_id": match.id,
        "task_id": task.id,
        "task_no": task.task_no
    })


# ============================================================
# 收运任务 API
# ============================================================

@enterprise_bp.route('/api/tasks', methods=['GET'])
@require_login
@require_role('enterprise')
def get_tasks_api():
    """获取企业相关的收运任务列表"""
    user = get_current_user()
    # 通过 需求 → 匹配 → 任务 链查询
    tasks = DispatchTask.query.join(SupplyDemandMatch).join(
        MaterialDemand, SupplyDemandMatch.demand_id == MaterialDemand.id
    ).filter(MaterialDemand.enterprise_id == user.id)\
     .order_by(DispatchTask.created_at.desc()).all()

    return jsonify([t.to_dict() for t in tasks])


@enterprise_bp.route('/api/tasks/<int:task_id>', methods=['GET'])
@require_login
@require_role('enterprise')
def get_task_detail_api(task_id):
    """获取收运任务详情"""
    task = DispatchTask.query.get(task_id)
    if not task:
        return jsonify({"error": "任务不存在"}), 404

    match = SupplyDemandMatch.query.get(task.match_id)
    supply = MaterialSupply.query.get(match.supply_id) if match else None
    logs = DispatchTaskLog.query.filter_by(task_id=task_id)\
                                .order_by(DispatchTaskLog.created_at.asc()).all()

    return jsonify({
        'task': task.to_dict(),
        'supply': supply.to_dict() if supply else None,
        'logs': [{
            'status': l.status,
            'operator_role': l.operator_role,
            'content': l.content,
            'created_at': l.created_at.isoformat() if l.created_at else None,
        } for l in logs]
    })


# ============================================================
# 商品管理 API
# ============================================================

@enterprise_bp.route('/api/products', methods=['GET'])
@require_login
@require_role('enterprise')
def get_products_api():
    """获取企业商品列表"""
    user = get_current_user()
    products = Product.query.filter_by(enterprise_id=user.id, is_deleted=False)\
                            .order_by(Product.created_at.desc()).all()
    return jsonify([p.to_dict() for p in products])


@enterprise_bp.route('/api/products', methods=['POST'])
@require_login
@require_role('enterprise')
def create_product_api():
    """上架商品"""
    user = get_current_user()
    data = request.json

    required = ['product_name', 'price', 'stock_qty']
    for field in required:
        if not data.get(field):
            return jsonify({"error": f"缺少字段: {field}"}), 400

    product = Product(
        enterprise_id=user.id,
        supplier_name=user.company or user.username,
        product_name=data['product_name'],
        specification=data.get('specification', ''),
        unit=data.get('unit', 'bag'),
        price=float(data['price']),
        stock_qty=int(data['stock_qty']),
        min_order_qty=int(data.get('min_order_qty', 1)),
        delivery_scope=data.get('delivery_scope', ''),
        suitable_crops=data.get('suitable_crops', ''),
        detail_content=data.get('detail_content', ''),
        status='on_shelf',
    )
    db.session.add(product)
    db.session.commit()

    return jsonify({"message": "商品上架成功", "product_id": product.id, "product": product.to_dict()})


@enterprise_bp.route('/api/products/<int:product_id>', methods=['PUT'])
@require_login
@require_role('enterprise')
def update_product_api(product_id):
    """编辑商品"""
    user = get_current_user()
    product = Product.query.get(product_id)
    if not product or product.enterprise_id != user.id:
        return jsonify({"error": "商品不存在"}), 404

    data = request.json
    for field in ['product_name', 'specification', 'unit', 'delivery_scope',
                   'suitable_crops', 'detail_content']:
        if field in data:
            setattr(product, field, data[field])
    if 'price' in data:
        product.price = float(data['price'])
    if 'stock_qty' in data:
        product.stock_qty = int(data['stock_qty'])
    if 'min_order_qty' in data:
        product.min_order_qty = int(data['min_order_qty'])

    db.session.commit()
    return jsonify({"message": "商品已更新"})


@enterprise_bp.route('/api/products/<int:product_id>/toggle', methods=['POST'])
@require_login
@require_role('enterprise')
def toggle_product_api(product_id):
    """商品上下架"""
    user = get_current_user()
    product = Product.query.get(product_id)
    if not product or product.enterprise_id != user.id:
        return jsonify({"error": "商品不存在"}), 404

    product.status = 'off_shelf' if product.status == 'on_shelf' else 'on_shelf'
    db.session.commit()
    return jsonify({"message": f"商品已{'下架' if product.status == 'off_shelf' else '上架'}"})
