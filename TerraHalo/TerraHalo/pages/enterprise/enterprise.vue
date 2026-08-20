<template>
  <view class="enterprise-page">
    <!-- 头部 -->
    <view class="top-bar">
      <view class="brand">
        <text>🌱</text>
        <text class="brand-name">有机肥厂</text>
      </view>
      <view class="top-right">
        <text class="notify">🔔</text>
        <view class="user-info">
          <view class="user-avatar">厂</view>
          <text class="user-name">张厂长</text>
        </view>
      </view>
    </view>

    <scroll-view scroll-y class="main-content">
      <!-- 欢迎 -->
      <view class="welcome">
        <text class="welcome-title">欢迎回来，有机肥厂</text>
        <text class="welcome-date">2026年6月26日 · 周五</text>
      </view>

      <!-- KPI卡片 -->
      <view class="kpi-row">
        <view class="kpi-card">
          <view class="kpi-top">
            <text class="kpi-label">采购需求</text>
            <text class="kpi-badge badge-green">进行中</text>
          </view>
          <text class="kpi-value">12</text>
        </view>
        <view class="kpi-card">
          <view class="kpi-top">
            <text class="kpi-label">收运任务</text>
            <text class="kpi-badge badge-warm">运输中</text>
          </view>
          <text class="kpi-value">5</text>
        </view>
      </view>
      <view class="kpi-row">
        <view class="kpi-card">
          <text class="kpi-label">上架商品</text>
          <text class="kpi-value">28</text>
        </view>
        <view class="kpi-card">
          <text class="kpi-label">本月交易额</text>
          <text class="kpi-value">¥128,500</text>
        </view>
      </view>

      <!-- 待办事项 -->
      <view class="section">
        <text class="section-title">待办事项</text>
        <view class="todo-list">
          <view class="todo-item" v-for="item in todos" :key="item.label">
            <view class="todo-left">
              <text class="todo-label">{{ item.label }}</text>
              <text class="todo-desc">{{ item.desc }}</text>
            </view>
            <text class="todo-link">去处理</text>
          </view>
        </view>
      </view>

      <!-- 近期收运任务 -->
      <view class="section">
        <text class="section-title">近期收运任务</text>
        <view class="task-table">
          <view class="table-row table-header">
            <text class="col col-id">编号</text>
            <text class="col col-type">原料</text>
            <text class="col col-driver">司机</text>
            <text class="col col-status">状态</text>
          </view>
          <view class="table-row" v-for="t in tasks" :key="t.id">
            <text class="col col-id">{{ t.id }}</text>
            <text class="col col-type">{{ t.type }}</text>
            <text class="col col-driver">{{ t.driver }}</text>
            <text class="col col-status">
              <text class="status-tag" :class="t.status === '已完成' ? 'tag-done' : 'tag-transit'">{{ t.status }}</text>
            </text>
          </view>
        </view>
      </view>

      <!-- 快捷入口 -->
      <view class="section">
        <text class="section-title">快捷入口</text>
        <view class="quick-grid">
          <view class="quick-card" v-for="q in quicks" :key="q.label">
            <view class="quick-icon-box"><text>{{ q.icon }}</text></view>
            <text class="quick-label">{{ q.label }}</text>
            <text class="quick-arrow">→</text>
          </view>
        </view>
      </view>
    </scroll-view>
  </view>
</template>

<script setup>
const todos = [
  { label: '待匹配需求', desc: '3条采购需求待匹配' },
  { label: '待派单任务', desc: '2个收运任务待派单' },
  { label: '待结算订单', desc: '6笔订单待结算' }
]

const tasks = [
  { id: '#TSK-2406', type: '鸡粪', driver: '王师傅', status: '已完成' },
  { id: '#TSK-2407', type: '猪粪', driver: '李师傅', status: '运输中' },
  { id: '#TSK-2408', type: '牛粪', driver: '赵师傅', status: '运输中' },
  { id: '#TSK-2409', type: '秸秆', driver: '陈师傅', status: '已完成' }
]

const quicks = [
  { icon: '➕', label: '发布需求' },
  { icon: '🔍', label: '查看匹配' },
  { icon: '📦', label: '管理商品' }
]
</script>

<style scoped>
.enterprise-page { background: #faf8f2; min-height: 100vh; display: flex; flex-direction: column; }

/* 顶栏 */
.top-bar {
  display: flex; justify-content: space-between; align-items: center;
  padding: 16rpx 24rpx; background: #fff; border-bottom: 1px solid #ede6d5;
}
.brand { display: flex; align-items: center; gap: 8rpx; font-size: 32rpx; }
.brand-name { font-size: 32rpx; font-weight: 600; color: #2b2416; }
.top-right { display: flex; align-items: center; gap: 20rpx; }
.notify { font-size: 36rpx; }
.user-info { display: flex; align-items: center; gap: 8rpx; }
.user-avatar {
  width: 56rpx; height: 56rpx; border-radius: 28rpx; background: #8B6914;
  color: #fff; font-size: 24rpx; font-weight: 600;
  display: flex; align-items: center; justify-content: center;
}
.user-name { font-size: 26rpx; color: #2b2416; }

/* 主内容 */
.main-content { flex: 1; height: 0; padding: 24rpx; }

/* 欢迎 */
.welcome { margin-bottom: 24rpx; }
.welcome-title { font-size: 34rpx; font-weight: 700; color: #2b2416; display: block; }
.welcome-date { font-size: 24rpx; color: #6e6456; margin-top: 4rpx; display: block; }

/* KPI */
.kpi-row { display: flex; gap: 16rpx; margin-bottom: 16rpx; }
.kpi-card {
  flex: 1; background: #fff; border: 1px solid #ede6d5; border-radius: 20rpx;
  padding: 24rpx;
}
.kpi-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12rpx; }
.kpi-label { font-size: 24rpx; color: #6e6456; }
.kpi-badge { font-size: 20rpx; padding: 4rpx 12rpx; border-radius: 24rpx; }
.badge-green { background: #eef5ec; color: #2D5A27; }
.badge-warm { background: #fdf3d6; color: #7a5c11; }
.kpi-value { font-size: 44rpx; font-weight: 700; color: #8B6914; display: block; }

/* Section */
.section { margin-bottom: 28rpx; }
.section-title { font-size: 30rpx; font-weight: 700; color: #2b2416; display: block; margin-bottom: 16rpx; }

/* 待办 */
.todo-list { display: flex; flex-direction: column; gap: 12rpx; }
.todo-item {
  background: #fff; border: 1px solid #ede6d5; border-radius: 20rpx;
  padding: 20rpx 24rpx; display: flex; justify-content: space-between; align-items: center;
}
.todo-label { font-size: 26rpx; font-weight: 500; color: #2b2416; display: block; }
.todo-desc { font-size: 22rpx; color: #a39887; margin-top: 4rpx; display: block; }
.todo-link { font-size: 24rpx; color: #8B6914; font-weight: 600; }

/* 任务表格 */
.task-table { background: #fff; border: 1px solid #ede6d5; border-radius: 20rpx; overflow: hidden; }
.table-row { display: flex; padding: 16rpx 16rpx; border-bottom: 1px solid #ede6d5; }
.table-row:last-child { border-bottom: none; }
.table-header { background: #faf8f2; }
.col { font-size: 24rpx; color: #6e6456; }
.table-header .col { font-weight: 600; }
.col-id { flex: 2; }
.col-type { flex: 1; text-align: center; }
.col-driver { flex: 1; text-align: center; }
.col-status { flex: 1; text-align: center; }
.status-tag { font-size: 20rpx; padding: 4rpx 12rpx; border-radius: 24rpx; }
.tag-done { background: #eef5ec; color: #2D5A27; }
.tag-transit { background: #f5f1e7; color: #5c5448; }

/* 快捷入口 */
.quick-grid { display: flex; gap: 16rpx; }
.quick-card {
  flex: 1; background: #fff; border: 1px solid #ede6d5; border-radius: 20rpx;
  padding: 24rpx; display: flex; align-items: center; justify-content: space-between;
}
.quick-icon-box {
  width: 56rpx; height: 56rpx; border-radius: 16rpx;
  background: #fdf3d6; display: flex; align-items: center; justify-content: center;
  font-size: 30rpx;
}
.quick-label { font-size: 26rpx; font-weight: 600; color: #2b2416; }
.quick-arrow { font-size: 24rpx; color: #a39887; }
</style>