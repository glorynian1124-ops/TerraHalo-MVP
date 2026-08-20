#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import uuid
from datetime import datetime, timezone
from flask import Blueprint, request, jsonify, session
from models import db, User, MaterialSupply, MaterialCategory, MaterialOrder, MaterialSupplyImage, MaterialDemand
from models.product import Product, ProductCategory, ProductImage, ProductOrder, ProductOrderItem
from utils import require_login, require_role, calculate_credit_score

api_bp = Blueprint('api', __name__)


# ============================================================
# 原料 API
# ============================================================

@api_bp.route('/api/materials', methods=['GET'])
def get_materials_api():
    """获取原料列表（支持多种筛选）"""
    # 如果传了 id 参数，返回单条详情
    material_id = request.args.get('id')
    if material_id:
        try:
            material = MaterialSupply.query.get(int(material_id))
            if not material:
                return jsonify({"error": "原料不存在"}), 404
            return jsonify(material.to_dict())
        except ValueError:
            return jsonify({"error": "无效的 ID"}), 400

    query = MaterialSupply.query.filter_by(is_available=True, is_deleted=False)

    # 筛选条件
    m_type = request.args.get('type')
    location = request.args.get('location')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    supplier_id = request.args.get('supplier_id')
    search = request.args.get('search')
    sort_by = request.args.get('sort_by', 'created_at')

    # 筛选
    category_id = request.args.get('category_id')
    if category_id:
        try:
            query = query.filter(MaterialSupply.category_id == int(category_id))
        except ValueError:
            pass
    if m_type:
        query = query.filter(MaterialSupply.type == m_type)
    if location:
        query = query.filter(MaterialSupply.location.contains(location))
    if min_price:
        try:
            query = query.filter(MaterialSupply.price >= float(min_price))
        except ValueError:
            pass
    if max_price:
        try:
            query = query.filter(MaterialSupply.price <= float(max_price))
        except ValueError:
            pass
    if supplier_id:
        try:
            query = query.filter(MaterialSupply.publisher_user_id == int(supplier_id))
        except ValueError:
            pass
    if search:
        search_lower = search.lower()
        query = query.filter(
            db.or_(
                MaterialSupply.type.ilike(f'%{search_lower}%'),
                MaterialSupply.description.ilike(f'%{search_lower}%'),
                MaterialSupply.supplier_name.ilike(f'%{search_lower}%')
            )
        )

    # 排序
    if sort_by == 'price':
        query = query.order_by(MaterialSupply.price.asc())
    elif sort_by == 'price_desc':
        query = query.order_by(MaterialSupply.price.desc())
    elif sort_by == 'rating':
        query = query.order_by(MaterialSupply.rating.desc())
    else:
        query = query.order_by(MaterialSupply.created_at.desc())

    materials = query.all()
    return jsonify([m.to_dict() for m in materials])


@api_bp.route('/api/materials', methods=['POST'])
@require_login
@require_role('supplier')
def post_material_api():
    """发布原料信息（完整 MVP 表单）"""
    data = request.json
    current_user = User.query.get(session.get('user_id'))

    # MVP 必填字段
    required_fields = ['category_id', 'estimated_weight', 'price', 'province', 'city', 'detail_address']
    for field in required_fields:
        if not data.get(field):
            return jsonify({"error": f"缺少字段: {field}"}), 400

    # 查找品类
    category = MaterialCategory.query.get(int(data['category_id']))
    category_name = category.name if category else data.get('type', '')

    material = MaterialSupply(
        supply_no=f'MS{datetime.now().strftime("%Y%m%d%H%M%S")}{uuid.uuid4().hex[:6].upper()}',
        publisher_user_id=current_user.id,
        publisher_type='supplier',
        supplier_name=current_user.username,
        category_id=int(data['category_id']),
        # 兼容字段
        type=category_name,
        quantity=float(data.get('estimated_weight', 0)),
        location=f"{data.get('province','')}{data.get('city','')}{data.get('district','')} {data.get('detail_address','')}",
        price=float(data['price']),
        description=data.get('remark', ''),
        moisture=data.get('moisture_range', ''),
        organic_matter=data.get('organic_matter', ''),
        is_available=True,
        rating=0.0,
        review_count=0,
        # MVP 标准字段
        estimated_weight=float(data['estimated_weight']),
        weight_unit=data.get('weight_unit', 'kg'),
        estimated_volume=float(data['estimated_volume']) if data.get('estimated_volume') else None,
        moisture_range=data.get('moisture_range', ''),
        impurity_desc=data.get('impurity_desc', ''),
        packaging_type=data.get('packaging_type', '散装'),
        loadable_flag=data.get('loadable_flag', 'true') in ('true', True, '1', 1),
        available_start_time=datetime.fromisoformat(data['available_start_time']) if data.get('available_start_time') else None,
        available_end_time=datetime.fromisoformat(data['available_end_time']) if data.get('available_end_time') else None,
        province=data.get('province', ''),
        city=data.get('city', ''),
        district=data.get('district', ''),
        detail_address=data.get('detail_address', ''),
        lat=float(data['lat']) if data.get('lat') else None,
        lng=float(data['lng']) if data.get('lng') else None,
        remark=data.get('remark', ''),
        status='pending_audit',
        audit_status='pending',
    )
    db.session.add(material)
    db.session.flush()

    # 关联图片
    image_urls = data.get('image_urls', [])
    for i, url in enumerate(image_urls):
        img = MaterialSupplyImage(supply_id=material.id, image_url=url, sort_no=i)
        db.session.add(img)

    db.session.commit()

    return jsonify({
        "message": "原料发布成功，待审核",
        "material_id": material.id,
        "material": material.to_dict()
    })


@api_bp.route('/api/materials/<int:material_id>/audit', methods=['POST'])
@require_role('admin')
def audit_material_api(material_id):
    """管理员审核原料供给"""
    data = request.json
    action = data.get('action')  # 'approve' or 'reject'
    material = MaterialSupply.query.get(material_id)

    if not material:
        return jsonify({"error": "原料不存在"}), 404
    if material.audit_status != 'pending':
        return jsonify({"error": "该原料已审核"}), 400

    current_user = User.query.get(session.get('user_id'))

    if action == 'approve':
        material.audit_status = 'approved'
        material.status = 'approved'
    elif action == 'reject':
        material.audit_status = 'rejected'
        material.status = 'cancelled'
        material.is_available = False
    else:
        return jsonify({"error": "无效操作"}), 400

    material.audit_user_id = current_user.id
    material.audit_time = datetime.now(timezone.utc)
    db.session.commit()

    return jsonify({"message": f"原料已{'通过' if action=='approve' else '驳回'}"})


@api_bp.route('/api/upload', methods=['POST'])
@require_login
def upload_image():
    """上传图片（返回 URL）"""
    import os
    from config import get_config
    cfg = get_config()

    if 'file' not in request.files:
        return jsonify({"error": "未选择文件"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "文件名为空"}), 400

    # 生成唯一文件名
    ext = file.filename.rsplit('.', 1)[-1].lower() if '.' in file.filename else 'jpg'
    if ext not in ('jpg', 'jpeg', 'png', 'gif', 'webp'):
        return jsonify({"error": "不支持的图片格式"}), 400

    filename = f"{uuid.uuid4().hex}.{ext}"
    upload_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'uploads')
    os.makedirs(upload_dir, exist_ok=True)
    filepath = os.path.join(upload_dir, filename)
    file.save(filepath)

    url = f"/static/uploads/{filename}"
    return jsonify({"url": url, "message": "上传成功"})


@api_bp.route('/api/materials/toggle', methods=['POST'])
@require_login
@require_role('supplier')
def toggle_material_status():
    """切换原料上下架状态"""
    data = request.json
    current_user = User.query.get(session.get('user_id'))
    material = MaterialSupply.query.get(data.get('material_id'))

    if not material:
        return jsonify({"error": "原料不存在"}), 404
    if material.publisher_user_id != current_user.id:
        return jsonify({"error": "无权操作该原料"}), 403

    material.is_available = not material.is_available
    db.session.commit()

    return jsonify({
        "message": f"原料已{'上架' if material.is_available else '下架'}",
        "material_id": material.id,
        "is_available": material.is_available
    })


# ============================================================
# 购物车 API（session 临时存储）
# ============================================================

def _get_cart():
    """获取当前 session 购物车"""
    if 'cart' not in session:
        session['cart'] = []
    return session['cart']


@api_bp.route('/api/cart', methods=['GET'])
@require_login
def get_cart_api():
    """获取购物车详情（含原料信息）"""
    cart = _get_cart()
    items = []
    total_price = 0.0
    for item in cart:
        material = MaterialSupply.query.get(item['material_id'])
        if material and material.is_available:
            price = float(material.price or 0)
            qty = item['quantity']
            item_total = price * qty
            items.append({
                'material_id': material.id,
                'type': material.type or '',
                'quantity': qty,
                'price': price,
                'location': material.location or '',
                'supplier_name': material.supplier_name or '',
            })
            total_price += item_total
    return jsonify({'items': items, 'total': total_price})


@api_bp.route('/api/cart/add', methods=['POST'])
@require_login
def add_to_cart():
    """添加到购物车"""
    data = request.json
    material_id = data.get('material_id')
    quantity = int(data.get('quantity', 1))

    material = MaterialSupply.query.get(material_id)
    if not material:
        return jsonify({"error": "原料不存在"}), 404
    if not material.is_available:
        return jsonify({"error": "该原料已下架"}), 400

    cart = _get_cart()
    for item in cart:
        if item['material_id'] == material_id:
            item['quantity'] += quantity
            session.modified = True
            return jsonify({"message": "购物车已更新"})

    cart.append({
        "material_id": material_id,
        "quantity": quantity
    })
    session.modified = True
    return jsonify({"message": "已加入购物车"})


@api_bp.route('/api/cart/update', methods=['POST'])
@require_login
def update_cart():
    """更新购物车数量"""
    data = request.json
    material_id = data.get('material_id')
    change = int(data.get('change', 0))

    cart = _get_cart()
    for item in cart:
        if item['material_id'] == material_id:
            item['quantity'] += change
            if item['quantity'] <= 0:
                cart.remove(item)
            session.modified = True
            return jsonify({"message": "购物车已更新"})

    return jsonify({"error": "商品不在购物车中"}), 404


@api_bp.route('/api/cart/remove', methods=['POST'])
@require_login
def remove_from_cart():
    """从购物车移除商品"""
    data = request.json
    material_id = data.get('material_id')

    cart = _get_cart()
    for i, item in enumerate(cart):
        if item['material_id'] == material_id:
            cart.pop(i)
            session.modified = True
            return jsonify({"message": "商品已移除"})

    return jsonify({"error": "商品不在购物车中"}), 404


# ============================================================
# 订单 API
# ============================================================

@api_bp.route('/api/orders', methods=['GET'])
@require_login
def get_orders_api():
    """获取当前用户的订单列表"""
    current_user = User.query.get(session.get('user_id'))
    query = MaterialOrder.query

    # 按角色过滤
    if current_user.role_type in ('buyer', 'enterprise'):
        query = query.filter(MaterialOrder.enterprise_id == current_user.id)
    elif current_user.role_type == 'supplier':
        query = query.filter(MaterialOrder.seller_user_id == current_user.id)
    else:
        query = query.filter(
            db.or_(
                MaterialOrder.enterprise_id == current_user.id,
                MaterialOrder.seller_user_id == current_user.id
            )
        )

    # 状态筛选
    status = request.args.get('status')
    if status:
        query = query.filter(MaterialOrder.status == status)

    orders = query.order_by(MaterialOrder.created_at.desc()).all()
    return jsonify([o.to_dict() for o in orders])


@api_bp.route('/api/order/<int:order_id>', methods=['GET'])
@require_login
def get_order_detail(order_id):
    """获取订单详情"""
    current_user = User.query.get(session.get('user_id'))
    order = MaterialOrder.query.get(order_id)

    if not order:
        return jsonify({"error": "订单不存在"}), 404
    if order.enterprise_id != current_user.id and order.seller_user_id != current_user.id:
        return jsonify({"error": "无权查看该订单"}), 403

    return jsonify(order.to_dict())


@api_bp.route('/api/order/create', methods=['POST'])
@require_login
def create_order_api():
    """创建订单"""
    current_user = User.query.get(session.get('user_id'))
    if current_user.role_type != 'buyer':
        return jsonify({"error": "只有买家可以下单"}), 403

    data = request.json
    items = data.get('items', [])
    if not items:
        return jsonify({"error": "请选择商品"}), 400

    total_amount = 0.0
    order_items = []

    for item in items:
        material = MaterialSupply.query.get(item['material_id'])
        if not material:
            return jsonify({"error": f"原料不存在: {item['material_id']}"}), 404
        if not material.is_available:
            return jsonify({"error": f"原料已下架: {material.type}"}), 400

        qty = int(item['quantity'])
        if material.quantity and float(material.quantity) < qty:
            return jsonify({"error": f"库存不足: {material.type}"}), 400

        item_total = float(material.price or 0) * qty
        total_amount += item_total

        order_items.append({
            "material_id": material.id,
            "type": material.type,
            "quantity": qty,
            "unit_price": float(material.price or 0),
            "total_price": item_total,
            "supplier_id": material.publisher_user_id,
            "supplier_name": material.supplier_name
        })

    # 尝试关联企业需求：查找同一企业、同一品类的进行中需求
    matched_demand = MaterialDemand.query.filter_by(
        enterprise_id=current_user.id,
        status='active'
    ).filter(
        MaterialDemand.category_id == items[0].get('category_id', 0)
    ).first() if hasattr(MaterialSupply, 'category_id') else None

    order = MaterialOrder(
        order_no=f'MO{datetime.now().strftime("%Y%m%d%H%M%S")}{uuid.uuid4().hex[:6].upper()}',
        supply_id=items[0]['material_id'],
        demand_id=matched_demand.id if matched_demand else 0,
        enterprise_id=current_user.id,
        seller_user_id=order_items[0]['supplier_id'],
        category_id=order_items[0].get('category_id', 0),
        estimated_weight=sum(it['quantity'] for it in order_items),
        goods_amount=total_amount,
        status='pending_confirm',
    )
    db.session.add(order)

    # 减少库存
    for item in items:
        material = MaterialSupply.query.get(item['material_id'])
        if material.quantity:
            material.quantity = float(material.quantity) - int(item['quantity'])
            if float(material.quantity) <= 0:
                material.is_available = False

    db.session.commit()

    return jsonify({
        "message": "订单创建成功",
        "order_id": order.id,
        "order": order.to_dict()
    })


@api_bp.route('/api/order/create_from_cart', methods=['POST'])
@require_login
def create_order_from_cart():
    """从购物车创建订单"""
    current_user = User.query.get(session.get('user_id'))
    if current_user.role_type != 'buyer':
        return jsonify({"error": "只有买家可以下单"}), 403

    cart = _get_cart()
    if not cart:
        return jsonify({"error": "购物车为空"}), 400

    items = [{"material_id": item['material_id'], "quantity": item['quantity']} for item in cart]

    data = {
        "items": items,
        "shipping_address": request.json.get('shipping_address', current_user.address or '')
    }

    # 内联创建订单逻辑
    total_amount = 0.0
    for item in items:
        material = MaterialSupply.query.get(item['material_id'])
        if material and material.is_available:
            total_amount += float(material.price or 0) * int(item['quantity'])

    first_material = MaterialSupply.query.get(items[0]['material_id']) if items else None
    matched_demand = MaterialDemand.query.filter_by(
        enterprise_id=current_user.id, status='active'
    ).first() if first_material else None

    order = MaterialOrder(
        order_no=f'MO{datetime.now().strftime("%Y%m%d%H%M%S")}{uuid.uuid4().hex[:6].upper()}',
        supply_id=items[0]['material_id'],
        demand_id=matched_demand.id if matched_demand else 0,
        enterprise_id=current_user.id,
        seller_user_id=first_material.publisher_user_id if first_material else 0,
        category_id=first_material.category_id if first_material else 0,
        estimated_weight=sum(it['quantity'] for it in items),
        goods_amount=total_amount,
        status='pending_confirm',
    )
    db.session.add(order)

    for item in items:
        material = MaterialSupply.query.get(item['material_id'])
        if material and material.quantity:
            material.quantity = float(material.quantity) - int(item['quantity'])
            if float(material.quantity) <= 0:
                material.is_available = False

    db.session.commit()

    # 清空购物车
    session['cart'] = []
    session.modified = True

    return jsonify({
        "message": "订单创建成功",
        "order_id": order.id,
        "order": order.to_dict()
    })


@api_bp.route('/api/order/pay', methods=['POST'])
@require_login
def pay_order():
    """订单支付"""
    data = request.json
    current_user = User.query.get(session.get('user_id'))
    order = MaterialOrder.query.get(data.get('order_id'))

    if not order:
        return jsonify({"error": "订单不存在"}), 404
    if order.enterprise_id != current_user.id:
        return jsonify({"error": "无权操作该订单"}), 403
    if order.status != 'pending_confirm' and order.status != 'pending':
        return jsonify({"error": "订单状态不正确"}), 400

    order_amount = float(order.goods_amount or 0)
    if float(current_user.balance or 0) < order_amount:
        return jsonify({"error": "余额不足"}), 400

    current_user.balance = float(current_user.balance) - order_amount
    order.status = 'paid'
    db.session.commit()

    return jsonify({"message": "支付成功", "order_id": order.id})


# 原料订单状态流转表
ORDER_STATUS_FLOW = {
    'pending_confirm': ['paid', 'cancelled'],
    'paid': ['dispatched', 'cancelled'],
    'dispatched': ['transported'],
    'transported': ['signed'],
    'signed': ['settled'],
    'completed': [],
    'cancelled': [],
}

@api_bp.route('/api/order/<int:order_id>/status', methods=['POST'])
@require_login
def update_order_status(order_id):
    """更新订单状态（带状态机校验）"""
    current_user = User.query.get(session.get('user_id'))
    order = MaterialOrder.query.get(order_id)

    if not order:
        return jsonify({"error": "订单不存在"}), 404
    if order.enterprise_id != current_user.id and order.seller_user_id != current_user.id \
       and current_user.role_type not in ('admin', 'driver'):
        return jsonify({"error": "无权操作"}), 403

    new_status = request.json.get('status')
    if not new_status:
        return jsonify({"error": "缺少 status 参数"}), 400

    allowed = ORDER_STATUS_FLOW.get(order.status, [])
    if new_status not in allowed:
        return jsonify({"error": f"不允许从 {order.status} 转为 {new_status}，允许：{allowed}"}), 400

    order.status = new_status
    if new_status in ('settled', 'cancelled'):
        order.completed_at = datetime.now(timezone.utc)
    # 订单结算时自动生成 SettlementBill
    if new_status == 'settled':
        existing = SettlementBill.query.filter_by(biz_type='material', biz_order_id=order_id).first()
        if not existing:
            bill = SettlementBill(
                bill_no=f'ST{datetime.now().strftime("%Y%m%d%H%M%S")}{uuid.uuid4().hex[:6].upper()}',
                biz_type='material', biz_order_id=order_id,
                payer_id=order.enterprise_id, payee_id=order.seller_user_id,
                amount=float(order.goods_amount or 0),
                fee_amount=round(float(order.goods_amount or 0) * 0.02, 2),
                settle_status='pending',
            )
            db.session.add(bill)
    db.session.commit()

    # 自动结算：订单变为 settled 时创建结算单
    if new_status == 'settled':
        existing = SettlementBill.query.filter_by(biz_type='material', biz_order_id=order.id).first()
        if not existing:
            bill = SettlementBill(
                bill_no=f'ST{datetime.now().strftime("%Y%m%d%H%M%S")}{uuid.uuid4().hex[:6].upper()}',
                biz_type='material',
                biz_order_id=order.id,
                payer_id=order.enterprise_id,
                payee_id=order.seller_user_id,
                amount=float(order.goods_amount or 0),
                fee_amount=round(float(order.goods_amount or 0) * 0.02, 2),
                settle_status='pending',
            )
            db.session.add(bill)
            db.session.commit()

    return jsonify({"message": "状态已更新", "order_id": order.id, "status": order.status})


# ============================================================
# 结算 API
# ============================================================

from models.order import SettlementBill


@api_bp.route('/api/settlements', methods=['GET'])
@require_login
def get_settlements():
    """获取当前用户的结算账单"""
    current_user = User.query.get(session.get('user_id'))
    bills = SettlementBill.query.filter(
        db.or_(
            SettlementBill.payer_id == current_user.id,
            SettlementBill.payee_id == current_user.id
        )
    ).order_by(SettlementBill.created_at.desc()).all()
    return jsonify([{
        'id': b.id,
        'bill_no': b.bill_no,
        'biz_type': b.biz_type,
        'biz_order_id': b.biz_order_id,
        'payer_id': b.payer_id,
        'payee_id': b.payee_id,
        'amount': float(b.amount),
        'fee_amount': float(b.fee_amount or 0),
        'subsidy_amount': float(b.subsidy_amount or 0),
        'settle_status': b.settle_status,
        'settle_time': b.settle_time.isoformat() if b.settle_time else None,
        'created_at': b.created_at.isoformat() if b.created_at else None,
        'remark': b.remark,
    } for b in bills])


@api_bp.route('/api/settlements/create', methods=['POST'])
@require_login
def create_settlement():
    """创建结算账单（订单完成时由系统或管理员触发）"""
    current_user = User.query.get(session.get('user_id'))
    if current_user.role_type not in ('admin', 'enterprise'):
        return jsonify({"error": "无权创建结算单"}), 403

    data = request.json
    order_id = data.get('order_id')
    biz_type = data.get('biz_type', 'material')

    if biz_type == 'material':
        order = MaterialOrder.query.get(order_id)
        if not order:
            return jsonify({"error": "订单不存在"}), 404
        amount = float(order.goods_amount or 0)
        payer_id = order.enterprise_id
        payee_id = order.seller_user_id
    else:
        order = ProductOrder.query.get(order_id)
        if not order:
            return jsonify({"error": "订单不存在"}), 404
        amount = float(order.payable_amount or 0)
        payer_id = order.buyer_user_id
        payee_id = order.enterprise_id

    bill = SettlementBill(
        bill_no=f'ST{datetime.now().strftime("%Y%m%d%H%M%S")}{uuid.uuid4().hex[:6].upper()}',
        biz_type=biz_type,
        biz_order_id=order_id,
        payer_id=payer_id,
        payee_id=payee_id,
        amount=amount,
        fee_amount=round(amount * 0.02, 2),  # 平台 2% 服务费
        settle_status='pending',
    )
    db.session.add(bill)
    db.session.commit()

    return jsonify({"message": "结算单已创建", "bill_id": bill.id, "bill_no": bill.bill_no})


# ============================================================
# 用户 API
# ============================================================

@api_bp.route('/api/user/profile', methods=['GET'])
@require_login
def get_user_profile():
    """获取用户个人信息"""
    current_user = User.query.get(session.get('user_id'))
    user_dict = current_user.to_dict()

    if current_user.role_type == 'supplier':
        user_dict['materials_count'] = MaterialSupply.query.filter_by(
            publisher_user_id=current_user.id, is_deleted=False
        ).count()
    elif current_user.role_type == 'buyer':
        user_dict['orders_count'] = MaterialOrder.query.filter_by(
            enterprise_id=current_user.id
        ).count()

    return jsonify(user_dict)


# ============================================================
# 商品有机肥商城 API
# ============================================================

@api_bp.route('/api/products', methods=['GET'])
def get_products():
    """获取商品列表（支持筛选/搜索/排序，包含图片）"""
    query = Product.query.filter_by(is_deleted=False, status='online')

    category_id = request.args.get('category_id')
    enterprise_id = request.args.get('enterprise_id')
    search = request.args.get('search')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    sort_by = request.args.get('sort_by', 'created_at')

    if category_id:
        try: query = query.filter(Product.category_id == int(category_id))
        except ValueError: pass
    if enterprise_id:
        try: query = query.filter(Product.enterprise_id == int(enterprise_id))
        except ValueError: pass
    if search:
        kw = f'%{search}%'
        query = query.filter(db.or_(
            Product.product_name.ilike(kw),
            Product.specification.ilike(kw),
            Product.suitable_crops.ilike(kw),
        ))
    if min_price:
        try: query = query.filter(Product.price >= float(min_price))
        except ValueError: pass
    if max_price:
        try: query = query.filter(Product.price <= float(max_price))
        except ValueError: pass

    if sort_by == 'price_asc':
        query = query.order_by(Product.price.asc())
    elif sort_by == 'price_desc':
        query = query.order_by(Product.price.desc())
    else:
        query = query.order_by(Product.created_at.desc())

    products = query.all()
    result = []
    for p in products:
        d = p.to_dict()
        d['images'] = [{'id': img.id, 'url': img.image_url} for img in p.images]
        result.append(d)
    return jsonify(result)


@api_bp.route('/api/products/<int:product_id>', methods=['GET'])
def get_product_detail(product_id):
    """商品详情（含图片）"""
    product = Product.query.get(product_id)
    if not product or product.is_deleted:
        return jsonify({"error": "商品不存在"}), 404

    data = product.to_dict()
    data['images'] = [{'id': img.id, 'url': img.image_url} for img in product.images]
    return jsonify(data)


@api_bp.route('/api/products', methods=['POST'])
@require_login
def create_product():
    """企业发布商品"""
    current_user = User.query.get(session.get('user_id'))
    if current_user.role_type != 'enterprise':
        return jsonify({"error": "仅企业用户可以上架商品"}), 403

    data = request.json
    required = ['product_name', 'price', 'stock_qty']
    for f in required:
        if not data.get(f):
            return jsonify({"error": f"缺少必填字段: {f}"}), 400

    product = Product(
        enterprise_id=current_user.id,
        category_id=data.get('category_id', 0),
        supplier_name=current_user.company or current_user.username,
        product_name=data['product_name'],
        product_code=data.get('product_code', ''),
        specification=data.get('specification', ''),
        unit=data.get('unit', 'bag'),
        price=data['price'],
        market_price=data.get('market_price'),
        stock_qty=int(data.get('stock_qty', 0)),
        min_order_qty=int(data.get('min_order_qty', 1)),
        delivery_scope=data.get('delivery_scope', ''),
        suitable_crops=data.get('suitable_crops', ''),
        detail_content=data.get('detail_content', ''),
        status='pending_audit',
    )
    db.session.add(product)
    db.session.flush()

    images = data.get('images', [])
    for idx, img_url in enumerate(images):
        db.session.add(ProductImage(product_id=product.id, image_url=img_url, sort_no=idx))

    db.session.commit()
    return jsonify({"message": "商品发布成功，等待审核", "product_id": product.id})


@api_bp.route('/api/products/<int:product_id>', methods=['PUT'])
@require_login
def update_product(product_id):
    """编辑商品"""
    current_user = User.query.get(session.get('user_id'))
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "商品不存在"}), 404
    if product.enterprise_id != current_user.id and current_user.role_type != 'admin':
        return jsonify({"error": "无权编辑"}), 403

    data = request.json
    for field in ['product_name', 'category_id', 'specification', 'unit',
                  'price', 'market_price', 'stock_qty', 'min_order_qty',
                  'delivery_scope', 'suitable_crops', 'detail_content']:
        if field in data and data[field] is not None:
            setattr(product, field, data[field])

    if 'images' in data:
        ProductImage.query.filter_by(product_id=product.id).delete()
        for idx, img_url in enumerate(data['images']):
            db.session.add(ProductImage(product_id=product.id, image_url=img_url, sort_no=idx))

    db.session.commit()
    return jsonify({"message": "商品更新成功"})


@api_bp.route('/api/products/<int:product_id>/status', methods=['POST'])
@require_login
def update_product_status(product_id):
    """商品状态变更"""
    current_user = User.query.get(session.get('user_id'))
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "商品不存在"}), 404

    new_status = request.json.get('status')
    if new_status not in ('pending_audit', 'online', 'offline'):
        return jsonify({"error": "无效状态"}), 400

    if new_status == 'online' and product.status == 'pending_audit':
        if current_user.role_type != 'admin':
            return jsonify({"error": "只有管理员可以审核通过"}), 403
    elif product.enterprise_id != current_user.id and current_user.role_type != 'admin':
        return jsonify({"error": "无权操作"}), 403

    product.status = new_status
    db.session.commit()
    return jsonify({"message": f"商品状态已更新为 {new_status}"})


# ============================================================
# 商品有机肥订单 API
# ============================================================

@api_bp.route('/api/product-orders', methods=['GET'])
@require_login
def get_product_orders():
    """我的商品订单列表（企业看卖出的，买家看买入的）"""
    current_user = User.query.get(session.get('user_id'))
    query = ProductOrder.query.filter_by(is_deleted=False)

    if current_user.role_type == 'enterprise':
        query = query.filter_by(enterprise_id=current_user.id)
    else:
        query = query.filter_by(buyer_user_id=current_user.id)

    query = query.order_by(ProductOrder.created_at.desc())
    orders = query.all()
    return jsonify([o.to_dict() for o in orders])


@api_bp.route('/api/product-order/<int:order_id>', methods=['GET'])
@require_login
def get_product_order_detail(order_id):
    """商品订单详情（含订单项）"""
    current_user = User.query.get(session.get('user_id'))
    order = ProductOrder.query.get(order_id)
    if not order:
        return jsonify({"error": "订单不存在"}), 404
    if order.buyer_user_id != current_user.id and order.enterprise_id != current_user.id:
        return jsonify({"error": "无权查看"}), 403

    data = order.to_dict()
    data['items'] = [{
        'id': item.id, 'product_id': item.product_id,
        'product_name': item.product_name, 'specification': item.specification,
        'unit_price': float(item.unit_price), 'quantity': item.quantity,
        'amount': float(item.amount),
    } for item in order.items]
    return jsonify(data)


@api_bp.route('/api/product-order/create', methods=['POST'])
@require_login
def create_product_order():
    """创建商品订单（支持多商品）"""
    current_user = User.query.get(session.get('user_id'))
    data = request.json
    items_data = data.get('items', [])
    if not items_data:
        return jsonify({"error": "请选择商品"}), 400

    total_amount = 0.0
    enterprise_id = None
    order_items = []

    for item in items_data:
        product = Product.query.get(item['product_id'])
        if not product or product.is_deleted or product.status != 'online':
            return jsonify({"error": f"商品不可购买: {item.get('product_id')}"}), 400

        qty = int(item.get('quantity', 1))
        if product.stock_qty < qty:
            return jsonify({"error": f"库存不足: {product.product_name}"}), 400

        if enterprise_id is None:
            enterprise_id = product.enterprise_id
        elif enterprise_id != product.enterprise_id:
            return jsonify({"error": "一次只能购买同一企业的商品"}), 400

        item_amount = float(product.price) * qty
        total_amount += item_amount
        order_items.append({'product': product, 'qty': qty, 'amount': item_amount})

    order = ProductOrder(
        order_no=f'PO{datetime.now().strftime("%Y%m%d%H%M%S")}{uuid.uuid4().hex[:6].upper()}',
        buyer_user_id=current_user.id,
        buyer_type=current_user.role_type,
        enterprise_id=enterprise_id,
        total_amount=total_amount,
        payable_amount=total_amount,
        pay_status='unpaid',
        order_status='pending',
        receiver_name=data.get('receiver_name', current_user.username),
        receiver_mobile=data.get('receiver_mobile', ''),
        receiver_address=data.get('receiver_address', current_user.address or ''),
        remark=data.get('remark', ''),
    )
    db.session.add(order)
    db.session.flush()

    for oi in order_items:
        p = oi['product']
        db.session.add(ProductOrderItem(
            order_id=order.id, product_id=p.id,
            product_name=p.product_name, specification=p.specification,
            unit_price=p.price, quantity=oi['qty'], amount=oi['amount'],
        ))
        p.stock_qty -= oi['qty']
        if p.stock_qty <= 0:
            p.status = 'offline'

    db.session.commit()
    return jsonify({"message": "订单创建成功", "order_id": order.id, "order": order.to_dict()})


@api_bp.route('/api/product-order/<int:order_id>/pay', methods=['POST'])
@require_login
def pay_product_order(order_id):
    """支付商品订单"""
    current_user = User.query.get(session.get('user_id'))
    order = ProductOrder.query.get(order_id)
    if not order:
        return jsonify({"error": "订单不存在"}), 404
    if order.buyer_user_id != current_user.id:
        return jsonify({"error": "无权操作"}), 403
    if order.pay_status != 'unpaid':
        return jsonify({"error": "订单已支付或已取消"}), 400

    payable = float(order.payable_amount)
    if float(current_user.balance or 0) < payable:
        return jsonify({"error": "余额不足"}), 400

    current_user.balance = float(current_user.balance) - payable
    order.pay_status = 'paid'
    order.order_status = 'paid'
    db.session.commit()
    return jsonify({"message": "支付成功", "order_id": order.id})


@api_bp.route('/api/product-order/<int:order_id>/cancel', methods=['POST'])
@require_login
def cancel_product_order(order_id):
    """取消商品订单（恢复库存）"""
    current_user = User.query.get(session.get('user_id'))
    order = ProductOrder.query.get(order_id)
    if not order:
        return jsonify({"error": "订单不存在"}), 404
    if order.buyer_user_id != current_user.id and current_user.role_type != 'admin':
        return jsonify({"error": "无权操作"}), 403
    if order.pay_status == 'paid':
        return jsonify({"error": "已支付订单不可取消"}), 400

    order.order_status = 'cancelled'
    order.pay_status = 'cancelled'
    for item in order.items:
        product = item.product
        if product:
            product.stock_qty += item.quantity
            if product.status == 'offline' and product.stock_qty > 0:
                product.status = 'online'
    db.session.commit()
    return jsonify({"message": "订单已取消"})


# ============================================================
# 商品购物车 API（session 后端存储）
# ============================================================

def _get_product_cart():
    """获取 session 商品购物车"""
    if 'product_cart' not in session:
        session['product_cart'] = []
    return session['product_cart']


@api_bp.route('/api/product-cart', methods=['GET'])
@require_login
def get_product_cart_api():
    """获取商品购物车"""
    cart = _get_product_cart()
    items = []
    total = 0.0
    for entry in cart:
        prod = Product.query.get(entry['product_id'])
        if prod and prod.status == 'approved':
            price = float(prod.price)
            qty = entry['quantity']
            items.append({
                'product_id': prod.id,
                'product_name': prod.product_name,
                'specification': prod.specification or '',
                'price': price,
                'quantity': qty,
                'stock_qty': prod.stock_qty,
            })
            total += price * qty
    return jsonify({'items': items, 'total': total})


@api_bp.route('/api/product-cart/add', methods=['POST'])
@require_login
def add_product_to_cart():
    """商品加入购物车"""
    data = request.json
    product_id = int(data.get('product_id'))
    quantity = int(data.get('quantity', 1))

    prod = Product.query.get(product_id)
    if not prod:
        return jsonify({"error": "商品不存在"}), 404
    if prod.status != 'approved':
        return jsonify({"error": "商品已下架"}), 400

    cart = _get_product_cart()
    for item in cart:
        if item['product_id'] == product_id:
            item['quantity'] += quantity
            session.modified = True
            return jsonify({"message": "购物车已更新"})

    cart.append({'product_id': product_id, 'quantity': quantity})
    session.modified = True
    return jsonify({"message": "已加入购物车"})


@api_bp.route('/api/product-cart/remove', methods=['POST'])
@require_login
def remove_product_from_cart():
    """从商品购物车移除"""
    product_id = int(request.json.get('product_id'))
    cart = _get_product_cart()
    for i, item in enumerate(cart):
        if item['product_id'] == product_id:
            cart.pop(i)
            session.modified = True
            return jsonify({"message": "已移除"})
    return jsonify({"error": "商品不在购物车中"}), 404


@api_bp.route('/api/product-cart/clear', methods=['POST'])
@require_login
def clear_product_cart():
    """清空商品购物车"""
    session['product_cart'] = []
    session.modified = True
    return jsonify({"message": "购物车已清空"})


# ============================================================
# 评价 API
# ============================================================

from models.review import Review


@api_bp.route('/api/reviews', methods=['GET'])
def get_reviews():
    """获取评价列表（按供给/用户/订单筛选）"""
    query = Review.query
    supply_id = request.args.get('supply_id')
    user_id = request.args.get('user_id')
    order_id = request.args.get('order_id')

    if supply_id:
        query = query.join(MaterialSupply, Review.order_id == MaterialSupply.id)\
                     .filter(Review.order_type == 'material')
    if user_id:
        query = query.filter(db.or_(Review.reviewer_id == int(user_id), Review.reviewee_id == int(user_id)))
    if order_id:
        query = query.filter_by(order_id=int(order_id))

    reviews = query.order_by(Review.created_at.desc()).limit(50).all()
    return jsonify([r.to_dict() for r in reviews])


@api_bp.route('/api/reviews/create', methods=['POST'])
@require_login
def create_review():
    """创建评价"""
    current_user = User.query.get(session.get('user_id'))
    data = request.json

    rating = int(data.get('rating', 5))
    if rating < 1 or rating > 5:
        return jsonify({"error": "评分需在 1-5 之间"}), 400

    reviewee_id = data.get('reviewee_id')
    order_id = data.get('order_id')
    order_type = data.get('order_type', 'material')
    content = data.get('content', '')

    if not reviewee_id:
        return jsonify({"error": "缺少被评价人"}), 400

    # 检查重复评价
    if order_id:
        dup = Review.query.filter_by(reviewer_id=current_user.id, order_id=order_id, order_type=order_type).first()
        if dup:
            return jsonify({"error": "该订单已评价"}), 400

    review = Review(
        reviewer_id=current_user.id,
        reviewee_id=int(reviewee_id),
        order_id=int(order_id) if order_id else None,
        order_type=order_type,
        rating=rating,
        content=content,
    )
    db.session.add(review)
    db.session.flush()

    # 更新供给评分（如果是原料评价）
    if order_type == 'material' and order_id:
        from models.supply import MaterialSupply
        supply = MaterialSupply.query.filter_by(publisher_user_id=reviewee_id).first()
        if supply:
            avg = db.session.query(db.func.avg(Review.rating)).filter_by(reviewee_id=reviewee_id).scalar()
            count = Review.query.filter_by(reviewee_id=reviewee_id).count()
            supply.rating = round(float(avg), 1) if avg else 5.0
            supply.review_count = count

    db.session.commit()
    return jsonify({"message": "评价成功", "review_id": review.id})


# ============================================================
# 管理 API
# ============================================================

@api_bp.route('/api/admin/stats', methods=['GET'])
@require_role('admin')
def admin_stats():
    """管理员统计数据（总控室看板：用户/企业/司机/商品/订单/交易额）"""
    from collections import Counter
    role_counter = Counter(r[0] for r in db.session.query(User.role_type).filter(User.is_deleted == False).all())
    paid_orders = ProductOrder.query.filter(
        ProductOrder.pay_status == 'paid',
        ProductOrder.is_deleted == False
    ).all()
    total_amount = sum(float(o.total_amount or 0) for o in paid_orders)
    stats = {
        "total_users": User.query.filter_by(is_deleted=False).count(),
        "role_users": dict(role_counter),
        "farmers": role_counter.get('farmer', 0),
        "suppliers": role_counter.get('supplier', 0),
        "enterprises": role_counter.get('enterprise', 0),
        "drivers": role_counter.get('driver', 0),
        "buyers": role_counter.get('buyer', 0),
        "experts": role_counter.get('expert', 0),
        "total_materials": MaterialSupply.query.filter_by(is_deleted=False).count(),
        "available_materials": MaterialSupply.query.filter_by(is_available=True, is_deleted=False).count(),
        "pending_materials": MaterialSupply.query.filter_by(audit_status='pending', is_deleted=False).count(),
        "total_products": Product.query.filter_by(is_deleted=False).count(),
        "online_products": Product.query.filter_by(status='online', is_deleted=False).count(),
        "pending_products": Product.query.filter_by(status='pending_audit', is_deleted=False).count(),
        "total_orders": ProductOrder.query.filter_by(is_deleted=False).count(),
        "paid_orders": len(paid_orders),
        "total_amount": total_amount,
        "total_demands": MaterialDemand.query.filter_by(is_deleted=False).count(),
        "active_demands": MaterialDemand.query.filter_by(status='active', is_deleted=False).count(),
        "recent_activities": []
    }
    return jsonify(stats)


# ============================================================
# 聊天 API（简化版，session 存储）
# ============================================================

@api_bp.route('/api/chat/message', methods=['POST'])
@require_login
def send_chat_message():
    """发送聊天消息"""
    data = request.json
    message = data.get('message')
    to_user_id = data.get('to_user_id')

    if not message:
        return jsonify({"error": "消息不能为空"}), 400

    from models.system import MessageNotice
    current_user = User.query.get(session.get('user_id'))

    notice = MessageNotice(
        from_user_id=current_user.id,
        to_user_id=to_user_id,
        msg_type='chat',
        title=f'来自 {current_user.username} 的消息',
        content=message,
        is_read=False,
    )
    db.session.add(notice)
    db.session.commit()

    return jsonify({
        "message": "消息已发送",
        "msg_id": notice.id,
        "from": current_user.id,
        "content": message,
        "timestamp": datetime.now(timezone.utc).isoformat()
    })


@api_bp.route('/api/chat/messages', methods=['GET'])
@require_login
def get_chat_messages():
    """获取当前用户的消息列表"""
    current_user = User.query.get(session.get('user_id'))
    from models.system import MessageNotice
    notices = MessageNotice.query.filter_by(to_user_id=current_user.id, is_deleted=False)\
                                 .order_by(MessageNotice.created_at.desc()).limit(50).all()
    return jsonify([{
        'id': n.id,
        'from_user_id': n.from_user_id,
        'msg_type': n.msg_type,
        'title': n.title,
        'content': n.content,
        'is_read': n.is_read,
        'created_at': n.created_at.isoformat() if n.created_at else None,
    } for n in notices])


@api_bp.route('/api/chat/messages/<int:msg_id>/read', methods=['POST'])
@require_login
def mark_message_read(msg_id):
    """标记消息已读"""
    from models.system import MessageNotice
    notice = MessageNotice.query.get(msg_id)
    if not notice:
        return jsonify({"error": "消息不存在"}), 404
    notice.is_read = True
    db.session.commit()
    return jsonify({"message": "已标记已读"})
