# 沃土之环 MVP功能清单 + 页面结构图 + 数据库核心表设计

## 一、MVP定位

- 平台名称：沃土之环
- 平台目标：打造农业废弃物资源化利用与商品有机肥交易的数字化服务平台
- MVP阶段建议聚焦两条主线：
  - 原料回收撮合
  - 商品有机肥销售
- 首版建议覆盖 4 类核心角色：
  - 供给方：农户、养殖户、合作社、村集体
  - 采购企业：有机肥生产企业、原料采购方
  - 司机/承运方：负责收运和配送
  - 平台运营后台：负责审核、匹配、调度、结算和内容维护
- MVP建设原则：
  - 先跑通真实交易闭环
  - 先做规则化、轻量化系统
  - 先小范围试点，再逐步扩区域和品类

---

## 二、MVP功能清单

## 2.1 功能优先级划分

- P0：必须上线，保障平台最小可行交易闭环
- P1：增强体验和运营效率，可在首版稳定后补充
- 暂缓：技术复杂度高、对首轮验证不关键的能力

## 2.2 P0功能清单

### 1. 用户与认证

- 手机号登录
- 微信登录
- 角色选择
  - 农户/养殖户
  - 企业
  - 司机
- 个人实名认证
- 企业资质上传与审核
- 司机身份与车辆信息审核
- 地址簿管理

### 2. 原料供给发布

- 发布可回收农业废弃物信息
- 填写原料品类
- 填写预估重量/体积
- 填写存放地点
- 填写可回收时间
- 上传现场图片
- 填写补充属性
  - 含水率区间
  - 杂质说明
  - 是否便于装车
- 查看发布状态
  - 待审核
  - 待匹配
  - 待收运
  - 已完成
  - 已取消

### 3. 企业采购需求

- 企业发布原料采购需求
- 设置需求品类
- 设置质量要求
- 设置收购半径
- 设置目标数量
- 设置价格区间
- 查看待匹配货源
- 选择货源并发起收运
- 查看采购订单状态

### 4. 匹配与调度

- 平台按规则匹配供给与需求
- 运营后台人工确认匹配结果
- 自动或人工生成收运任务
- 派单给司机
- 司机接单
- 到场打卡
- 装货拍照
- 运输状态更新
- 签收确认
- 全流程状态流转记录

### 5. 原料交易与结算

- 记录预估重量与实际重量
- 记录指导价和成交价
- 记录运费
- 记录平台服务费
- 支持线下结算登记
- 支持后台记账
- 生成账单与结算记录

### 6. 商品有机肥商城

- 企业上架商品有机肥
- 商品信息维护
  - 名称
  - 规格
  - 适用作物
  - 价格
  - 库存
  - 配送范围
- 农户/村集体/合作社浏览商品
- 商品下单
- 支持询价
- 支持线下支付登记
- 商品订单状态管理
  - 待支付
  - 待确认
  - 待发货
  - 待收货
  - 已完成

### 7. 后台运营

- 用户审核
- 企业审核
- 品类标准维护
- 原料供给审核
- 商品审核
- 订单管理
- 调度管理
- 结算管理
- 首页数据看板

## 2.3 P1增强功能

- 地图展示供给点与需求点
- 运费自动估算
- 补贴登记与核销
- 评价与投诉
- 站内消息通知
- 数据报表导出
- 区域价格参考
- 常见问题与帮助中心

## 2.4 暂缓功能

- 复杂路径优化算法
- IoT硬件自动采集
- 完整在线支付闭环
- 微服务拆分
- 碳积分与碳交易模块

---

## 三、页面结构图

## 3.1 用户端/小程序

### 首页

- 原料回收入口
- 商品有机肥入口
- 平台公告
- 热门品类
- 帮助中心

### 发布原料

- 选择品类
- 填写数量与时间
- 选择位置
- 上传图片
- 提交审核

### 我的原料单

- 待审核
- 待匹配
- 待收运
- 已完成
- 已取消

### 商品商城

- 商品列表
- 商品详情
- 购物车/询价单
- 下单页

### 我的商品订单

- 待支付
- 待确认
- 待发货
- 待收货
- 已完成

### 我的

- 身份信息
- 地址管理
- 认证中心
- 客服与反馈

## 3.2 企业端

### 工作台

- 今日待处理
- 最新供给信息
- 采购数据摘要

### 原料采购大厅

- 筛选供给
- 查看供给详情
- 发起匹配/收购

### 采购需求管理

- 新建需求
- 需求列表
- 需求状态管理

### 收运任务

- 待派单
- 运输中
- 已签收
- 异常任务

### 商品管理

- 商品列表
- 新增商品
- 库存管理

### 订单管理

- 采购订单
- 商品订单

### 结算中心

- 账单
- 付款登记
- 收款登记

## 3.3 司机端

### 司机首页

- 待接单
- 我的任务
- 历史任务

### 任务详情

- 到场打卡
- 装货拍照
- 重量录入
- 签收确认
- 异常上报

### 我的车辆

- 车辆信息
- 载重信息

## 3.4 平台后台

### 仪表盘

- 区域供给量
- 成交量
- 收运效率
- 商品销量

### 用户管理

- 供给方管理
- 企业管理
- 司机管理
- 资质审核

### 品类标准库

- 原料品类
- 分类分级规则
- 商品分类

### 原料供给管理

- 待审核
- 待匹配
- 异常单

### 采购需求管理

- 需求审核
- 需求匹配

### 调度中心

- 任务派单
- 运输追踪
- 异常处理

### 商品管理

- 商品审核
- 商品上下架

### 订单中心

- 原料订单
- 商品订单
- 售后/争议处理

### 财务中心

- 结算单
- 服务费
- 补贴台账

### 内容中心

- 公告
- 帮助文档
- Banner管理

## 3.5 页面核心流程

### 用户端原料回收路径

- 首页 -> 发布原料 -> 审核 -> 匹配 -> 收运 -> 完成

### 用户端商品购买路径

- 首页 -> 商品列表 -> 商品详情 -> 下单 -> 收货

### 企业端采购路径

- 工作台 -> 采购大厅 -> 匹配供给 -> 发起收运 -> 签收 -> 结算

### 后台运营路径

- 审核 -> 匹配 -> 派单 -> 异常处理 -> 结算 -> 看板

---

## 四、数据库核心表设计

## 4.1 设计原则

- 首版统一使用 bigint 主键
- 所有核心表建议包含以下通用字段：
  - id
  - created_at
  - updated_at
  - is_deleted
- 商品订单与原料订单分开建表
- 图片、附件、签收凭证建议独立子表
- 金额字段建议使用 decimal(10,2) 或更高精度
- 重量字段建议统一基础单位，例如 kg
- 经纬度单独存储，便于地图与距离计算
- 所有关键状态变化都要保留日志记录

## 4.2 用户与组织

### 1. user

| 字段名 | 说明 |
| --- | --- |
| id | 主键 |
| mobile | 手机号 |
| password_hash | 密码摘要 |
| wechat_openid | 小程序标识 |
| role_type | 角色类型 |
| real_name | 真实姓名 |
| status | 用户状态 |
| last_login_at | 最近登录时间 |
| created_at | 创建时间 |
| updated_at | 更新时间 |

### 2. user_profile

| 字段名 | 说明 |
| --- | --- |
| id | 主键 |
| user_id | 用户ID |
| avatar | 头像 |
| gender | 性别 |
| province | 省 |
| city | 市 |
| district | 区/县 |
| detail_address | 详细地址 |
| lat | 纬度 |
| lng | 经度 |
| village_name | 村名 |
| remark | 备注 |

### 3. enterprise

| 字段名 | 说明 |
| --- | --- |
| id | 主键 |
| user_id | 关联用户ID |
| enterprise_name | 企业名称 |
| enterprise_type | 企业类型 |
| license_no | 营业执照号 |
| contact_name | 联系人 |
| contact_mobile | 联系电话 |
| address | 地址 |
| lat | 纬度 |
| lng | 经度 |
| service_radius_km | 服务半径 |
| audit_status | 审核状态 |
| audit_remark | 审核备注 |

### 4. driver

| 字段名 | 说明 |
| --- | --- |
| id | 主键 |
| user_id | 关联用户ID |
| vehicle_type | 车型 |
| vehicle_no | 车牌号 |
| vehicle_capacity_ton | 载重吨位 |
| id_card_no | 身份证号 |
| driving_license_url | 行驶证/驾驶证附件 |
| audit_status | 审核状态 |

## 4.3 基础标准

### 5. material_category

| 字段名 | 说明 |
| --- | --- |
| id | 主键 |
| name | 品类名称 |
| parent_id | 父级分类 |
| code | 分类编码 |
| description | 描述 |
| status | 状态 |
| sort_no | 排序号 |

### 6. material_grade_rule

| 字段名 | 说明 |
| --- | --- |
| id | 主键 |
| category_id | 原料品类ID |
| grade_name | 等级名称 |
| moisture_min | 最低含水率 |
| moisture_max | 最高含水率 |
| impurity_desc | 杂质要求 |
| price_reference_min | 最低参考价 |
| price_reference_max | 最高参考价 |
| transport_note | 收运说明 |
| status | 状态 |

### 7. product_category

| 字段名 | 说明 |
| --- | --- |
| id | 主键 |
| name | 商品分类名称 |
| parent_id | 父级分类 |
| description | 描述 |
| status | 状态 |

## 4.4 原料供给与需求

### 8. material_supply

| 字段名 | 说明 |
| --- | --- |
| id | 主键 |
| supply_no | 供给单编号 |
| publisher_user_id | 发布人ID |
| publisher_type | 发布人类型 |
| category_id | 原料品类ID |
| estimated_weight | 预估重量 |
| weight_unit | 重量单位 |
| estimated_volume | 预估体积 |
| moisture_range | 含水率区间 |
| impurity_desc | 杂质说明 |
| packaging_type | 包装/堆放形式 |
| loadable_flag | 是否便于装车 |
| available_start_time | 可回收开始时间 |
| available_end_time | 可回收结束时间 |
| province | 省 |
| city | 市 |
| district | 区/县 |
| detail_address | 详细地址 |
| lat | 纬度 |
| lng | 经度 |
| status | 供给单状态 |
| audit_status | 审核状态 |
| audit_user_id | 审核人 |
| audit_time | 审核时间 |
| remark | 备注 |

### 9. material_supply_image

| 字段名 | 说明 |
| --- | --- |
| id | 主键 |
| supply_id | 供给单ID |
| image_url | 图片地址 |
| sort_no | 排序号 |

### 10. material_demand

| 字段名 | 说明 |
| --- | --- |
| id | 主键 |
| demand_no | 需求单编号 |
| enterprise_id | 企业ID |
| category_id | 原料品类ID |
| target_weight | 目标数量 |
| min_weight | 最小收购量 |
| quality_requirement | 质量要求 |
| purchase_radius_km | 收购半径 |
| expected_price_min | 最低期望价格 |
| expected_price_max | 最高期望价格 |
| delivery_requirement | 交付要求 |
| expected_start_time | 期望开始时间 |
| expected_end_time | 期望结束时间 |
| status | 需求单状态 |
| remark | 备注 |

## 4.5 匹配与调度

### 11. supply_demand_match

| 字段名 | 说明 |
| --- | --- |
| id | 主键 |
| supply_id | 供给单ID |
| demand_id | 需求单ID |
| match_score | 匹配分数 |
| match_type | 匹配方式 |
| distance_km | 距离 |
| status | 匹配状态 |
| operator_user_id | 操作人 |
| remark | 备注 |

### 12. dispatch_task

| 字段名 | 说明 |
| --- | --- |
| id | 主键 |
| task_no | 调度任务编号 |
| match_id | 匹配记录ID |
| driver_id | 司机ID |
| vehicle_no | 车牌号 |
| pickup_address | 提货地址 |
| pickup_lat | 提货点纬度 |
| pickup_lng | 提货点经度 |
| delivery_address | 送达地址 |
| delivery_lat | 送达点纬度 |
| delivery_lng | 送达点经度 |
| planned_pickup_time | 计划提货时间 |
| actual_pickup_time | 实际提货时间 |
| actual_arrival_time | 实际送达时间 |
| status | 任务状态 |
| route_distance_km | 运输距离 |
| transport_fee | 运费 |
| remark | 备注 |

### 13. dispatch_task_log

| 字段名 | 说明 |
| --- | --- |
| id | 主键 |
| task_id | 调度任务ID |
| status | 状态 |
| operator_user_id | 操作人ID |
| operator_role | 操作角色 |
| content | 操作内容 |
| created_at | 创建时间 |

## 4.6 原料订单与结算

### 14. material_order

| 字段名 | 说明 |
| --- | --- |
| id | 主键 |
| order_no | 订单编号 |
| supply_id | 供给单ID |
| demand_id | 需求单ID |
| enterprise_id | 企业ID |
| seller_user_id | 卖方用户ID |
| driver_id | 司机ID |
| category_id | 原料品类ID |
| estimated_weight | 预估重量 |
| actual_weight | 实际重量 |
| unit_price | 单价 |
| goods_amount | 货款金额 |
| transport_fee | 运费 |
| platform_service_fee | 平台服务费 |
| subsidy_amount | 补贴金额 |
| settlement_amount | 应结算金额 |
| status | 订单状态 |
| completed_at | 完成时间 |
| cancel_reason | 取消原因 |

### 15. material_sign_record

| 字段名 | 说明 |
| --- | --- |
| id | 主键 |
| order_id | 原料订单ID |
| pickup_photo_url | 提货照片 |
| delivery_photo_url | 送达照片 |
| pickup_weight | 提货重量 |
| delivery_weight | 送达重量 |
| sign_user_id | 签收人 |
| sign_time | 签收时间 |
| remark | 备注 |

### 16. settlement_bill

| 字段名 | 说明 |
| --- | --- |
| id | 主键 |
| bill_no | 结算单编号 |
| biz_type | 业务类型 |
| biz_order_id | 关联业务单ID |
| payer_id | 付款方 |
| payee_id | 收款方 |
| amount | 金额 |
| fee_amount | 服务费 |
| subsidy_amount | 补贴金额 |
| settle_status | 结算状态 |
| settle_time | 结算时间 |
| remark | 备注 |

## 4.7 商品有机肥电商

### 17. product

| 字段名 | 说明 |
| --- | --- |
| id | 主键 |
| enterprise_id | 企业ID |
| category_id | 商品分类ID |
| product_name | 商品名称 |
| product_code | 商品编码 |
| specification | 规格 |
| unit | 单位 |
| price | 销售价 |
| market_price | 市场价 |
| stock_qty | 库存 |
| min_order_qty | 最小起订量 |
| delivery_scope | 配送范围 |
| suitable_crops | 适用作物 |
| detail_content | 图文详情 |
| status | 状态 |

### 18. product_image

| 字段名 | 说明 |
| --- | --- |
| id | 主键 |
| product_id | 商品ID |
| image_url | 图片地址 |
| sort_no | 排序号 |

### 19. product_order

| 字段名 | 说明 |
| --- | --- |
| id | 主键 |
| order_no | 订单编号 |
| buyer_user_id | 买家用户ID |
| buyer_type | 买家类型 |
| enterprise_id | 卖家企业ID |
| total_amount | 订单总金额 |
| discount_amount | 优惠金额 |
| freight_amount | 运费 |
| payable_amount | 应付金额 |
| pay_status | 支付状态 |
| order_status | 订单状态 |
| receiver_name | 收货人 |
| receiver_mobile | 收货电话 |
| receiver_address | 收货地址 |
| remark | 备注 |

### 20. product_order_item

| 字段名 | 说明 |
| --- | --- |
| id | 主键 |
| order_id | 订单ID |
| product_id | 商品ID |
| product_name | 商品名称 |
| specification | 规格 |
| unit_price | 单价 |
| quantity | 数量 |
| amount | 小计金额 |

## 4.8 通用能力

### 21. address_book

| 字段名 | 说明 |
| --- | --- |
| id | 主键 |
| user_id | 用户ID |
| contact_name | 联系人 |
| contact_mobile | 联系电话 |
| province | 省 |
| city | 市 |
| district | 区/县 |
| detail_address | 详细地址 |
| lat | 纬度 |
| lng | 经度 |
| is_default | 是否默认地址 |

### 22. message_notice

| 字段名 | 说明 |
| --- | --- |
| id | 主键 |
| user_id | 用户ID |
| biz_type | 业务类型 |
| biz_id | 业务ID |
| title | 标题 |
| content | 内容 |
| read_status | 已读状态 |
| created_at | 创建时间 |

### 23. operation_log

| 字段名 | 说明 |
| --- | --- |
| id | 主键 |
| operator_user_id | 操作人ID |
| biz_type | 业务类型 |
| biz_id | 业务ID |
| action | 操作动作 |
| content | 操作内容 |
| created_at | 创建时间 |

---

## 五、关键状态枚举建议

### 用户状态

- 正常
- 待审核
- 禁用

### 供给单状态

- 待审核
- 待匹配
- 待确认
- 待收运
- 运输中
- 已完成
- 已取消

### 需求单状态

- 待审核
- 匹配中
- 已锁定
- 已完成
- 已关闭

### 调度任务状态

- 待派单
- 待接单
- 已接单
- 已到场
- 运输中
- 已签收
- 异常
- 已完成

### 原料订单状态

- 待确认
- 待收运
- 待签收
- 待结算
- 已完成
- 已取消

### 商品订单状态

- 待支付
- 待确认
- 待发货
- 待收货
- 已完成
- 已取消
- 售后中

---

## 六、推荐开发顺序

### 第一阶段

- 用户/认证
- 供给发布
- 需求发布
- 后台审核

### 第二阶段

- 匹配
- 派单
- 运输状态更新
- 原料订单

### 第三阶段

- 商品上架
- 商品订单
- 基础结算

### 第四阶段

- 数据看板
- 消息通知
- 评价与反馈
- 补贴台账

---

## 七、后续建议产出文档

- PRD功能说明书
- 页面原型说明书
- 状态流转图
- 数据库ER图
- API接口清单
- MySQL建表SQL草案

---

## 八、总结

- 本文档适合作为沃土之环项目 MVP 阶段的产品与技术基础框架
- 如果下一步进入研发阶段，建议优先补齐以下成果：
  - 页面原型图
  - 字段级数据库设计
  - 接口清单
  - 状态流转图
- 如进入路演、比赛或申报材料阶段，可在此基础上再扩展商业模式、试点方案与运营规划
