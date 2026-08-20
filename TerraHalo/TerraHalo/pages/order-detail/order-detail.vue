<template>
  <view class="order-detail">
    <up-navbar title="订单详情" bg-color="#1e7e34" title-color="#fff" :auto-back="true" />

    <view v-if="loading" class="loading-wrap"><text class="loading-text">加载中...</text></view>
    <text v-else-if="error" class="error-msg">{{ error }}</text>
    <up-empty v-else-if="!order" text="订单不存在" />
    <template v-else>
    <view class="card">
      <text class="no">订单号: {{ order.order_no || '#'+order.id }}</text>
      <view class="row"><text>状态</text><text :class="statusClass">{{ statusLabel }}</text></view>
      <view class="row"><text>金额</text><text class="price">¥{{ amount }}</text></view>
      <view class="row"><text>创建时间</text><text>{{ (order.created_at||'').slice(0,16) }}</text></view>
    </view>

    <!-- 状态流转进度条 -->
    <view class="progress-card">
      <text class="section-title">订单进度</text>
      <view class="progress-bar">
        <template v-for="(s, i) in statusSteps" :key="s.key">
          <view class="step" :class="{ done: stepIdx >= i, current: stepIdx === i }">
            <text class="step-dot">{{ stepIdx >= i ? '✓' : i+1 }}</text>
            <text class="step-label">{{ s.label }}</text>
          </view>
          <view v-if="i < statusSteps.length-1" class="step-line" :class="{ done: stepIdx > i }" />
        </template>
      </view>
    </view>

    <!-- 操作按钮 -->
    <view class="actions" v-if="nextActions.length">
      <up-button v-for="act in nextActions" :key="act.status" :type="act.type||'primary'"
                :loading="acting===act.status" @click="doAction(act.status)" block shape="circle"
                custom-style="margin:16rpx 20rpx">{{ act.label }}</up-button>
    </view>

    <up-button v-if="order && order.status === 'pending_confirm'" type="error" :loading="paying"
              @click="pay" block shape="circle" custom-style="margin:30rpx 20rpx">立即付款</up-button>

    <!-- 订单完成后评价 -->
    <view class="review-section" v-if="order && (order.status==='settled'||order.status==='completed') && !reviewed">
      <text class="section-title">评价</text>
      <view class="stars">
        <text v-for="s in 5" :key="s" class="star" :class="{on: reviewRating>=s}" @click="reviewRating=s">{{ reviewRating>=s ? '★' : '☆' }}</text>
      </view>
      <up-input v-model="reviewContent" placeholder="分享你的体验..." />
      <up-button type="success" size="small" :loading="reviewing" @click="submitReview" custom-style="margin-top:16rpx">提交评价</up-button>
    </view>
    </template>
  </view>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { payOrder, getOrderDetail, updateOrderStatus } from '@/api/orders'
import http from '@/api/request'

const order = ref(null)
const loading = ref(false)
const error = ref(null)
const paying = ref(false)
const acting = ref(null)
const reviewed = ref(false)
const reviewRating = ref(5)
const reviewContent = ref('')
const reviewing = ref(false)

const statusSteps = [
  { key: 'pending_confirm', label: '待确认' },
  { key: 'paid', label: '已付款' },
  { key: 'dispatched', label: '已派单' },
  { key: 'transported', label: '运输中' },
  { key: 'signed', label: '已签收' },
  { key: 'settled', label: '已结算' },
]
const statusLabels = {
  pending_confirm: '待确认', paid: '已付款', dispatched: '已派单',
  transported: '运输中', signed: '已签收', settled: '已结算', cancelled: '已取消',
}
const statusClasses = {
  pending_confirm: 'warning', paid: 'info', dispatched: 'primary',
  transported: 'info', signed: 'success', settled: 'success', cancelled: 'muted',
}

// 允许的手动推进（按角色）
const actionMap = {
  paid: [{ status: 'dispatched', label: '确认发货', type: 'primary' }],
  dispatched: [{ status: 'transported', label: '确认运输', type: 'primary' }],
  transported: [{ status: 'signed', label: '确认签收', type: 'success' }],
  signed: [{ status: 'settled', label: '确认结算', type: 'success' }],
}

onMounted(async () => {
  const pages = getCurrentPages()
  const id = pages[pages.length - 1].$page.options.id
  if (!id) { error.value = '缺少订单 ID'; return }
  loading.value = true
  try { order.value = await getOrderDetail(id) } catch (e) { error.value = '加载失败' } finally { loading.value = false }
})

const amount = computed(() => {
  if (!order.value) return '0.00'
  return (order.value.goods_amount || order.value.total_amount || 0).toFixed(2)
})
const statusLabel = computed(() => statusLabels[order.value?.status] || order.value?.status || '-')
const statusClass = computed(() => statusClasses[order.value?.status] || '')
const stepIdx = computed(() => statusSteps.findIndex(s => s.key === order.value?.status))
const nextActions = computed(() => actionMap[order.value?.status] || [])

async function pay() {
  paying.value = true
  try {
    await payOrder(order.value.id)
    order.value.status = 'paid'
    uni.showToast({ title: '付款成功', icon: 'success' })
  } catch (e) {} finally { paying.value = false }
}

async function doAction(status) {
  acting.value = status
  try {
    await updateOrderStatus(order.value.id, status)
    order.value.status = status
    uni.showToast({ title: '状态已更新', icon: 'success' })
  } catch (e) {} finally { acting.value = null }
}

async function submitReview() {
  if (!reviewRating.value) { uni.showToast({ title: '请选择评分', icon: 'none' }); return }
  reviewing.value = true
  try {
    await http.post('/api/reviews/create', {
      rating: reviewRating.value,
      content: reviewContent.value,
      target_user_id: order.value.seller_user_id,
      order_id: order.value.id,
    })
    reviewed.value = true
    uni.showToast({ title: '评价成功', icon: 'success' })
  } catch (e) {} finally { reviewing.value = false }
}
</script>

<style scoped>
.order-detail { min-height:100vh; background:#f5f5f5; }
.card { background:#fff; margin:20rpx; padding:30rpx; border-radius:12rpx; }
.no { font-size:26rpx; color:#666; margin-bottom:20rpx; display:block; }
.row { display:flex; justify-content:space-between; padding:12rpx 0; font-size:28rpx; border-bottom:1rpx solid #f0f0f0; }
.price { color:#e53935; font-weight:bold; }
.warning { color:#fd7e14; }
.info { color:#17a2b8; }
.primary { color:#007aff; }
.success { color:#28a745; }
.muted { color:#999; }
.progress-card { background:#fff; margin:20rpx; padding:24rpx; border-radius:12rpx; }
.section-title { font-size:28rpx; font-weight:bold; margin-bottom:20rpx; display:block; }
.progress-bar { display:flex; align-items:center; }
.step { display:flex; flex-direction:column; align-items:center; flex:1; }
.step-dot { width:40rpx; height:40rpx; line-height:40rpx; text-align:center; border-radius:50%; background:#eee; color:#999; font-size:22rpx; }
.step.done .step-dot { background:#28a745; color:#fff; }
.step.current .step-dot { background:#007aff; color:#fff; }
.step-label { font-size:20rpx; color:#999; margin-top:6rpx; }
.step.done .step-label, .step.current .step-label { color:#333; font-weight:bold; }
.step-line { flex:1; height:4rpx; background:#eee; margin-bottom:30rpx; }
.step-line.done { background:#28a745; }
.actions { margin-top:10rpx; }
.error-msg { text-align:center; color:#dc3545; padding:40rpx; font-size:26rpx; }
.review-section { background:#fff; margin:20rpx; padding:24rpx; border-radius:12rpx; }
.section-title { font-size:28rpx; font-weight:bold; display:block; margin-bottom:12rpx; }
.stars { display:flex; gap:8rpx; margin-bottom:14rpx; }
.star { font-size:48rpx; color:#ddd; }
.star.on { color:#fd7e14; }
</style>
