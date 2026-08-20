#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from datetime import datetime, timezone
from models import db, User
from utils import generate_id, hash_password, verify_password, get_current_user

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login')
def login_page():
    """登录页面"""
    current_user = get_current_user()
    if current_user:
        return redirect(url_for('main.home'))
    return render_template('login.html')


@auth_bp.route('/register')
def register_page():
    """注册页面"""
    current_user = get_current_user()
    if current_user:
        return redirect(url_for('main.home'))
    return render_template('register.html')


@auth_bp.route('/logout')
def logout():
    """用户登出"""
    session.clear()
    return redirect(url_for('main.home'))


@auth_bp.route('/api/login', methods=['POST'])
def login_api():
    """用户登录API"""
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "用户名和密码不能为空"}), 400

    # 查找用户
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "用户名或密码错误"}), 401

    # 验证密码（兼容旧 SHA-256）
    is_valid, needs_rehash = verify_password(password, user.password_hash)
    if not is_valid:
        return jsonify({"error": "用户名或密码错误"}), 401

    # 旧密码自动升级为 bcrypt
    if needs_rehash:
        user.password_hash = hash_password(password)

    # 更新登录时间
    user.last_login_at = datetime.now(timezone.utc)
    db.session.commit()

    # 设置session
    session['user_id'] = user.id
    session['username'] = user.username
    session['role'] = user.role_type

    return jsonify({
        "message": "登录成功",
        "user": {
            "id": user.id,
            "username": user.username,
            "role": user.role_type,
            "avatar": user.avatar,
            "credit_score": user.credit_score
        }
    })


@auth_bp.route('/api/register', methods=['POST'])
def register_api():
    """用户注册API"""
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    phone = data.get('phone')
    role = data.get('role', 'buyer')

    # 验证必填字段
    if not all([username, password, email, phone]):
        return jsonify({"error": "缺少必填字段"}), 400

    # 检查用户名是否已存在
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "用户名已存在"}), 400

    # 创建用户
    user = User(
        username=username,
        password_hash=hash_password(password),
        role_type=role,
        email=email,
        phone=phone,
        avatar=f"https://api.dicebear.com/7.x/avataaars/svg?seed={username}",
        company=data.get('company', ''),
        address=data.get('address', ''),
        balance=0.0,
        credit_score=80,
        is_verified=False,
        status='normal',
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "注册成功",
        "user_id": user.id,
        "username": user.username,
        "role": user.role_type
    })


# ============================================================
# 微信登录 API
# ============================================================

@auth_bp.route('/api/wechat-login', methods=['POST'])
def wechat_login():
    """微信一键登录（接收前端 wx.login() 返回的 code）"""
    import os
    import requests as http_requests

    data = request.json
    code = data.get('code')

    if not code:
        return jsonify({"error": "缺少微信 code"}), 400

    # 从环境变量读取微信配置
    appid = os.environ.get('WECHAT_APPID', '')
    secret = os.environ.get('WECHAT_SECRET', '')

    if not appid or not secret:
        # 降级：如果没有微信配置，用模拟数据（开发环境）
        mock_openid = f'mock_wechat_{code[:8]}'
        user = User.query.filter_by(wechat_openid=mock_openid).first()
        if not user:
            user = User(
                username=f'微信用户{mock_openid[-4:]}',
                password_hash=hash_password(mock_openid),
                role_type='farmer',
                wechat_openid=mock_openid,
                avatar='https://api.dicebear.com/7.x/avataaars/svg?seed=' + mock_openid,
                balance=0.0,
                credit_score=80,
                is_verified=True,
                status='normal',
            )
            db.session.add(user)
            db.session.commit()
    else:
        # 调用微信 code2session
        try:
            resp = http_requests.get(
                'https://api.weixin.qq.com/sns/jscode2session',
                params={'appid': appid, 'secret': secret, 'js_code': code, 'grant_type': 'authorization_code'},
                timeout=5,
            )
            wx_data = resp.json()
            openid = wx_data.get('openid')
            if not openid:
                return jsonify({"error": f"微信登录失败: {wx_data.get('errmsg', '未知错误')}"}), 400
        except Exception as e:
            return jsonify({"error": f"微信接口调用失败: {str(e)}"}), 500

        user = User.query.filter_by(wechat_openid=openid).first()
        if not user:
            user = User(
                username=f'微信用户{openid[-6:]}',
                password_hash=hash_password(openid),
                role_type='farmer',
                wechat_openid=openid,
                avatar='https://api.dicebear.com/7.x/avataaars/svg?seed=' + openid,
                balance=0.0,
                credit_score=80,
                is_verified=True,
                status='normal',
            )
            db.session.add(user)
            db.session.commit()

    # 设置 session
    user.last_login_at = datetime.now(timezone.utc)
    db.session.commit()

    session['user_id'] = user.id
    session['username'] = user.username
    session['role'] = user.role_type

    return jsonify({
        "message": "登录成功",
        "user": {
            "id": user.id,
            "username": user.username,
            "role": user.role_type,
            "avatar": user.avatar,
            "credit_score": user.credit_score,
        }
    })
