<template>
  <view class="detail-page">
    <!-- 返回按钮 -->
    <view class="back-bar">
      <text class="back-btn" @click="goBack">← 返回</text>
    </view>

    <view v-if="loading" class="loading-wrap"><text class="loading-text">加载中...</text></view>
    <text v-else-if="error" class="error-msg">{{ error }}</text>
    <view v-else class="content">
      <!-- 图片 -->
      <view class="img-area">
        <text class="img-placeholder">🌾</text>
      </view>

      <!-- 信息卡片 -->
      <view class="info-card">
        <view class="info-top">
          <text class="info-title">{{ material.type }}</text>
          <text class="status-badge" :class="material.status === '待收购' ? 'badge-open' : 'badge-transit'">{{ material.status || '待收购' }}</text>
        </view>

        <view class="meta-row">
          <view class="meta-item">
            <text class="meta-label">数量</text>
            <text class="meta-value">{{ material.quantity }}吨</text>
          </view>
          <view class="meta-item">
            <text class="meta-label">单价</text>
            <text class="meta-value price">¥{{ material.price }}/吨</text>
          </view>
          <view class="meta-item">
            <text class="meta-label">总价</text>
            <text class="meta-value price">¥{{ (material.price || 0) * (material.quantity || 0) }}</text>
          </view>
        </view>

        <view class="info-row">
          <text class="row-label">📍 产地</text>
          <text class="row-value">{{ material.city || material.location }}</text>
        </view>
        <view class="info-row">
          <text class="row-label">📋 品类</text>
          <text class="row-value">{{ material.type }}</text>
        </view>
        <view class="info-row">
          <text class="row-label">📝 描述</text>
          <text class="row-value">{{ material.description || '暂无描述' }}</text>
        </view>
        <view class="info-row">
          <text class="row-label">🕐 发布时间</text>
          <text class="row-value">{{ material.time || '刚刚' }}</text>
        </view>
      </view>

      <!-- 操作按钮 -->
      <view class="actions">
        <button class="btn-primary" @click="handleBook">联系卖家</button>
        <button class="btn-outline" @click="handleShare">分享</button>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getMaterialById } from '@/api/materials'

const material = ref({})
const loading = ref(false)
const error = ref(null)

onMounted(async () => {
  const pages = getCurrentPages()
  const id = pages[pages.length - 1].options?.id
  if (!id) { error.value = '缺少参数'; return }
  loading.value = true
  try { material.value = await getMaterialById(id) || {} } catch (e) { error.value = '加载失败' } finally { loading.value = false }
})

function goBack() { uni.navigateBack() }
function handleBook() { uni.showToast({ title: '已发送联系请求', icon: 'success' }) }
function handleShare() { uni.showToast({ title: '分享功能开发中', icon: 'none' }) }
</script>

<style scoped>
.detail-page { background: #faf8f2; min-height: 100vh; padding-bottom: 40rpx; }
.back-bar { padding: 20rpx 30rpx; background: #fff; border-bottom: 1px solid #ede6d5; }
.back-btn { font-size: 28rpx; color: #8B6914; font-weight: 600; }
.img-area {
  width: 100%; height: 480rpx; background: linear-gradient(135deg, #fdf3d6, #ede6d5);
  display: flex; align-items: center; justify-content: center;
}
.img-placeholder { font-size: 120rpx; }
.content { padding: 24rpx; }
.info-card {
  background: #fff; border: 1px solid #ede6d5; border-radius: 24rpx;
  padding: 28rpx; margin-bottom: 24rpx;
}
.info-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24rpx; }
.info-title { font-size: 34rpx; font-weight: 700; color: #2b2416; }
.status-badge { font-size: 22rpx; padding: 6rpx 20rpx; border-radius: 24rpx; }
.badge-open { background: #eef5ec; color: #2D5A27; }
.badge-transit { background: #fdf3d6; color: #7a5c11; }
.meta-row {
  display: flex; justify-content: space-between; padding: 20rpx 0;
  border-top: 1px solid #ede6d5; border-bottom: 1px solid #ede6d5; margin-bottom: 20rpx;
}
.meta-item { text-align: center; flex: 1; }
.meta-label { font-size: 24rpx; color: #a39887; display: block; }
.meta-value { font-size: 28rpx; font-weight: 600; color: #2b2416; display: block; margin-top: 4rpx; }
.meta-value.price { color: #8B6914; }
.info-row {
  display: flex; justify-content: space-between; padding: 16rpx 0;
  border-bottom: 1px solid #f5f1e7;
}
.row-label { font-size: 26rpx; color: #6e6456; }
.row-value { font-size: 26rpx; color: #2b2416; text-align: right; flex: 1; margin-left: 20rpx; }
.actions { display: flex; gap: 20rpx; }
.btn-primary {
  flex: 1; height: 88rpx; border-radius: 44rpx; background: #8B6914;
  color: #fff; font-size: 30rpx; font-weight: 600; border: none;
}
.btn-outline {
  flex: 1; height: 88rpx; border-radius: 44rpx; background: transparent;
  color: #8B6914; font-size: 30rpx; font-weight: 600;
  border: 1px solid #8B6914;
}
.error-msg { text-align: center; color: #dc2626; padding: 80rpx; font-size: 28rpx; }
</style>