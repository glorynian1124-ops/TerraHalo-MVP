#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
匹配引擎 — 供给与需求自动匹配
规则：供给.type == 需求.category_name AND 供给.quantity >= 需求.min_weight
"""

from models import db, MaterialSupply, MaterialDemand, SupplyDemandMatch
from math import radians, sin, cos, sqrt, atan2


def haversine_km(lat1, lng1, lat2, lng2):
    """计算两点间的直线距离（km），使用 Haversine 公式"""
    if not all([lat1, lng1, lat2, lng2]):
        return None
    R = 6371.0
    dlat = radians(float(lat2) - float(lat1))
    dlng = radians(float(lng2) - float(lng1))
    a = sin(dlat/2)**2 + cos(radians(float(lat1))) * cos(radians(float(lat2))) * sin(dlng/2)**2
    return round(R * 2 * atan2(sqrt(a), sqrt(1-a)), 2)


def auto_match(demand_id):
    """
    对指定需求执行自动匹配，生成 SupplyDemandMatch 记录。
    优先按 category_id 匹配，fallback 到 category_name 字符串匹配。
    返回匹配到的供给列表。
    """
    demand = MaterialDemand.query.get(demand_id)
    if not demand:
        return []

    # 查找匹配的供给：同品类 + 上架中 + 库存满足最低收购量
    query = MaterialSupply.query.filter(
        MaterialSupply.is_available == True,
        MaterialSupply.is_deleted == False
    )

    # 优先用 category_id
    if demand.category_id:
        query = query.filter(MaterialSupply.category_id == demand.category_id)
    elif demand.category_name:
        query = query.filter(MaterialSupply.type == demand.category_name)
    else:
        return []

    if demand.min_weight:
        query = query.filter(MaterialSupply.quantity >= demand.min_weight)

    supplies = query.order_by(MaterialSupply.rating.desc()).all()

    # 获取需求方的坐标（从企业信息中获取）
    demand_lat, demand_lng = None, None
    if demand.enterprise_id:
        from models import Enterprise
        ent = Enterprise.query.get(demand.enterprise_id)
        if ent and ent.lat and ent.lng:
            demand_lat, demand_lng = ent.lat, ent.lng

    matches_created = []
    for supply in supplies:
        # 计算地理距离（坐标缺失时跳过）
        dist = haversine_km(
            supply.lat, supply.lng,
            demand_lat, demand_lng
        )

        # 计算匹配分数（含距离因素）
        score = _calc_score(supply, demand, dist)

        # 检查是否已有匹配记录
        existing = SupplyDemandMatch.query.filter_by(
            supply_id=supply.id, demand_id=demand.id
        ).first()
        if existing:
            existing.match_score = score
            existing.distance_km = dist
            matches_created.append(existing)
        else:
            match = SupplyDemandMatch(
                supply_id=supply.id,
                demand_id=demand.id,
                match_score=score,
                match_type='auto',
                status='pending',
                distance_km=dist,
            )
            db.session.add(match)
            matches_created.append(match)

    db.session.commit()
    return matches_created


def _calc_score(supply, demand, distance_km=None):
    """计算供给-需求匹配分数（0-100），含距离因素"""
    score = 50.0  # 基础分（品类已匹配）

    # 价格匹配度（± 25 分）
    if demand.expected_price_min and demand.expected_price_max and supply.price:
        sp = float(supply.price)
        low = float(demand.expected_price_min)
        high = float(demand.expected_price_max)
        if low <= sp <= high:
            score += 25
        elif sp < low:
            score += 15
        else:
            score += 5

    # 数量匹配度（± 15 分）
    if demand.target_weight and supply.quantity:
        ratio = float(supply.quantity) / float(demand.target_weight)
        if ratio >= 1.0:
            score += 15
        elif ratio >= 0.5:
            score += 8

    # 评分加成（± 10 分）
    if supply.rating:
        score += min(float(supply.rating) * 2, 10)

    # 距离因素（± 15 分）：越近越好
    if distance_km is not None:
        if distance_km <= 10:
            score += 15
        elif distance_km <= 50:
            score += 12
        elif distance_km <= 100:
            score += 8
        elif distance_km <= 300:
            score += 3
        # >300km 不加分

    return min(score, 100.0)


def get_matches_for_demand(demand_id):
    """获取某需求的所有匹配记录，含供给详情"""
    matches = SupplyDemandMatch.query.filter_by(demand_id=demand_id)\
                                     .order_by(SupplyDemandMatch.match_score.desc()).all()
    result = []
    for m in matches:
        supply = MaterialSupply.query.get(m.supply_id)
        result.append({
            'match_id': m.id,
            'supply': supply.to_dict() if supply else None,
            'match_score': float(m.match_score) if m.match_score else 0,
            'match_type': m.match_type,
            'status': m.status,
            'created_at': m.created_at.isoformat() if m.created_at else None,
        })
    return result
