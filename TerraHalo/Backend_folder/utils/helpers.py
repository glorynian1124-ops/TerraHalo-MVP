#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import uuid
import hashlib
import bcrypt
from functools import wraps
from flask import session, request, jsonify, redirect, url_for


def generate_id():
    """生成唯一ID"""
    return str(uuid.uuid4())


def hash_password(password):
    """使用 bcrypt 哈希密码"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_password(password, password_hash):
    """
    验证密码，兼容旧 SHA-256 格式。
    返回 (is_valid, needs_rehash) 元组。
    - is_valid: 密码是否正确
    - needs_rehash: 是否需要升级哈希（旧 SHA-256 用户首次登录时为 True）
    """
    # bcrypt hash 以 $2b$ 或 $2a$ 开头
    if password_hash.startswith('$2'):
        try:
            return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8')), False
        except ValueError:
            return False, False

    # 兼容旧 SHA-256 格式（64 字符 hex）
    if len(password_hash) == 64:
        old_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        if old_hash == password_hash:
            return True, True  # 密码正确，需要升级
        return False, False

    return False, False


def require_login(f):
    """登录验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from models import User
        user_id = session.get('user_id')
        if not user_id:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({"error": "请先登录"}), 401
            return redirect(url_for('auth.login_page'))
        user = User.query.get(user_id)
        if not user or user.is_deleted:
            session.clear()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({"error": "请先登录"}), 401
            return redirect(url_for('auth.login_page'))
        return f(*args, **kwargs)
    return decorated_function


def require_role(role):
    """角色权限验证装饰器"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from models import User
            user_id = session.get('user_id')
            if not user_id:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return jsonify({"error": "请先登录"}), 401
                return redirect(url_for('auth.login_page'))
            user = User.query.get(user_id)
            if not user or user.is_deleted:
                session.clear()
                return jsonify({"error": "请先登录"}), 401
            if user.role_type != role and user.role_type != 'admin':
                return jsonify({"error": "权限不足"}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def calculate_credit_score(user_id):
    """计算用户信用分（5分制转100分制）"""
    from models import User
    user = User.query.get(user_id)
    if not user:
        return 80
    # TODO: 接入评价表后实现真实计算
    return user.credit_score


def get_current_user():
    """获取当前登录用户（返回 User ORM 对象或 None）"""
    from models import User
    user_id = session.get('user_id')
    if user_id:
        return User.query.get(user_id)
    return None
