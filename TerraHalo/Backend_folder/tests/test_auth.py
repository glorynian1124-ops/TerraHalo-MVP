"""认证 API 测试"""
import os
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'

import pytest
import sys
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
        yield c

def test_register_success(client):
    res = client.post('/api/register', json={
        'username':'testuser','password':'123456','email':'a@b.com','phone':'13800138000','role':'farmer'
    })
    assert res.status_code == 200
    assert '注册成功' in res.get_json()['message']

def test_register_duplicate(client):
    client.post('/api/register', json={'username':'dup','password':'123456','email':'a@b.com','phone':'13800138001','role':'farmer'})
    res = client.post('/api/register', json={'username':'dup','password':'123456','email':'c@d.com','phone':'13800138002','role':'farmer'})
    assert res.status_code == 400

def test_login_success(client):
    client.post('/api/register', json={'username':'logintest','password':'123456','email':'e@f.com','phone':'13800138003','role':'farmer'})
    res = client.post('/api/login', json={'username':'logintest','password':'123456'})
    assert res.status_code == 200
    assert res.get_json()['user']['username'] == 'logintest'

def test_login_wrong_password(client):
    client.post('/api/register', json={'username':'wrongpw','password':'123456','email':'g@h.com','phone':'13800138004','role':'farmer'})
    res = client.post('/api/login', json={'username':'wrongpw','password':'000000'})
    assert res.status_code == 401

def test_logout(client):
    client.post('/api/register', json={'username':'logouttest','password':'123456','email':'i@j.com','phone':'13800138005','role':'farmer'})
    client.post('/api/login', json={'username':'logouttest','password':'123456'})
    res = client.get('/logout')
    assert res.status_code in (200, 302)
