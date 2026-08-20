"""原料 API 测试"""
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
        # 注册供应商
        c.post('/api/register', json={'username':'supplier','password':'123456','email':'s@t.com','phone':'13800000001','role':'supplier'})
        c.post('/api/login', json={'username':'supplier','password':'123456'})
        yield c

def test_get_materials_empty(client):
    res = client.get('/api/materials')
    assert res.status_code == 200
    assert isinstance(res.get_json(), list)

def test_publish_material(client):
    res = client.post('/api/materials', json={
        'category_id':1,'estimated_weight':100,'price':150,'province':'江苏','city':'南京','detail_address':'江宁区'
    })
    assert res.status_code == 200
    assert 'material_id' in res.get_json()

def test_get_materials_after_publish(client):
    client.post('/api/materials', json={'category_id':2,'estimated_weight':200,'price':80,'province':'安徽','city':'滁州','detail_address':'来安县'})
    res = client.get('/api/materials')
    assert len(res.get_json()) >= 1

def test_toggle_material(client):
    r = client.post('/api/materials', json={'category_id':3,'estimated_weight':50,'price':100,'province':'江苏','city':'苏州','detail_address':'吴中区'})
    mid = r.get_json()['material_id']
    res = client.post('/api/materials/toggle', json={'material_id':mid})
    assert res.status_code == 200

def test_get_material_by_id(client):
    r = client.post('/api/materials', json={'category_id':4,'estimated_weight':80,'price':120,'province':'浙江','city':'杭州','detail_address':'余杭区'})
    mid = r.get_json()['material_id']
    res = client.get(f'/api/materials?id={mid}')
    assert res.status_code == 200
