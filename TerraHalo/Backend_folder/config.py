#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
沃土之环 - 应用配置模块
所有配置优先从环境变量读取，fallback 到默认值。
"""

import os


class Config:
    """基础配置"""
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY', 'terrahalo_dev_key_change_in_production')
    DEBUG = os.environ.get('DEBUG', 'false').lower() == 'true'
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', '5000'))

    # Session
    PERMANENT_SESSION_LIFETIME = 7 * 24 * 60 * 60  # 7 天

    # 数据库（默认 SQLite，设 DATABASE_URL 环境变量可切换 MySQL）
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        f'sqlite:///{os.path.join(basedir, "terrahalo.db")}'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = os.environ.get('SQLALCHEMY_ECHO', 'false').lower() == 'true'


class DevelopmentConfig(Config):
    """开发环境"""
    DEBUG = True


class ProductionConfig(Config):
    """生产环境"""
    DEBUG = False


class TestingConfig(Config):
    """测试环境"""
    DEBUG = True
    TESTING = True


# 配置映射
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
}


def get_config():
    """根据环境变量获取对应配置类"""
    env = os.environ.get('FLASK_ENV', 'development')
    return config_by_name.get(env, DevelopmentConfig)
