-- ============================================================
-- 沃土之环 (TerraHalo) - MySQL 建表脚本 (MVP 核心表)
-- 基于: 01_设计文档/沃土之环_MVP功能清单_页面结构图_数据库核心表设计.md
-- ============================================================

CREATE DATABASE IF NOT EXISTS terrahalo
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

USE terrahalo;

-- ============================================================
-- 1. 用户与组织
-- ============================================================

CREATE TABLE IF NOT EXISTS `user` (
    `id`            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `mobile`        VARCHAR(20)     DEFAULT NULL COMMENT '手机号',
    `password_hash` VARCHAR(255)    NOT NULL COMMENT '密码摘要',
    `wechat_openid` VARCHAR(128)    DEFAULT NULL COMMENT '微信小程序标识',
    `role_type`     VARCHAR(20)     NOT NULL DEFAULT 'farmer' COMMENT '角色: farmer/enterprise/driver/admin',
    `real_name`     VARCHAR(64)     DEFAULT NULL COMMENT '真实姓名',
    `status`        VARCHAR(20)     NOT NULL DEFAULT 'pending' COMMENT 'normal/pending/disabled',
    `last_login_at` DATETIME       DEFAULT NULL,
    `created_at`    DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at`    DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `is_deleted`    TINYINT(1)     NOT NULL DEFAULT 0,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_mobile` (`mobile`),
    UNIQUE KEY `uk_wechat_openid` (`wechat_openid`),
    KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';


CREATE TABLE IF NOT EXISTS `user_profile` (
    `id`             BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `user_id`        BIGINT UNSIGNED NOT NULL,
    `avatar`         VARCHAR(512)   DEFAULT NULL,
    `gender`         TINYINT(1)     DEFAULT 0 COMMENT '0未知/1男/2女',
    `province`       VARCHAR(32)    DEFAULT NULL,
    `city`           VARCHAR(32)    DEFAULT NULL,
    `district`       VARCHAR(32)    DEFAULT NULL,
    `detail_address` VARCHAR(256)   DEFAULT NULL,
    `lat`            DECIMAL(10,6)  DEFAULT NULL,
    `lng`            DECIMAL(10,6)  DEFAULT NULL,
    `village_name`   VARCHAR(64)    DEFAULT NULL,
    `remark`         VARCHAR(512)   DEFAULT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户资料表';


CREATE TABLE IF NOT EXISTS `enterprise` (
    `id`               BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `user_id`          BIGINT UNSIGNED NOT NULL,
    `enterprise_name`  VARCHAR(128)   NOT NULL COMMENT '企业名称',
    `enterprise_type`  VARCHAR(32)    DEFAULT NULL COMMENT '企业类型',
    `license_no`       VARCHAR(64)    DEFAULT NULL COMMENT '营业执照号',
    `contact_name`     VARCHAR(64)    DEFAULT NULL,
    `contact_mobile`   VARCHAR(20)    DEFAULT NULL,
    `address`          VARCHAR(256)   DEFAULT NULL,
    `lat`              DECIMAL(10,6)  DEFAULT NULL,
    `lng`              DECIMAL(10,6)  DEFAULT NULL,
    `service_radius_km` INT           DEFAULT 50 COMMENT '服务半径(km)',
    `audit_status`     VARCHAR(20)    NOT NULL DEFAULT 'pending' COMMENT 'pending/approved/rejected',
    `audit_remark`     VARCHAR(512)   DEFAULT NULL,
    `created_at`       DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at`       DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='企业表';


CREATE TABLE IF NOT EXISTS `driver` (
    `id`                    BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `user_id`               BIGINT UNSIGNED NOT NULL,
    `vehicle_type`          VARCHAR(32)   DEFAULT NULL COMMENT '车型',
    `vehicle_no`            VARCHAR(32)   DEFAULT NULL COMMENT '车牌号',
    `vehicle_capacity_ton`  DECIMAL(6,2)  DEFAULT NULL COMMENT '载重吨位',
    `id_card_no`            VARCHAR(32)   DEFAULT NULL COMMENT '身份证号',
    `driving_license_url`   VARCHAR(512)  DEFAULT NULL COMMENT '行驶证/驾驶证附件',
    `audit_status`          VARCHAR(20)   NOT NULL DEFAULT 'pending',
    `created_at`            DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at`            DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='司机表';


-- ============================================================
-- 2. 基础标准
-- ============================================================

CREATE TABLE IF NOT EXISTS `material_category` (
    `id`          BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `name`        VARCHAR(64)   NOT NULL,
    `parent_id`   BIGINT UNSIGNED DEFAULT 0,
    `code`        VARCHAR(32)   DEFAULT NULL,
    `description` VARCHAR(256)  DEFAULT NULL,
    `status`      VARCHAR(20)   NOT NULL DEFAULT 'active',
    `sort_no`     INT           DEFAULT 0,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='原料品类表';


CREATE TABLE IF NOT EXISTS `material_grade_rule` (
    `id`                  BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `category_id`         BIGINT UNSIGNED NOT NULL,
    `grade_name`          VARCHAR(64)   NOT NULL,
    `moisture_min`        DECIMAL(5,2)  DEFAULT NULL,
    `moisture_max`        DECIMAL(5,2)  DEFAULT NULL,
    `impurity_desc`       VARCHAR(256)  DEFAULT NULL,
    `price_reference_min` DECIMAL(10,2) DEFAULT NULL,
    `price_reference_max` DECIMAL(10,2) DEFAULT NULL,
    `transport_note`      VARCHAR(256)  DEFAULT NULL,
    `status`              VARCHAR(20)   NOT NULL DEFAULT 'active',
    PRIMARY KEY (`id`),
    KEY `idx_category_id` (`category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='原料等级规则表';


CREATE TABLE IF NOT EXISTS `product_category` (
    `id`          BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `name`        VARCHAR(64)   NOT NULL,
    `parent_id`   BIGINT UNSIGNED DEFAULT 0,
    `description` VARCHAR(256)  DEFAULT NULL,
    `status`      VARCHAR(20)   NOT NULL DEFAULT 'active',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品分类表';


-- ============================================================
-- 3. 原料供给与需求
-- ============================================================

CREATE TABLE IF NOT EXISTS `material_supply` (
    `id`                   BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `supply_no`            VARCHAR(32)   NOT NULL COMMENT '供给单编号',
    `publisher_user_id`    BIGINT UNSIGNED NOT NULL,
    `publisher_type`       VARCHAR(20)   DEFAULT 'farmer',
    `category_id`          BIGINT UNSIGNED NOT NULL,
    `estimated_weight`     DECIMAL(10,2) NOT NULL COMMENT '预估重量(kg)',
    `weight_unit`          VARCHAR(8)    DEFAULT 'kg',
    `estimated_volume`     DECIMAL(10,2) DEFAULT NULL,
    `moisture_range`       VARCHAR(32)   DEFAULT NULL,
    `impurity_desc`        VARCHAR(256)  DEFAULT NULL,
    `packaging_type`       VARCHAR(32)   DEFAULT NULL COMMENT '散装/袋装/堆放',
    `loadable_flag`        TINYINT(1)    DEFAULT 1 COMMENT '是否便于装车',
    `available_start_time` DATETIME      DEFAULT NULL,
    `available_end_time`   DATETIME      DEFAULT NULL,
    `province`             VARCHAR(32)   DEFAULT NULL,
    `city`                 VARCHAR(32)   DEFAULT NULL,
    `district`             VARCHAR(32)   DEFAULT NULL,
    `detail_address`       VARCHAR(256)  DEFAULT NULL,
    `lat`                  DECIMAL(10,6) DEFAULT NULL,
    `lng`                  DECIMAL(10,6) DEFAULT NULL,
    `status`               VARCHAR(20)   NOT NULL DEFAULT 'pending_audit' COMMENT 'pending_audit/pending_match/pending_confirm/pending_transport/in_transit/completed/cancelled',
    `audit_status`         VARCHAR(20)   NOT NULL DEFAULT 'pending',
    `audit_user_id`        BIGINT UNSIGNED DEFAULT NULL,
    `audit_time`           DATETIME      DEFAULT NULL,
    `remark`               VARCHAR(512)  DEFAULT NULL,
    `created_at`           DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at`           DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `is_deleted`           TINYINT(1)    NOT NULL DEFAULT 0,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_supply_no` (`supply_no`),
    KEY `idx_publisher` (`publisher_user_id`),
    KEY `idx_category` (`category_id`),
    KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='原料供给单';


CREATE TABLE IF NOT EXISTS `material_supply_image` (
    `id`        BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `supply_id` BIGINT UNSIGNED NOT NULL,
    `image_url` VARCHAR(512)  NOT NULL,
    `sort_no`   INT           DEFAULT 0,
    PRIMARY KEY (`id`),
    KEY `idx_supply_id` (`supply_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='供给单图片';


CREATE TABLE IF NOT EXISTS `material_demand` (
    `id`                    BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `demand_no`             VARCHAR(32)   NOT NULL,
    `enterprise_id`         BIGINT UNSIGNED NOT NULL,
    `category_id`           BIGINT UNSIGNED NOT NULL,
    `target_weight`         DECIMAL(10,2) NOT NULL,
    `min_weight`            DECIMAL(10,2) DEFAULT NULL,
    `quality_requirement`   VARCHAR(256)  DEFAULT NULL,
    `purchase_radius_km`    INT           DEFAULT 50,
    `expected_price_min`    DECIMAL(10,2) DEFAULT NULL,
    `expected_price_max`    DECIMAL(10,2) DEFAULT NULL,
    `delivery_requirement`  VARCHAR(256)  DEFAULT NULL,
    `expected_start_time`   DATETIME      DEFAULT NULL,
    `expected_end_time`     DATETIME      DEFAULT NULL,
    `status`                VARCHAR(20)   NOT NULL DEFAULT 'pending_audit' COMMENT 'pending_audit/matching/locked/completed/closed',
    `remark`                VARCHAR(512)  DEFAULT NULL,
    `created_at`            DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at`            DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `is_deleted`            TINYINT(1)    NOT NULL DEFAULT 0,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_demand_no` (`demand_no`),
    KEY `idx_enterprise` (`enterprise_id`),
    KEY `idx_category` (`category_id`),
    KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='原料需求单';


-- ============================================================
-- 4. 匹配与调度
-- ============================================================

CREATE TABLE IF NOT EXISTS `supply_demand_match` (
    `id`                BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `supply_id`         BIGINT UNSIGNED NOT NULL,
    `demand_id`         BIGINT UNSIGNED NOT NULL,
    `match_score`       DECIMAL(5,2)  DEFAULT NULL,
    `match_type`        VARCHAR(20)   DEFAULT 'auto' COMMENT 'auto/manual',
    `distance_km`       DECIMAL(8,2)  DEFAULT NULL,
    `status`            VARCHAR(20)   NOT NULL DEFAULT 'pending',
    `operator_user_id`  BIGINT UNSIGNED DEFAULT NULL,
    `remark`            VARCHAR(512)  DEFAULT NULL,
    `created_at`        DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at`        DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    KEY `idx_supply` (`supply_id`),
    KEY `idx_demand` (`demand_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='供给需求匹配记录';


CREATE TABLE IF NOT EXISTS `dispatch_task` (
    `id`                   BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `task_no`              VARCHAR(32)   NOT NULL,
    `match_id`             BIGINT UNSIGNED NOT NULL,
    `driver_id`            BIGINT UNSIGNED NOT NULL,
    `vehicle_no`           VARCHAR(32)   DEFAULT NULL,
    `pickup_address`       VARCHAR(256)  NOT NULL,
    `pickup_lat`           DECIMAL(10,6) DEFAULT NULL,
    `pickup_lng`           DECIMAL(10,6) DEFAULT NULL,
    `delivery_address`     VARCHAR(256)  NOT NULL,
    `delivery_lat`         DECIMAL(10,6) DEFAULT NULL,
    `delivery_lng`         DECIMAL(10,6) DEFAULT NULL,
    `planned_pickup_time`  DATETIME      DEFAULT NULL,
    `actual_pickup_time`   DATETIME      DEFAULT NULL,
    `actual_arrival_time`  DATETIME      DEFAULT NULL,
    `status`               VARCHAR(20)   NOT NULL DEFAULT 'pending_assign' COMMENT 'pending_assign/pending_accept/accepted/arrived/in_transit/signed/abnormal/completed',
    `route_distance_km`    DECIMAL(8,2)  DEFAULT NULL,
    `transport_fee`        DECIMAL(10,2) DEFAULT NULL,
    `remark`               VARCHAR(512)  DEFAULT NULL,
    `created_at`           DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at`           DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_task_no` (`task_no`),
    KEY `idx_match` (`match_id`),
    KEY `idx_driver` (`driver_id`),
    KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='调度任务表';


CREATE TABLE IF NOT EXISTS `dispatch_task_log` (
    `id`               BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `task_id`          BIGINT UNSIGNED NOT NULL,
    `status`           VARCHAR(20)   NOT NULL,
    `operator_user_id` BIGINT UNSIGNED NOT NULL,
    `operator_role`    VARCHAR(20)   NOT NULL,
    `content`          VARCHAR(512)  DEFAULT NULL,
    `created_at`       DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    KEY `idx_task_id` (`task_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='调度任务日志';


-- ============================================================
-- 5. 原料订单与结算
-- ============================================================

CREATE TABLE IF NOT EXISTS `material_order` (
    `id`                    BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `order_no`              VARCHAR(32)   NOT NULL,
    `supply_id`             BIGINT UNSIGNED NOT NULL,
    `demand_id`             BIGINT UNSIGNED NOT NULL,
    `enterprise_id`         BIGINT UNSIGNED NOT NULL,
    `seller_user_id`        BIGINT UNSIGNED NOT NULL,
    `driver_id`             BIGINT UNSIGNED DEFAULT NULL,
    `category_id`           BIGINT UNSIGNED NOT NULL,
    `estimated_weight`      DECIMAL(10,2) NOT NULL,
    `actual_weight`         DECIMAL(10,2) DEFAULT NULL,
    `unit_price`            DECIMAL(10,2) DEFAULT NULL,
    `goods_amount`          DECIMAL(10,2) DEFAULT NULL,
    `transport_fee`         DECIMAL(10,2) DEFAULT NULL,
    `platform_service_fee`  DECIMAL(10,2) DEFAULT NULL,
    `subsidy_amount`        DECIMAL(10,2) DEFAULT 0,
    `settlement_amount`     DECIMAL(10,2) DEFAULT NULL,
    `status`                VARCHAR(20)   NOT NULL DEFAULT 'pending_confirm' COMMENT 'pending_confirm/pending_transport/pending_sign/pending_settle/completed/cancelled',
    `completed_at`          DATETIME      DEFAULT NULL,
    `cancel_reason`         VARCHAR(256)  DEFAULT NULL,
    `created_at`            DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at`            DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `is_deleted`            TINYINT(1)    NOT NULL DEFAULT 0,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_order_no` (`order_no`),
    KEY `idx_supply` (`supply_id`),
    KEY `idx_enterprise` (`enterprise_id`),
    KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='原料订单表';


CREATE TABLE IF NOT EXISTS `material_sign_record` (
    `id`                  BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `order_id`            BIGINT UNSIGNED NOT NULL,
    `pickup_photo_url`    VARCHAR(512)  DEFAULT NULL,
    `delivery_photo_url`  VARCHAR(512)  DEFAULT NULL,
    `pickup_weight`       DECIMAL(10,2) DEFAULT NULL,
    `delivery_weight`     DECIMAL(10,2) DEFAULT NULL,
    `sign_user_id`        BIGINT UNSIGNED NOT NULL,
    `sign_time`           DATETIME      DEFAULT NULL,
    `remark`              VARCHAR(256)  DEFAULT NULL,
    PRIMARY KEY (`id`),
    KEY `idx_order_id` (`order_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='签收记录表';


CREATE TABLE IF NOT EXISTS `settlement_bill` (
    `id`             BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `bill_no`        VARCHAR(32)   NOT NULL,
    `biz_type`       VARCHAR(20)   NOT NULL COMMENT 'material_order/product_order',
    `biz_order_id`   BIGINT UNSIGNED NOT NULL,
    `payer_id`       BIGINT UNSIGNED NOT NULL,
    `payee_id`       BIGINT UNSIGNED NOT NULL,
    `amount`         DECIMAL(10,2) NOT NULL,
    `fee_amount`     DECIMAL(10,2) DEFAULT 0,
    `subsidy_amount` DECIMAL(10,2) DEFAULT 0,
    `settle_status`  VARCHAR(20)   NOT NULL DEFAULT 'pending' COMMENT 'pending/settled/cancelled',
    `settle_time`    DATETIME      DEFAULT NULL,
    `remark`         VARCHAR(256)  DEFAULT NULL,
    `created_at`     DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at`     DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_bill_no` (`bill_no`),
    KEY `idx_payer` (`payer_id`),
    KEY `idx_payee` (`payee_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='结算账单表';


-- ============================================================
-- 6. 商品有机肥电商
-- ============================================================

CREATE TABLE IF NOT EXISTS `product` (
    `id`              BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `enterprise_id`   BIGINT UNSIGNED NOT NULL,
    `category_id`     BIGINT UNSIGNED NOT NULL,
    `product_name`    VARCHAR(128)  NOT NULL,
    `product_code`    VARCHAR(32)   DEFAULT NULL,
    `specification`   VARCHAR(64)   DEFAULT NULL,
    `unit`            VARCHAR(16)   DEFAULT 'bag',
    `price`           DECIMAL(10,2) NOT NULL,
    `market_price`    DECIMAL(10,2) DEFAULT NULL,
    `stock_qty`       INT           NOT NULL DEFAULT 0,
    `min_order_qty`   INT           DEFAULT 1,
    `delivery_scope`  VARCHAR(256)  DEFAULT NULL,
    `suitable_crops`  VARCHAR(256)  DEFAULT NULL,
    `detail_content`  TEXT          DEFAULT NULL,
    `status`          VARCHAR(20)   NOT NULL DEFAULT 'pending_audit' COMMENT 'pending_audit/on_shelf/off_shelf',
    `created_at`      DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at`      DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `is_deleted`      TINYINT(1)    NOT NULL DEFAULT 0,
    PRIMARY KEY (`id`),
    KEY `idx_enterprise` (`enterprise_id`),
    KEY `idx_category` (`category_id`),
    KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品表';


CREATE TABLE IF NOT EXISTS `product_image` (
    `id`         BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `product_id` BIGINT UNSIGNED NOT NULL,
    `image_url`  VARCHAR(512)  NOT NULL,
    `sort_no`    INT           DEFAULT 0,
    PRIMARY KEY (`id`),
    KEY `idx_product_id` (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品图片表';


CREATE TABLE IF NOT EXISTS `product_order` (
    `id`                 BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `order_no`           VARCHAR(32)   NOT NULL,
    `buyer_user_id`      BIGINT UNSIGNED NOT NULL,
    `buyer_type`         VARCHAR(20)   DEFAULT 'farmer',
    `enterprise_id`      BIGINT UNSIGNED NOT NULL,
    `total_amount`       DECIMAL(10,2) NOT NULL,
    `discount_amount`    DECIMAL(10,2) DEFAULT 0,
    `freight_amount`     DECIMAL(10,2) DEFAULT 0,
    `payable_amount`     DECIMAL(10,2) NOT NULL,
    `pay_status`         VARCHAR(20)   NOT NULL DEFAULT 'unpaid' COMMENT 'unpaid/paid/refunding/refunded',
    `order_status`       VARCHAR(20)   NOT NULL DEFAULT 'pending' COMMENT 'pending/confirmed/shipped/received/completed/cancelled/after_sale',
    `receiver_name`      VARCHAR(64)   DEFAULT NULL,
    `receiver_mobile`    VARCHAR(20)   DEFAULT NULL,
    `receiver_address`   VARCHAR(256)  DEFAULT NULL,
    `remark`             VARCHAR(512)  DEFAULT NULL,
    `created_at`         DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at`         DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `is_deleted`         TINYINT(1)    NOT NULL DEFAULT 0,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_order_no` (`order_no`),
    KEY `idx_buyer` (`buyer_user_id`),
    KEY `idx_enterprise` (`enterprise_id`),
    KEY `idx_order_status` (`order_status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品订单表';


CREATE TABLE IF NOT EXISTS `product_order_item` (
    `id`            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `order_id`      BIGINT UNSIGNED NOT NULL,
    `product_id`    BIGINT UNSIGNED NOT NULL,
    `product_name`  VARCHAR(128)  NOT NULL,
    `specification` VARCHAR(64)   DEFAULT NULL,
    `unit_price`    DECIMAL(10,2) NOT NULL,
    `quantity`      INT           NOT NULL,
    `amount`        DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (`id`),
    KEY `idx_order_id` (`order_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品订单明细表';


-- ============================================================
-- 7. 通用能力
-- ============================================================

CREATE TABLE IF NOT EXISTS `address_book` (
    `id`             BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `user_id`        BIGINT UNSIGNED NOT NULL,
    `contact_name`   VARCHAR(64)   NOT NULL,
    `contact_mobile` VARCHAR(20)   NOT NULL,
    `province`       VARCHAR(32)   DEFAULT NULL,
    `city`           VARCHAR(32)   DEFAULT NULL,
    `district`       VARCHAR(32)   DEFAULT NULL,
    `detail_address` VARCHAR(256)  NOT NULL,
    `lat`            DECIMAL(10,6) DEFAULT NULL,
    `lng`            DECIMAL(10,6) DEFAULT NULL,
    `is_default`     TINYINT(1)    DEFAULT 0,
    `created_at`     DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    KEY `idx_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='地址簿';


CREATE TABLE IF NOT EXISTS `message_notice` (
    `id`          BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `user_id`     BIGINT UNSIGNED NOT NULL,
    `biz_type`    VARCHAR(20)   DEFAULT NULL,
    `biz_id`      BIGINT UNSIGNED DEFAULT NULL,
    `title`       VARCHAR(128)  NOT NULL,
    `content`     TEXT          DEFAULT NULL,
    `read_status` TINYINT(1)    NOT NULL DEFAULT 0,
    `created_at`  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    KEY `idx_user_read` (`user_id`, `read_status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='消息通知表';


CREATE TABLE IF NOT EXISTS `operation_log` (
    `id`               BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `operator_user_id` BIGINT UNSIGNED NOT NULL,
    `biz_type`         VARCHAR(20)   DEFAULT NULL,
    `biz_id`           BIGINT UNSIGNED DEFAULT NULL,
    `action`           VARCHAR(32)   NOT NULL,
    `content`          VARCHAR(512)  DEFAULT NULL,
    `created_at`       DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    KEY `idx_operator` (`operator_user_id`),
    KEY `idx_biz` (`biz_type`, `biz_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='操作日志表';
