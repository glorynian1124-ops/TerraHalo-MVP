#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
司机端路由 — 任务列表 / 任务详情 / 接单 / 送达确认
"""

from datetime import datetime, timezone
from flask import Blueprint, render_template, request, jsonify, session
from models import db, User, Driver, DispatchTask, DispatchTaskLog, SupplyDemandMatch, MaterialSupply, MaterialOrder
from utils import require_login, require_role, get_current_user

driver_bp = Blueprint('driver', __name__, url_prefix='/driver')


# ============================================================
# 页面路由
# ============================================================

@driver_bp.route('/tasks')
@require_login
@require_role('driver')
def tasks_page():
    """司机任务列表页"""
    user = get_current_user()
    return render_template('driver/tasks.html', current_user=user)


# ============================================================
# 任务 API
# ============================================================

@driver_bp.route('/api/tasks', methods=['GET'])
@require_login
@require_role('driver')
def get_tasks_api():
    """获取司机的任务列表"""
    user = get_current_user()
    driver = Driver.query.filter_by(user_id=user.id).first()
    if not driver:
        return jsonify({"error": "司机信息未完善"}), 400

    status_filter = request.args.get('status')
    query = DispatchTask.query.filter_by(driver_id=driver.id)

    if status_filter:
        query = query.filter(DispatchTask.status == status_filter)
    else:
        # 默认显示活跃任务
        query = query.filter(DispatchTask.status.in_(['pending_accept', 'accepted']))

    tasks = query.order_by(DispatchTask.created_at.desc()).all()

    result = []
    for t in tasks:
        match = SupplyDemandMatch.query.get(t.match_id)
        supply = MaterialSupply.query.get(match.supply_id) if match else None
        result.append({
            **t.to_dict(),
            'supply': supply.to_dict() if supply else None,
        })

    return jsonify(result)


@driver_bp.route('/api/tasks/pool', methods=['GET'])
@require_login
@require_role('driver')
def get_task_pool_api():
    """获取待接单任务池（所有待派单 + 已派给当前司机的待接单）"""
    user = get_current_user()
    driver = Driver.query.filter_by(user_id=user.id).first()
    if not driver:
        return jsonify({"error": "司机信息未完善"}), 400

    # 已派给当前司机待接单的
    my_pending = DispatchTask.query.filter_by(driver_id=driver.id, status='pending_accept').all()

    result = []
    for t in my_pending:
        match = SupplyDemandMatch.query.get(t.match_id)
        supply = MaterialSupply.query.get(match.supply_id) if match else None
        result.append({
            **t.to_dict(),
            'supply': supply.to_dict() if supply else None,
        })

    return jsonify(result)


@driver_bp.route('/api/tasks/<int:task_id>/accept', methods=['POST'])
@require_login
@require_role('driver')
def accept_task_api(task_id):
    """司机接单"""
    user = get_current_user()
    driver = Driver.query.filter_by(user_id=user.id).first()
    if not driver:
        return jsonify({"error": "司机信息未完善"}), 400

    task = DispatchTask.query.get(task_id)
    if not task:
        return jsonify({"error": "任务不存在"}), 404
    if task.driver_id != driver.id:
        return jsonify({"error": "该任务未分配给您"}), 403
    if task.status != 'pending_accept':
        return jsonify({"error": "任务状态不正确"}), 400

    task.status = 'accepted'
    task.actual_pickup_time = datetime.now(timezone.utc)

    log = DispatchTaskLog(
        task_id=task.id,
        status='accepted',
        operator_user_id=user.id,
        operator_role='driver',
        content='司机已接单'
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({"message": "接单成功", "task_id": task.id})


@driver_bp.route('/api/tasks/<int:task_id>/complete', methods=['POST'])
@require_login
@require_role('driver')
def complete_task_api(task_id):
    """司机确认送达"""
    user = get_current_user()
    driver = Driver.query.filter_by(user_id=user.id).first()
    if not driver:
        return jsonify({"error": "司机信息未完善"}), 400

    task = DispatchTask.query.get(task_id)
    if not task:
        return jsonify({"error": "任务不存在"}), 404
    if task.driver_id != driver.id:
        return jsonify({"error": "该任务未分配给您"}), 403
    if task.status != 'accepted':
        return jsonify({"error": "当前状态不可完成"}), 400

    task.status = 'completed'
    task.actual_arrival_time = datetime.now(timezone.utc)

    log = DispatchTaskLog(
        task_id=task.id,
        status='completed',
        operator_user_id=user.id,
        operator_role='driver',
        content='司机已确认送达'
    )
    db.session.add(log)
    db.session.commit()

    # 关联原料订单：推进到 transported
    match = SupplyDemandMatch.query.get(task.match_id)
    if match:
        order = MaterialOrder.query.filter_by(
            supply_id=match.supply_id, status='dispatched'
        ).first()
        if order:
            order.status = 'transported'
            db.session.commit()

    return jsonify({"message": "已确认送达", "task_id": task.id})
