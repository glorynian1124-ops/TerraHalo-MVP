#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
管理后台调度 API — 任务池 / 司机列表 / 派单
"""

from datetime import datetime, timezone, timedelta
from flask import Blueprint, render_template, request, jsonify, session
from models import db, User, Driver, Enterprise, MaterialDemand, MaterialOrder, DispatchTask, DispatchTaskLog, SupplyDemandMatch, MaterialSupply
from models.product import Product, ProductOrder, ProductOrderItem, ProductImage, ProductCategory
from utils import require_login, require_role, get_current_user

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


# ============================================================
# 页面路由
# ============================================================

@admin_bp.route('/')
@admin_bp.route('/dashboard')
@require_login
@require_role('admin')
def dashboard_page():
    """管理后台首页：企业工作台 / 司机调度 进入窗口"""
    return render_template('admin/dashboard.html', current_user=get_current_user())


@admin_bp.route('/dispatch')
@require_login
@require_role('admin')
def dispatch_page():
    """调度中心页面"""
    user = get_current_user()
    return render_template('admin/dispatch.html', current_user=user)


@admin_bp.route('/supply-audit')
@require_login
@require_role('admin')
def supply_audit_page():
    """供给审核页面"""
    return render_template('admin/supply-audit.html', current_user=get_current_user())


@admin_bp.route('/users')
@require_login
@require_role('admin')
def users_page():
    """用户管理页面"""
    return render_template('admin/users.html', current_user=get_current_user())


# ============================================================
# 调度 API
# ============================================================

@admin_bp.route('/api/dispatch/pending-tasks', methods=['GET'])
@require_login
@require_role('admin')
def get_pending_tasks_api():
    """获取待派单任务列表"""
    tasks = DispatchTask.query.filter_by(status='pending_assign')\
                              .order_by(DispatchTask.created_at.asc()).all()

    result = []
    for t in tasks:
        match = SupplyDemandMatch.query.get(t.match_id)
        supply = MaterialSupply.query.get(match.supply_id) if match else None
        demand = match.demand if match else None
        result.append({
            **t.to_dict(),
            'supply': supply.to_dict() if supply else None,
            'demand_category': demand.category_name if demand else None,
        })

    return jsonify(result)


@admin_bp.route('/api/dispatch/drivers', methods=['GET'])
@require_login
@require_role('admin')
def get_drivers_api():
    """获取可用司机列表"""
    drivers = Driver.query.filter_by(audit_status='approved').all()
    result = []
    for d in drivers:
        user = User.query.get(d.user_id)
        # 统计当前任务数
        active_tasks = DispatchTask.query.filter(
            DispatchTask.driver_id == d.id,
            DispatchTask.status.in_(['pending_accept', 'accepted'])
        ).count()
        result.append({
            'id': d.id,
            'user_id': d.user_id,
            'name': user.username if user else '-',
            'vehicle_type': d.vehicle_type,
            'vehicle_no': d.vehicle_no,
            'vehicle_capacity_ton': float(d.vehicle_capacity_ton) if d.vehicle_capacity_ton else 0,
            'active_tasks': active_tasks,
        })

    return jsonify(result)


@admin_bp.route('/api/dispatch/assign', methods=['POST'])
@require_login
@require_role('admin')
def assign_task_api():
    """派单：将任务分配给指定司机"""
    data = request.json
    task_id = data.get('task_id')
    driver_id = data.get('driver_id')
    current_user = get_current_user()

    task = DispatchTask.query.get(task_id)
    if not task:
        return jsonify({"error": "任务不存在"}), 404
    if task.status != 'pending_assign':
        return jsonify({"error": "该任务已分配"}), 400

    driver = Driver.query.get(driver_id)
    if not driver:
        return jsonify({"error": "司机不存在"}), 404

    task.driver_id = driver.id
    task.vehicle_no = driver.vehicle_no
    task.status = 'pending_accept'

    log = DispatchTaskLog(
        task_id=task.id,
        status='pending_accept',
        operator_user_id=current_user.id,
        operator_role='admin',
        content=f'管理员派单给司机 {User.query.get(driver.user_id).username} ({driver.vehicle_no})'
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({"message": "派单成功", "task_id": task.id, "driver_name": User.query.get(driver.user_id).username})


# ============================================================
# 供给审核 API
# ============================================================

@admin_bp.route('/api/audit/supplies', methods=['GET'])
@require_login
@require_role('admin')
def audit_supply_list():
    """获取待审核/全部原料供给列表"""
    status_filter = request.args.get('status', 'pending')
    query = MaterialSupply.query.filter_by(is_deleted=False)
    if status_filter != 'all':
        query = query.filter_by(audit_status=status_filter)
    supplies = query.order_by(MaterialSupply.created_at.desc()).limit(100).all()
    return jsonify([m.to_dict() for m in supplies])


@admin_bp.route('/api/audit/users', methods=['GET'])
@require_login
@require_role('admin')
def user_list():
    """获取用户列表（管理用）"""
    role_filter = request.args.get('role')
    query = User.query.filter_by(is_deleted=False)
    if role_filter:
        query = query.filter_by(role_type=role_filter)
    users = query.order_by(User.created_at.desc()).limit(100).all()
    return jsonify([{
        'id': u.id,
        'username': u.username,
        'role_type': u.role_type,
        'phone': u.phone,
        'email': u.email,
        'status': u.status,
        'is_verified': u.is_verified,
        'credit_score': u.credit_score,
        'created_at': u.created_at.isoformat() if u.created_at else None,
    } for u in users])


@admin_bp.route('/api/audit/users/<int:user_id>/toggle-status', methods=['POST'])
@require_login
@require_role('admin')
def toggle_user_status(user_id):
    """封禁/解封用户"""
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "用户不存在"}), 404
    user.status = 'banned' if user.status == 'normal' else 'normal'
    db.session.commit()
    return jsonify({"message": "状态已更新", "user_id": user.id, "status": user.status})


# ============================================================
# 总控室管理 API
# ============================================================

@admin_bp.route('/api/admin/enterprises', methods=['GET'])
@require_login
@require_role('admin')
def admin_enterprises():
    """总控室：企业列表（认证状态 / 需求数 / 商品数 / 交易额）
    说明：后端约定 enterprise_id 字段存企业用户的 user.id，故按企业角色用户统计"""
    ent_users = User.query.filter_by(role_type='enterprise', is_deleted=False).order_by(User.created_at.desc()).all()
    result = []
    for user in ent_users:
        ent = user.enterprise  # 企业档案（可能为空）
        uid = user.id
        demand_count = MaterialDemand.query.filter_by(enterprise_id=uid, is_deleted=False).count()
        product_count = Product.query.filter_by(enterprise_id=uid, is_deleted=False).count()
        online_products = Product.query.filter_by(enterprise_id=uid, is_deleted=False, status='online').count()
        paid_orders = ProductOrder.query.filter(
            ProductOrder.enterprise_id == uid,
            ProductOrder.is_deleted == False,
            ProductOrder.pay_status == 'paid'
        ).all()
        order_amount = sum(float(o.total_amount or 0) for o in paid_orders)
        result.append({
            'id': ent.id if ent else user.id,
            'user_id': uid,
            'enterprise_name': (ent.enterprise_name if ent else (user.company or user.username)),
            'enterprise_type': ent.enterprise_type if ent else '',
            'license_no': ent.license_no if ent else '',
            'contact_name': ent.contact_name if ent else '',
            'contact_mobile': ent.contact_mobile if ent else user.phone,
            'address': ent.address if ent else user.address,
            'audit_status': ent.audit_status if ent else 'pending',
            'username': user.username,
            'user_status': user.status,
            'is_verified': user.is_verified,
            'demand_count': demand_count,
            'product_count': product_count,
            'online_products': online_products,
            'order_count': len(paid_orders),
            'order_amount': order_amount,
            'created_at': user.created_at.isoformat() if user.created_at else None,
        })
    return jsonify(result)


@admin_bp.route('/api/admin/drivers', methods=['GET'])
@require_login
@require_role('admin')
def admin_drivers():
    """总控室：司机列表（含车辆 / 审核状态 / 任务统计）"""
    drivers = Driver.query.order_by(Driver.created_at.desc()).all()
    result = []
    for d in drivers:
        user = User.query.get(d.user_id)
        active_tasks = DispatchTask.query.filter(
            DispatchTask.driver_id == d.id,
            DispatchTask.status.in_(['pending_accept', 'accepted'])
        ).count()
        done_tasks = DispatchTask.query.filter(
            DispatchTask.driver_id == d.id,
            DispatchTask.status == 'completed'
        ).count()
        result.append({
            'id': d.id,
            'user_id': d.user_id,
            'name': user.username if user else '-',
            'phone': user.phone if user else None,
            'vehicle_type': d.vehicle_type,
            'vehicle_no': d.vehicle_no,
            'vehicle_capacity_ton': float(d.vehicle_capacity_ton) if d.vehicle_capacity_ton else 0,
            'audit_status': d.audit_status,
            'user_status': user.status if user else '-',
            'active_tasks': active_tasks,
            'done_tasks': done_tasks,
            'created_at': d.created_at.isoformat() if d.created_at else None,
        })
    return jsonify(result)


@admin_bp.route('/api/admin/products', methods=['GET'])
@require_login
@require_role('admin')
def admin_products():
    """总控室：商品全量（含待审核），附企业名 / 分类 / 图片"""
    status_filter = request.args.get('status', 'all')
    query = Product.query.filter_by(is_deleted=False)
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    products = query.order_by(Product.created_at.desc()).limit(200).all()
    result = []
    for p in products:
        d = p.to_dict()
        ent = Enterprise.query.get(p.enterprise_id) if p.enterprise_id else None
        cat = ProductCategory.query.get(p.category_id) if p.category_id else None
        d['enterprise_name'] = ent.enterprise_name if ent else (p.supplier_name or '-')
        d['category_name'] = cat.name if cat else ''
        d['images'] = [{'id': img.id, 'url': img.image_url} for img in p.images]
        result.append(d)
    return jsonify(result)


# ============================================================
# 企业总览（企业情况）— 平台全盘视角
# ============================================================

def _period_bounds(now):
    """自然周 / 月 / 年起点（UTC）"""
    week = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
    month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    year = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    return week, month, year


def _enterprise_base(user, ent):
    """企业基础档案字段（与总控室企业列表一致）"""
    uid = user.id
    return {
        'id': ent.id if ent else user.id,
        'user_id': uid,
        'enterprise_name': (ent.enterprise_name if ent else (user.company or user.username)),
        'enterprise_type': ent.enterprise_type if ent else '',
        'license_no': ent.license_no if ent else '',
        'contact_name': ent.contact_name if ent else '',
        'contact_mobile': ent.contact_mobile if ent else user.phone,
        'address': (ent.address if ent else user.address) or '',
        'audit_status': ent.audit_status if ent else 'pending',
        'username': user.username,
        'user_status': user.status,
        'is_verified': user.is_verified,
        'created_at': user.created_at.isoformat() if user.created_at else None,
    }


def _summarize_sales(enterprise_id, bounds):
    """产品销量（件数 + 金额）按周 / 月 / 年"""
    week_start, month_start, year_start = bounds
    out = {}
    for label, start in [('week', week_start), ('month', month_start), ('year', year_start)]:
        orders = ProductOrder.query.filter(
            ProductOrder.enterprise_id == enterprise_id,
            ProductOrder.pay_status == 'paid',
            ProductOrder.created_at >= start,
            ProductOrder.is_deleted == False,
        ).all()
        qty = 0
        amount = 0.0
        for o in orders:
            amount += float(o.total_amount or 0)
            for it in o.items:
                qty += it.quantity or 0
        out[label] = {'qty': int(qty), 'amount': round(amount, 2)}
    return out


def _summarize_imports(enterprise_id, bounds):
    """原料进口量（吨）按周 / 月 / 年"""
    week_start, month_start, year_start = bounds
    out = {}
    for label, start in [('week', week_start), ('month', month_start), ('year', year_start)]:
        rows = MaterialOrder.query.filter(
            MaterialOrder.enterprise_id == enterprise_id,
            MaterialOrder.status == 'completed',
            MaterialOrder.created_at >= start,
            MaterialOrder.is_deleted == False,
        ).all()
        weight = sum(float(r.actual_weight or r.estimated_weight or 0) for r in rows)
        out[label] = round(weight, 2)
    return out


def _product_sales(enterprise_id):
    """该企业上架单品 + 累计销量（paid 订单聚合）"""
    from sqlalchemy import func
    agg = db.session.query(
        ProductOrderItem.product_id,
        func.coalesce(func.sum(ProductOrderItem.quantity), 0),
        func.coalesce(func.sum(ProductOrderItem.amount), 0)
    ).join(ProductOrder, ProductOrder.id == ProductOrderItem.order_id).filter(
        ProductOrder.enterprise_id == enterprise_id,
        ProductOrder.pay_status == 'paid',
        ProductOrder.is_deleted == False,
    ).group_by(ProductOrderItem.product_id).all()
    sold = {pid: {'qty': int(qty), 'amount': float(amt)} for pid, qty, amt in agg}
    products = Product.query.filter_by(enterprise_id=enterprise_id, is_deleted=False).all()
    return [{
        'id': p.id,
        'product_name': p.product_name,
        'specification': p.specification,
        'price': float(p.price) if p.price else 0,
        'stock_qty': p.stock_qty,
        'status': p.status,
        'sold_qty': sold.get(p.id, {}).get('qty', 0),
        'sold_amount': sold.get(p.id, {}).get('amount', 0),
    } for p in products]


@admin_bp.route('/api/admin/enterprises/overview', methods=['GET'])
@require_login
@require_role('admin')
def enterprises_overview():
    """企业总览：全盘企业档案 + 周/月/年销量与原料进口量 + 上架单品及销量"""
    now = datetime.now(timezone.utc)
    bounds = _period_bounds(now)
    ent_users = User.query.filter_by(role_type='enterprise', is_deleted=False).order_by(User.created_at.desc()).all()
    result = []
    for user in ent_users:
        ent = user.enterprise
        base = _enterprise_base(user, ent)
        uid = user.id
        demand_count = MaterialDemand.query.filter_by(enterprise_id=uid, is_deleted=False).count()
        product_count = Product.query.filter_by(enterprise_id=uid, is_deleted=False).count()
        online_products = Product.query.filter_by(enterprise_id=uid, is_deleted=False, status='online').count()
        base['demand_count'] = demand_count
        base['product_count'] = product_count
        base['online_products'] = online_products
        base['sales'] = _summarize_sales(uid, bounds)
        base['imports'] = _summarize_imports(uid, bounds)
        base['products'] = _product_sales(uid)
        result.append(base)
    return jsonify(result)
