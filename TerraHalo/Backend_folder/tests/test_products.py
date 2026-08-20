"""商品有机肥商城 API 测试"""
import os
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'

import pytest, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import create_app
from models import db, User
from models.product import Product, ProductCategory, ProductOrder

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test'
    with app.app_context():
        db.create_all()
        db.session.add(ProductCategory(id=1, name='有机肥料', status='active'))
        db.session.commit()
    with app.test_client() as c:
        # 注册企业 + 发布商品
        c.post('/api/register', json={'username':'ent','password':'123','email':'e@t.com','phone':'13800000001','role':'enterprise','company':'测试有机肥公司'})
        c.post('/api/login', json={'username':'ent','password':'123'})
        c.post('/api/products', json={
            'product_name':'测试有机肥','category_id':1,'price':80,'stock_qty':100,
            'specification':'40kg/袋','images':['http://img.com/1.jpg']
        })
        # 审核
        with app.app_context():
            p = Product.query.first()
            if p and p.status == 'pending_audit':
                p.status = 'online'
                db.session.commit()
        c.get('/logout')
        # 注册买家 + 充值
        c.post('/api/register', json={'username':'farmer1','password':'123','email':'f@t.com','phone':'13800000002','role':'farmer'})
        c.post('/api/login', json={'username':'farmer1','password':'123'})
        with app.app_context():
            buyer = User.query.filter_by(username='farmer1').first()
            buyer.balance = 10000.0
            db.session.commit()
        yield c

def test_get_products(client):
    res = client.get('/api/products')
    assert res.status_code == 200
    data = res.get_json()
    assert len(data) >= 1
    assert data[0]['product_name'] == '测试有机肥'
    assert len(data[0].get('images', [])) == 1

def test_get_product_detail(client):
    res = client.get('/api/products/1')
    assert res.status_code == 200
    assert res.get_json()['product_name'] == '测试有机肥'
    assert len(res.get_json()['images']) == 1

def test_get_products_by_category(client):
    res = client.get('/api/products?category_id=1')
    assert res.status_code == 200
    assert len(res.get_json()) >= 1

def test_get_products_search(client):
    res = client.get('/api/products?search=有机肥')
    assert res.status_code == 200
    assert len(res.get_json()) >= 1

def test_create_product(client):
    client.get('/logout')
    client.post('/api/login', json={'username':'ent','password':'123'})
    res = client.post('/api/products', json={
        'product_name':'新商品','category_id':1,'price':100,'stock_qty':50
    })
    assert res.status_code == 200
    assert 'product_id' in res.get_json()

def test_update_product(client):
    client.get('/logout')
    client.post('/api/login', json={'username':'ent','password':'123'})
    res = client.put('/api/products/1', json={'price':90,'stock_qty':200})
    assert res.status_code == 200

def test_product_status(client):
    client.get('/logout')
    client.post('/api/login', json={'username':'ent','password':'123'})
    res = client.post('/api/products/1/status', json={'status':'offline'})
    assert res.status_code == 200

def test_create_product_order(client):
    res = client.post('/api/product-order/create', json={
        'items':[{'product_id':1,'quantity':2}],
        'receiver_name':'张三','receiver_mobile':'13900000000','receiver_address':'南京'
    })
    assert res.status_code == 200
    assert 'order_id' in res.get_json()

def test_pay_product_order(client):
    r = client.post('/api/product-order/create', json={'items':[{'product_id':1,'quantity':1}]})
    oid = r.get_json()['order_id']
    res = client.post(f'/api/product-order/{oid}/pay')
    assert res.status_code == 200

def test_cancel_product_order(client):
    r = client.post('/api/product-order/create', json={'items':[{'product_id':1,'quantity':1}]})
    oid = r.get_json()['order_id']
    res = client.post(f'/api/product-order/{oid}/cancel')
    assert res.status_code == 200

def test_get_product_orders(client):
    client.post('/api/product-order/create', json={'items':[{'product_id':1,'quantity':1}]})
    res = client.get('/api/product-orders')
    assert res.status_code == 200
    assert len(res.get_json()) >= 1
