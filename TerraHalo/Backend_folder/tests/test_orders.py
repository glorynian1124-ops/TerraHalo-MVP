"""订单 API 测试"""
import os
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'

import pytest, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import create_app
from models import db, User

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test'
    with app.app_context():
        db.create_all()
    with app.test_client() as c:
        # 供应商发布原料
        c.post('/api/register', json={'username':'supplier','password':'123','email':'s@t.com','phone':'13800000001','role':'supplier'})
        c.post('/api/login', json={'username':'supplier','password':'123'})
        c.post('/api/materials', json={'category_id':1,'estimated_weight':100,'price':150,'province':'江苏','city':'南京','detail_address':'江宁'})
        c.get('/logout')
        # 买家注册登录
        c.post('/api/register', json={'username':'buyer','password':'123','email':'b@t.com','phone':'13800000002','role':'buyer','company':'测试公司','address':'南京'})
        c.post('/api/login', json={'username':'buyer','password':'123'})
        # 给买家充值（支付需要余额）
        with app.app_context():
            buyer = User.query.filter_by(username='buyer').first()
            buyer.balance = 10000.0
            db.session.commit()
        yield c

def test_create_order(client):
    mats = client.get('/api/materials').get_json()
    assert len(mats) > 0
    res = client.post('/api/order/create', json={'items':[{'material_id':mats[0]['id'],'quantity':1}]})
    assert res.status_code == 200
    assert 'order_id' in res.get_json()

def test_get_orders(client):
    mats = client.get('/api/materials').get_json()
    client.post('/api/order/create', json={'items':[{'material_id':mats[0]['id'],'quantity':1}]})
    res = client.get('/api/orders')
    assert res.status_code == 200
    assert len(res.get_json()) >= 1

def test_pay_order(client):
    mats = client.get('/api/materials').get_json()
    r = client.post('/api/order/create', json={'items':[{'material_id':mats[0]['id'],'quantity':1}]})
    oid = r.get_json()['order_id']
    res = client.post('/api/order/pay', json={'order_id':oid})
    assert res.status_code == 200

def test_order_status_flow(client):
    mats = client.get('/api/materials').get_json()
    r = client.post('/api/order/create', json={'items':[{'material_id':mats[0]['id'],'quantity':1}]})
    oid = r.get_json()['order_id']
    # 支付
    client.post('/api/order/pay', json={'order_id':oid})
    # 派单
    res = client.post(f'/api/order/{oid}/status', json={'status':'dispatched'})
    assert res.status_code == 200
    # 运输
    res = client.post(f'/api/order/{oid}/status', json={'status':'transported'})
    assert res.status_code == 200
    # 签收
    res = client.post(f'/api/order/{oid}/status', json={'status':'signed'})
    assert res.status_code == 200
    # 结算
    res = client.post(f'/api/order/{oid}/status', json={'status':'settled'})
    assert res.status_code == 200

def test_invalid_status_transition(client):
    mats = client.get('/api/materials').get_json()
    r = client.post('/api/order/create', json={'items':[{'material_id':mats[0]['id'],'quantity':1}]})
    oid = r.get_json()['order_id']
    # 直接跳到 signed（不允许）
    res = client.post(f'/api/order/{oid}/status', json={'status':'signed'})
    assert res.status_code == 400
