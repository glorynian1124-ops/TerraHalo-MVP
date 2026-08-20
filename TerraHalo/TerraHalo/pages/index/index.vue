<template>
  <view class="home-page">
    <!-- Hero区 -->
    <view class="hero">
      <text class="hero-eyebrow">绿色农业 · 循环经济</text>
      <text class="hero-title">让每一寸沃土\n生生不息</text>
      <text class="hero-desc">连接农户、企业与司机的农业废弃物资源化利用一站式平台</text>
      <view class="hero-btns">
        <button class="hero-btn-primary" @click="goShop">立即体验</button>
        <text class="hero-btn-link" @click="scrollToIntro">了解更多 →</text>
      </view>
    </view>

    <!-- 快捷入口 -->
    <view class="quick-row">
      <view class="quick-item" @click="goPublish">
        <text class="quick-icon">📦</text>
        <text class="quick-text">发布原料</text>
      </view>
      <view class="quick-item" @click="goShop">
        <text class="quick-icon">🛒</text>
        <text class="quick-text">有机肥商城</text>
      </view>
      <view class="quick-item" @click="goOrders">
        <text class="quick-icon">📋</text>
        <text class="quick-text">我的订单</text>
      </view>
    </view>

    <!-- 核心能力 -->
    <view class="section" id="intro">
      <text class="section-title">平台核心能力</text>
      <text class="section-sub">以循环经济理念驱动农业废弃物资源化</text>
      <view class="capability-grid">
        <view class="cap-card">
          <text class="cap-icon">♻️</text>
          <text class="cap-title">原料回收</text>
          <text class="cap-desc">农户一键发布秸秆、畜禽粪污等废弃物信息，平台智能审核并快速匹配需求方</text>
        </view>
        <view class="cap-card">
          <text class="cap-icon">🚛</text>
          <text class="cap-title">智能调度</text>
          <text class="cap-desc">基于地理位置与运力数据的智能匹配算法，优化收运路线，降低物流成本</text>
        </view>
        <view class="cap-card">
          <text class="cap-icon">🛒</text>
          <text class="cap-title">有机肥商城</text>
          <text class="cap-desc">废弃物资源化加工为高品质有机肥，在线交易直达用户，实现经济价值闭环</text>
        </view>
      </view>
    </view>

    <!-- 平台数据 -->
    <view class="stats-section">
      <view class="stat-item">
        <text class="stat-num">5,000+</text>
        <text class="stat-label">注册农户</text>
      </view>
      <view class="stat-item">
        <text class="stat-num">200+</text>
        <text class="stat-label">合作企业</text>
      </view>
      <view class="stat-item">
        <text class="stat-num">30万吨</text>
        <text class="stat-label">年处理量</text>
      </view>
      <view class="stat-item">
        <text class="stat-num">98%</text>
        <text class="stat-label">匹配成功率</text>
      </view>
    </view>

    <!-- 四步完成循环 -->
    <view class="section">
      <text class="section-title center">四步完成循环</text>
      <text class="section-sub center">从原料发布到资源再生，平台贯穿全过程</text>
      <view class="steps-row">
        <view class="step">
          <view class="step-num">1</view>
          <text class="step-title">发布原料</text>
          <text class="step-desc">农户或企业发布秸秆、粪污等废弃物供应信息</text>
        </view>
        <view class="step">
          <view class="step-num">2</view>
          <text class="step-title">智能匹配</text>
          <text class="step-desc">平台根据需求与位置自动匹配最优处理方案</text>
        </view>
        <view class="step">
          <view class="step-num">3</view>
          <text class="step-title">收运调度</text>
          <text class="step-desc">司机接单并按路线完成废弃物收运任务</text>
        </view>
        <view class="step">
          <view class="step-num">4</view>
          <text class="step-title">资源再生</text>
          <text class="step-desc">废弃物加工为有机肥，返回农田完成循环</text>
        </view>
      </view>
    </view>

    <!-- 推荐原料 -->
    <view class="section">
      <view class="section-header">
        <text class="section-title">推荐原料</text>
        <text class="more-link" @click="goMaterials()">更多 ></text>
      </view>
      <view v-if="loading" class="loading-wrap"><text class="loading-text">加载中...</text></view>
      <text v-else-if="error" class="error-msg">{{ error }}</text>
      <view v-else-if="!materials.length" class="empty-hint"><text>暂无推荐原料</text></view>
      <view class="material-grid" v-else>
        <view class="material-card" v-for="m in materials" :key="m.id" @click="goDetail(m.id)">
          <text class="mat-type">{{ m.type }}</text>
          <text class="mat-location">{{ m.city || m.location }}</text>
          <view class="mat-footer">
            <text class="mat-price">¥{{ m.price }}/吨</text>
            <text class="mat-qty">{{ m.quantity }}吨</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 底部 -->
    <view class="footer">
      <view class="footer-brand">
        <text class="footer-logo">🌱</text>
        <text class="footer-name">沃土之环</text>
      </view>
      <text class="footer-text">绿色农业 · 循环经济</text>
      <text class="footer-copy">© 2026 沃土之环</text>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getMaterials } from '@/api/materials'
import { useUserStore } from '@/store/user'

const userStore = useUserStore()
const materials = ref([])
const loading = ref(false)
const error = ref(null)

onMounted(async () => {
  loading.value = true
  try {
    const data = await getMaterials({ sort_by: 'rating' })
    materials.value = (data || []).slice(0, 6)
  } catch (e) {
    error.value = '加载失败，请检查网络连接'
  } finally { loading.value = false }
})

function goPublish() {
  if (!userStore.isLoggedIn) { uni.navigateTo({ url: '/pages/login/login' }); return }
  uni.navigateTo({ url: '/pages/publish/publish' })
}
function goShop() { uni.switchTab({ url: '/pages/shop/shop' }) }
function goOrders() { uni.switchTab({ url: '/pages/orders/orders' }) }
function goMaterials(type) {
  const url = type ? `/pages/materials/materials?type=${type}` : '/pages/materials/materials'
  uni.navigateTo({ url })
}
function goDetail(id) { uni.navigateTo({ url: `/pages/material-detail/material-detail?id=${id}` }) }
function scrollToIntro() {
  uni.createSelectorQuery().select('#intro').boundingClientRect(rect => {
    uni.pageScrollTo({ scrollTop: rect.top, duration: 300 })
  }).exec()
}
</script>

<style scoped>
.home-page { background: #faf8f2; min-height: 100vh; padding-bottom: 20rpx; }

/* Hero */
.hero {
  background: linear-gradient(135deg, #6B4F10 0%, #2D5A27 60%, #1B3D18 100%);
  padding: 80rpx 40rpx 60rpx; text-align: center;
}
.hero-eyebrow { font-size: 22rpx; color: rgba(255,255,255,0.55); letter-spacing: 4rpx; text-transform: uppercase; }
.hero-title { display: block; font-size: 56rpx; font-weight: 700; color: #fff; line-height: 1.1; margin: 16rpx 0; white-space: pre-line; }
.hero-desc { font-size: 28rpx; color: rgba(255,255,255,0.8); line-height: 1.6; margin-bottom: 32rpx; display: block; }
.hero-btns { display: flex; align-items: center; justify-content: center; gap: 24rpx; }
.hero-btn-primary {
  background: #fff; color: #8B6914; font-size: 30rpx; font-weight: 600;
  padding: 20rpx 48rpx; border-radius: 48rpx; border: none;
}
.hero-btn-link { color: rgba(255,255,255,0.9); font-size: 28rpx; }

/* 快捷入口 */
.quick-row { display: flex; margin: -40rpx 30rpx 30rpx; background: #fff; border-radius: 24rpx; padding: 24rpx; box-shadow: 0 4rpx 20rpx rgba(0,0,0,0.06); }
.quick-item { flex: 1; text-align: center; }
.quick-icon { font-size: 48rpx; }
.quick-text { font-size: 24rpx; color: #6e6456; display: block; margin-top: 8rpx; }

/* Section */
.section { padding: 32rpx 30rpx; }
.section-title { font-size: 34rpx; font-weight: 700; color: #2b2416; display: block; }
.section-title.center { text-align: center; }
.section-sub { font-size: 26rpx; color: #6e6456; margin-top: 8rpx; display: block; }
.section-sub.center { text-align: center; }
.section-header { display: flex; justify-content: space-between; align-items: center; }
.more-link { font-size: 26rpx; color: #8B6914; }

/* 能力卡片 */
.capability-grid { display: flex; flex-direction: column; gap: 20rpx; margin-top: 24rpx; }
.cap-card {
  background: #fff; border: 1px solid #ede6d5; border-radius: 24rpx; padding: 28rpx;
  display: flex; flex-direction: column; gap: 12rpx;
}
.cap-icon { font-size: 44rpx; }
.cap-title { font-size: 30rpx; font-weight: 600; color: #2b2416; }
.cap-desc { font-size: 24rpx; color: #6e6456; line-height: 1.6; }

/* 数据统计 */
.stats-section {
  display: grid; grid-template-columns: 1fr 1fr; gap: 20rpx;
  margin: 0 30rpx 20rpx; background: #f5f1e7; border-radius: 24rpx; padding: 32rpx 24rpx;
}
.stat-item { text-align: center; }
.stat-num { font-size: 40rpx; font-weight: 700; color: #8B6914; display: block; }
.stat-label { font-size: 22rpx; color: #6e6456; margin-top: 4rpx; }

/* 四步流程 */
.steps-row { display: grid; grid-template-columns: 1fr 1fr; gap: 24rpx; margin-top: 24rpx; }
.step { display: flex; flex-direction: column; align-items: center; text-align: center; gap: 10rpx; }
.step-num {
  width: 72rpx; height: 72rpx; border-radius: 36rpx; background: #8B6914;
  color: #fff; font-size: 32rpx; font-weight: 700; display: flex;
  align-items: center; justify-content: center;
}
.step-title { font-size: 28rpx; font-weight: 600; color: #2b2416; }
.step-desc { font-size: 22rpx; color: #6e6456; line-height: 1.5; }

/* 原料卡片 */
.material-grid { display: flex; flex-wrap: wrap; margin-top: 20rpx; }
.material-card {
  width: calc(50% - 12rpx); margin-right: 24rpx; margin-bottom: 20rpx;
  background: #fff; border-radius: 16rpx; padding: 24rpx;
  border: 1px solid #ede6d5;
}
.material-card:nth-child(2n) { margin-right: 0; }
.mat-type { font-size: 28rpx; font-weight: 700; color: #2b2416; }
.mat-location { font-size: 22rpx; color: #a39887; margin-top: 4rpx; display: block; }
.mat-footer { display: flex; justify-content: space-between; margin-top: 16rpx; }
.mat-price { font-size: 26rpx; color: #c0392b; font-weight: 700; }
.mat-qty { font-size: 22rpx; color: #a39887; }

/* 底部 */
.footer {
  background: #2b2416; padding: 40rpx 30rpx; text-align: center; margin-top: 20rpx;
}
.footer-brand { display: flex; align-items: center; justify-content: center; gap: 8rpx; }
.footer-logo { font-size: 36rpx; }
.footer-name { font-size: 30rpx; font-weight: 600; color: #e5e0d8; }
.footer-text { font-size: 24rpx; color: #a39887; display: block; margin-top: 12rpx; }
.footer-copy { font-size: 22rpx; color: #8c8070; display: block; margin-top: 16rpx; }

.error-msg { text-align: center; color: #dc2626; padding: 40rpx; font-size: 26rpx; }
.empty-hint { padding: 40rpx; text-align: center; color: #a39887; font-size: 26rpx; }
</style>