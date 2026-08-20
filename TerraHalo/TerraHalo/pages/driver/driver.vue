<template>
  <view class="driver-page">
    <!-- 司机身份 -->
    <view class="driver-header">
      <view class="driver-info">
        <view class="avatar">小</view>
        <view class="info-text">
          <text class="driver-name">司机小李</text>
          <text class="driver-vehicle">🚛 苏A12345 · 厢式货车 · 5吨</text>
        </view>
      </view>
      <view class="notify-bell">
        <text class="bell">🔔</text>
        <text class="badge">3</text>
      </view>
    </view>

    <!-- Tab切换 -->
    <view class="tabs">
      <view class="tab" :class="{ active: tab === 'pending' }" @click="tab = 'pending'">待接单 (3)</view>
      <view class="tab" :class="{ active: tab === 'active' }" @click="tab = 'active'">进行中 (1)</view>
      <view class="tab" :class="{ active: tab === 'done' }" @click="tab = 'done'">已完成 (28)</view>
    </view>

    <!-- 待接单 -->
    <view v-if="tab === 'pending'" class="tab-content">
      <view class="task-card" v-for="i in 3" :key="'p'+i">
        <view class="task-top">
          <view class="task-main">
            <text class="task-route">📍 {{ routes[i-1] }}</text>
            <view class="task-meta">
              <text class="task-tag">{{ tags[i-1] }}</text>
              <text>{{ amounts[i-1] }} 吨</text>
              <text class="dot">|</text>
              <text class="task-price">¥{{ prices[i-1] }}</text>
              <text class="dot">|</text>
              <text>⏰ 截止 {{ deadlines[i-1] }}</text>
            </view>
          </view>
          <view class="task-btns">
            <button class="btn-accept">接单</button>
            <button class="btn-reject">拒绝</button>
          </view>
        </view>
      </view>
    </view>

    <!-- 进行中 -->
    <view v-if="tab === 'active'" class="tab-content">
      <view class="task-card active-task">
        <view class="task-top">
          <view class="task-main">
            <text class="task-route">📍 秦淮区 → 雨花台区</text>
            <view class="task-meta">
              <text class="task-tag">餐厨垃圾</text>
              <text>4 吨</text>
              <text class="dot">|</text>
              <text class="task-price">¥320</text>
            </view>
          </view>
          <text class="status-badge badge-progress">进行中</text>
        </view>

        <view class="progress-section">
          <text class="progress-title">任务进度</text>
          <view class="steps">
            <view class="step done">
              <text class="step-dot">✓</text>
              <text class="step-label">已到场</text>
            </view>
            <view class="step-connector done"></view>
            <view class="step current">
              <text class="step-dot">🚛</text>
              <text class="step-label">装货中</text>
            </view>
            <view class="step-connector"></view>
            <view class="step">
              <text class="step-dot">○</text>
              <text class="step-label">运输中</text>
            </view>
            <view class="step-connector"></view>
            <view class="step">
              <text class="step-dot">○</text>
              <text class="step-label">签收</text>
            </view>
          </view>
        </view>

        <view class="action-btns">
          <button class="btn-accept">确认装货</button>
          <button class="btn-outline">确认送达</button>
          <button class="btn-danger">上报异常</button>
        </view>
      </view>
    </view>

    <!-- 已完成 -->
    <view v-if="tab === 'done'" class="tab-content">
      <view class="done-card" v-for="i in 5" :key="'d'+i">
        <view class="done-icon">✅</view>
        <view class="done-info">
          <text class="done-title">{{ doneItems[i-1]?.title }}</text>
          <text class="done-meta">{{ doneItems[i-1]?.date }} · 苏A12345</text>
        </view>
        <text class="done-amount">+¥{{ doneItems[i-1]?.amount }}</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue'

const tab = ref('pending')
const routes = ['建邺区 → 江宁区', '鼓楼区 → 栖霞区', '玄武区 → 浦口区']
const tags = ['餐厨垃圾', '园林垃圾', '生活垃圾']
const amounts = [2, 3, 1.5]
const prices = [180, 240, 150]
const deadlines = ['14:30', '16:00', '17:30']

const doneItems = [
  { title: '江宁区 · 餐厨垃圾 · 2 吨', date: '2026-06-25', amount: 180 },
  { title: '栖霞区 · 园林垃圾 · 3 吨', date: '2026-06-24', amount: 240 },
  { title: '浦口区 · 生活垃圾 · 1.5 吨', date: '2026-06-24', amount: 150 },
  { title: '建邺区 · 餐厨垃圾 · 2.5 吨', date: '2026-06-23', amount: 200 },
  { title: '鼓楼区 · 园林垃圾 · 2 吨', date: '2026-06-22', amount: 180 }
]
</script>

<style scoped>
.driver-page { background: #faf8f2; min-height: 100vh; padding-bottom: 40rpx; }

/* 司机头部 */
.driver-header {
  display: flex; justify-content: space-between; align-items: center;
  padding: 24rpx 30rpx; background: #fff; border-bottom: 1px solid #ede6d5;
}
.driver-info { display: flex; align-items: center; gap: 16rpx; }
.avatar {
  width: 72rpx; height: 72rpx; border-radius: 36rpx; background: #8B6914;
  color: #fff; font-size: 28rpx; font-weight: 600;
  display: flex; align-items: center; justify-content: center;
}
.driver-name { font-size: 30rpx; font-weight: 600; color: #2b2416; display: block; }
.driver-vehicle { font-size: 24rpx; color: #6e6456; display: block; margin-top: 4rpx; }
.notify-bell { position: relative; }
.bell { font-size: 40rpx; }
.badge {
  position: absolute; top: -4rpx; right: -4rpx;
  width: 28rpx; height: 28rpx; border-radius: 14rpx;
  background: #dc2626; color: #fff; font-size: 18rpx;
  display: flex; align-items: center; justify-content: center;
}

/* Tabs */
.tabs { display: flex; padding: 16rpx 20rpx; background: #fff; gap: 12rpx; border-bottom: 1px solid #ede6d5; }
.tab {
  padding: 12rpx 28rpx; border-radius: 36rpx; font-size: 26rpx;
  color: #6e6456; border: 1px solid #ede6d5; background: transparent;
}
.tab.active { background: #8B6914; color: #fff; border-color: #8B6914; font-weight: 600; }

/* 内容 */
.tab-content { padding: 20rpx; display: flex; flex-direction: column; gap: 16rpx; }

/* 任务卡片 */
.task-card {
  background: #fff; border: 1px solid #ede6d5; border-radius: 24rpx; padding: 24rpx;
}
.task-top { display: flex; justify-content: space-between; align-items: flex-start; gap: 16rpx; }
.task-main { flex: 1; min-width: 0; }
.task-route { font-size: 30rpx; font-weight: 600; color: #2b2416; display: block; }
.task-meta { font-size: 24rpx; color: #6e6456; display: flex; flex-wrap: wrap; gap: 8rpx; align-items: center; margin-top: 8rpx; }
.task-tag { background: #f5f1e7; padding: 4rpx 12rpx; border-radius: 10rpx; color: #5c5448; font-size: 22rpx; }
.task-price { color: #8B6914; font-weight: 700; }
.dot { color: #ede6d5; }
.task-btns { display: flex; gap: 12rpx; flex-shrink: 0; }
.btn-accept {
  height: 64rpx; padding: 0 28rpx; border-radius: 32rpx; background: #8B6914;
  color: #fff; font-size: 24rpx; font-weight: 600; border: none;
}
.btn-reject {
  height: 64rpx; padding: 0 20rpx; border-radius: 32rpx;
  background: transparent; color: #a39887; font-size: 24rpx; border: none;
}
.btn-outline {
  height: 64rpx; padding: 0 28rpx; border-radius: 32rpx;
  background: transparent; color: #8B6914; font-size: 24rpx; font-weight: 600;
  border: 1px solid #8B6914;
}
.btn-danger {
  height: 64rpx; padding: 0 28rpx; border-radius: 32rpx;
  background: transparent; color: #dc2626; font-size: 24rpx; border: none;
}

/* 进行中任务 */
.status-badge { font-size: 22rpx; padding: 6rpx 16rpx; border-radius: 24rpx; }
.badge-progress { background: #fffbeb; color: #d97706; }
.progress-section { margin-top: 24rpx; padding-top: 20rpx; border-top: 1px solid #ede6d5; }
.progress-title { font-size: 26rpx; font-weight: 600; color: #6e6456; display: block; margin-bottom: 16rpx; }
.steps { display: flex; align-items: flex-start; justify-content: space-between; }
.step { display: flex; flex-direction: column; align-items: center; gap: 8rpx; flex: 1; min-width: 0; }
.step-dot {
  width: 48rpx; height: 48rpx; border-radius: 24rpx; font-size: 24rpx;
  display: flex; align-items: center; justify-content: center;
}
.step.done .step-dot { background: #2D5A27; color: #fff; }
.step.current .step-dot { background: #8B6914; color: #fff; }
.step .step-dot { background: #f5f1e7; color: #a39887; }
.step-label { font-size: 20rpx; color: #6e6456; white-space: nowrap; }
.step.done .step-label { color: #2D5A27; }
.step.current .step-label { color: #8B6914; font-weight: 600; }
.step-connector { flex: 1; height: 4rpx; margin-top: 24rpx; background: #ede6d5; min-width: 16rpx; }
.step-connector.done { background: #2D5A27; }
.action-btns { display: flex; gap: 12rpx; margin-top: 24rpx; padding-top: 20rpx; border-top: 1px solid #ede6d5; }

/* 已完成 */
.done-card {
  display: flex; align-items: center; gap: 16rpx;
  background: #fff; border: 1px solid #ede6d5; border-radius: 24rpx; padding: 20rpx 24rpx;
}
.done-icon { width: 56rpx; height: 56rpx; border-radius: 28rpx; background: #eef5ec; display: flex; align-items: center; justify-content: center; font-size: 28rpx; }
.done-info { flex: 1; min-width: 0; }
.done-title { font-size: 26rpx; font-weight: 500; color: #2b2416; display: block; }
.done-meta { font-size: 22rpx; color: #a39887; margin-top: 4rpx; display: block; }
.done-amount { font-size: 26rpx; font-weight: 700; color: #2D5A27; white-space: nowrap; }
</style>