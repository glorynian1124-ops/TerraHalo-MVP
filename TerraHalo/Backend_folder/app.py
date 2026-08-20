#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
沃土之环 - 有机肥原料交易平台
主应用程序入口 (API后端)
"""

from flask import Flask, session, g
from datetime import timedelta, datetime, timezone
from flask_cors import CORS
from flask_migrate import Migrate

# 导入自定义模块
from models import db, User, Enterprise, MaterialSupply, MaterialCategory, Driver
from models.product import Product, ProductCategory, ProductImage
from utils import get_current_user, hash_password
from config import get_config

# 导入蓝图
from routes import main, auth, materials as materials_routes, cart, orders as orders_routes, api, enterprise, driver, admin

CATEGORIES = [
    {"id": 1, "name": "畜禽粪便", "description": "鸡粪、牛粪、猪粪等"},
    {"id": 2, "name": "农作物秸秆", "description": "玉米秆、稻草、麦秸等"},
    {"id": 3, "name": "厨余垃圾", "description": "果蔬废料、食品残渣等"},
    {"id": 4, "name": "工业副产品", "description": "酒糟、豆渣、糖渣等"},
    {"id": 5, "name": "绿肥植物", "description": "紫云英、苕子、草木樨等"}
]


def seed_data():
    """初始化测试数据（幂等：已存在则跳过）"""
    if User.query.filter_by(username='admin').first():
        return  # 已初始化

    now = datetime.now(timezone.utc)

    # 管理员
    admin = User(
        username='admin',
        password_hash=hash_password('admin123'),
        role_type='admin',
        email='admin@terrahalo.com',
        phone='13800138000',
        avatar='https://api.dicebear.com/7.x/avataaars/svg?seed=admin',
        balance=0.0,
        credit_score=100,
        is_verified=True,
        status='normal',
        last_login_at=now,
    )
    db.session.add(admin)

    # 供应商
    supplier = User(
        username='绿色农场',
        password_hash=hash_password('123456'),
        role_type='supplier',
        email='farm@example.com',
        phone='13900139000',
        avatar='https://api.dicebear.com/7.x/avataaars/svg?seed=farm',
        company='绿色有机农场',
        address='江苏省南京市江宁区',
        balance=0.0,
        credit_score=95,
        is_verified=True,
        status='normal',
        last_login_at=now,
    )
    db.session.add(supplier)

    # 买家
    buyer = User(
        username='有机肥厂',
        password_hash=hash_password('123456'),
        role_type='enterprise',
        email='factory@example.com',
        phone='13700137000',
        avatar='https://api.dicebear.com/7.x/avataaars/svg?seed=factory',
        company='华东有机肥有限公司',
        address='浙江省杭州市余杭区',
        balance=10000.0,
        credit_score=88,
        is_verified=True,
        status='normal',
        last_login_at=now,
    )
    db.session.add(buyer)

    # 司机
    driver_user = User(
        username='司机小李',
        password_hash=hash_password('123456'),
        role_type='driver',
        email='driver@example.com',
        phone='13600136000',
        avatar='https://api.dicebear.com/7.x/avataaars/svg?seed=driver',
        company='个体运输',
        address='江苏省南京市',
        balance=0.0,
        credit_score=90,
        is_verified=True,
        status='normal',
        last_login_at=now,
    )
    db.session.add(driver_user)
    db.session.flush()

    # 司机车辆信息
    d = Driver(
        user_id=driver_user.id,
        vehicle_type='厢式货车',
        vehicle_no='苏A12345',
        vehicle_capacity_ton=5.0,
        id_card_no='320100199001011234',
        audit_status='approved',
    )
    db.session.add(d)

    db.session.flush()

    # === 创建标准品类 ===
    cat_data = [
        (1, '畜禽粪便', '鸡粪、牛粪、猪粪等'),
        (2, '农作物秸秆', '玉米秆、稻草、麦秸等'),
        (3, '厨余垃圾', '果蔬废料、食品残渣等'),
        (4, '工业副产品', '酒糟、豆渣、糖渣等'),
        (5, '绿肥植物', '紫云英、苕子、草木樨等'),
    ]
    cat_map = {}
    for cid, cname, cdesc in cat_data:
        cat = MaterialCategory(id=cid, name=cname, code=f'MC{cid:03d}', description=cdesc, status='active', sort_no=cid)
        db.session.add(cat)
        cat_map[cname] = cid
    db.session.flush()

    # === 示例原料（使用 MVP 完整字段）===
    sample_materials = [
        MaterialSupply(
            supply_no=f'MS-SEED-{i+1:03d}',
            publisher_user_id=supplier.id,
            publisher_type='supplier',
            category_id=cat_id,
            # 兼容字段
            type=t, supplier_name=supplier.username, quantity=q, location=loc,
            price=p, description=desc, moisture=m, organic_matter=om,
            is_available=True, rating=r, review_count=rc,
            # MVP 标准字段
            estimated_weight=q, weight_unit='kg',
            moisture_range=m,
            impurity_desc='无' if '无杂质' in desc else '少量杂质',
            packaging_type='散装',
            loadable_flag=True,
            province=prov, city=city, district='', detail_address=loc,
            status='approved', audit_status='approved',
        )
        for i, (t, cat_id, q, loc, p, desc, m, om, r, rc, prov, city) in enumerate([
            ('牛粪', 1, 100.0, '江苏省南京市江宁区', 150.0, '优质发酵牛粪，有机质含量高，无杂质',
             '30%', '45%', 4.5, 12, '江苏省', '南京市'),
            ('鸡粪', 1, 80.0, '江苏省南京市六合区', 180.0, '干鸡粪，氮磷钾含量均衡，发酵完全',
             '25%', '50%', 4.2, 8, '江苏省', '南京市'),
            ('农作物秸秆', 2, 200.0, '安徽省滁州市来安县', 80.0, '玉米秸秆，粉碎后可直接使用，含水率低',
             '15%', '40%', 4.0, 5, '安徽省', '滁州市'),
            ('厨余垃圾', 3, 150.0, '江苏省苏州市吴中区', 100.0, '餐饮厨余垃圾，分拣处理，无有害物质',
             '60%', '70%', 3.8, 3, '江苏省', '苏州市'),
            ('猪粪', 1, 120.0, '江苏省无锡市江阴市', 160.0, '发酵猪粪，肥效持久，适合果树种植',
             '35%', '48%', 4.3, 10, '江苏省', '无锡市'),
            ('酒糟', 4, 50.0, '江苏省宿迁市泗洪县', 120.0, '白酒酒糟，蛋白质含量高，适合饲料添加',
             '55%', '65%', 4.1, 6, '江苏省', '宿迁市'),
        ])
    ]
    for m in sample_materials:
        db.session.add(m)

    # === 商品有机肥品类 ===
    product_cats = [
        (1, '有机肥料', '生物有机肥、微生物菌剂等'),
        (2, '土壤调理剂', '土壤改良剂、修复剂'),
        (3, '营养基质', '育苗基质、栽培基质'),
        (4, '叶面肥', '液体叶面肥、微量元素肥'),
    ]
    for pc_id, pc_name, pc_desc in product_cats:
        if not ProductCategory.query.get(pc_id):
            db.session.add(ProductCategory(id=pc_id, name=pc_name, description=pc_desc, status='active'))

    db.session.flush()

    # === 企业档案（enterprise 表，供总控室展示资质）===
    buyer_enterprise = User.query.filter_by(username='有机肥厂').first()
    if buyer_enterprise and not Enterprise.query.filter_by(user_id=buyer_enterprise.id).first():
        db.session.add(Enterprise(
            user_id=buyer_enterprise.id,
            enterprise_name=buyer_enterprise.company or '华东有机肥有限公司',
            enterprise_type='organic_fertilizer',
            license_no='91330100MA2BXXXXXX',
            contact_name='张厂长',
            contact_mobile=buyer_enterprise.phone,
            address=buyer_enterprise.address,
            service_radius_km=80,
            audit_status='approved',
        ))
        db.session.flush()

    # === 示例商品（来自有机肥厂）===
    sample_products = [
        Product(
            enterprise_id=buyer_enterprise.id,
            category_id=1,
            supplier_name=buyer_enterprise.company,
            product_name='高效生物有机肥（通用型）',
            product_code='BOF-001',
            specification='40kg/袋',
            unit='bag',
            price=85.00,
            market_price=120.00,
            stock_qty=500,
            min_order_qty=5,
            suitable_crops='水稻、小麦、玉米、蔬菜',
            detail_content='以畜禽粪便为主要原料，经高温好氧发酵制成。富含有机质和有益微生物，可显著改善土壤结构，提高作物产量。',
            status='online',
        ),
        Product(
            enterprise_id=buyer_enterprise.id,
            category_id=1,
            supplier_name=buyer_enterprise.company,
            product_name='果树专用有机肥',
            product_code='BOF-002',
            specification='40kg/袋',
            unit='bag',
            price=95.00,
            market_price=135.00,
            stock_qty=300,
            min_order_qty=3,
            suitable_crops='柑橘、苹果、桃、梨等果树',
            detail_content='针对果树需肥特性研发，氮磷钾配比均衡，添加中微量元素。促进花芽分化，提高果实品质。',
            status='online',
        ),
        Product(
            enterprise_id=buyer_enterprise.id,
            category_id=3,
            supplier_name=buyer_enterprise.company,
            product_name='蔬菜育苗专用基质',
            product_code='SUB-001',
            specification='50L/袋',
            unit='bag',
            price=25.00,
            market_price=38.00,
            stock_qty=800,
            min_order_qty=10,
            suitable_crops='蔬菜、花卉育苗',
            detail_content='由优质草炭、蛭石、珍珠岩科学配比而成，添加生物菌剂。透气保水，出苗整齐健壮。',
            status='online',
        ),
        Product(
            enterprise_id=buyer_enterprise.id,
            category_id=2,
            supplier_name=buyer_enterprise.company,
            product_name='酸性土壤改良剂',
            product_code='SC-001',
            specification='25kg/袋',
            unit='bag',
            price=45.00,
            market_price=68.00,
            stock_qty=200,
            min_order_qty=2,
            suitable_crops='适用于南方酸性土壤区域',
            detail_content='以贝壳粉、白云石粉为主要原料，调节土壤pH值，补充钙镁元素。缓释长效，安全环保。',
            status='pending_audit',
        ),
    ]
    for p in sample_products:
        db.session.add(p)
    db.session.flush()

    # 商品图片
    sample_images = [
        (1, 'https://images.unsplash.com/photo-1585336261576-3b408cf0bea5?w=400'),
        (1, 'https://images.unsplash.com/photo-1599685317323-f9cd5b16b3ea?w=400'),
        (2, 'https://images.unsplash.com/photo-1551033541-1d5c3e1dac1c?w=400'),
    ]
    for prod_idx, url in sample_images:
        db.session.add(ProductImage(product_id=prod_idx, image_url=url, sort_no=0))

    db.session.commit()
    print("[OK] 测试数据初始化完成（含5个品类 + 6条MVP完整供给 + 4个商品品类 + 4个示例商品）")


def create_app():
    """创建并配置 Flask 应用"""
    app = Flask(__name__)

    # 加载配置
    config = get_config()
    app.config.from_object(config)
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
    
    # 启用CORS（允许跨域携带 cookie，H5 模式必需）
    CORS(app, supports_credentials=True)

    # 初始化数据库
    db.init_app(app)
    Migrate(app, db)

    # 注册蓝图
    app.register_blueprint(main.main_bp)
    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(materials_routes.materials_bp)
    app.register_blueprint(cart.cart_bp)
    app.register_blueprint(orders_routes.orders_bp)
    app.register_blueprint(api.api_bp)
    app.register_blueprint(enterprise.enterprise_bp)
    app.register_blueprint(driver.driver_bp)
    app.register_blueprint(admin.admin_bp)

    # 上下文处理器 - 自动传递 current_user 到模板
    @app.context_processor
    def inject_user():
        current_user = get_current_user()
        categories = MaterialCategory.query.filter_by(status='active').order_by(MaterialCategory.sort_no).all()
        return {
            'current_user': current_user,
            'categories': categories
        }

    return app


if __name__ == '__main__':
    # 创建应用实例
    app = create_app()

    # 创建表并初始化种子数据
    with app.app_context():
        db.create_all()
        seed_data()

    # 输出启动信息
    print("=" * 60)
    print("[OK] 沃土之环有机肥原料交易平台后端API已启动")
    print("    API地址：http://127.0.0.1:5000/")
    print("=" * 60)
    print("    测试账户：")
    print("    [管理员] admin / admin123")
    print("    [供应商] 绿色农场 / 123456")
    print("    [企业]   有机肥厂 / 123456")
    print("    [司机]   司机小李 / 123456")
    print("=" * 60)

    # 启动应用
    app.run(debug=app.config.get('DEBUG', False),
            port=app.config.get('PORT', 5000),
            host=app.config.get('HOST', '0.0.0.0'))
