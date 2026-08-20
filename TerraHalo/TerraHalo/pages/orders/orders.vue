<template>
  <view class="orders-page">
    <view class="tabs">
      <text v-for="t in tabs" :key="t.key" :class="['tab', { active: activeTab === t.key }]"
            @click="activeTab = t.key">{{ t.label }}</text>
    </view>

    <view v-if="loading" class="loading-wrap"><text class="loading-text">加载中...</text></view>
    <text v-else-if="error" class="error-msg">{{ error }}</text>
    <view v-else-if="!filteredOrders.length" class="empty">
      <up-empty text="暂无订单" />
    </view>

    <view v-else class="order-card" v-for="o in filteredOrders" :key="o._type+'-'+o.id" @click="goDetail(o)">
      <view class="card-hd">
        <text class="order-no">{{ o.order_no || '#'+o.id }}</text>
        <text class="order-type">{{ o._type === 'product' ? '商品' : '原料' }}</text>
        <text :class="['status', statusClass(o._status)]">{{ statusLabel(o._status) }}</text>
      </view>
      <text class="order-amount">¥{{ (o._amount || 0).toFixed(2) }}</text>
      <text class="order-time">{{ (o.created_at||'').slice(0,10) }}</text>
    </view>
  </view>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getOrders } from '@/api/orders'
import { getProductOrders } from '@/api/product-orders'

const tabs = [
  { key: 'all', label: '全部' },
  { key: 'pending', label: '待付款' },
  { key: 'paid', label: '已付款' },
  { key: 'completed', label: '已完成' },
]
const activeTab = ref('all')
const orders = ref([])
const loading = ref(false)
const error = ref(null)

onMounted(async () => {
  loading.value = true
  try {
    const [materialOrders, productOrders] = await Promise.all([
      getOrders().catch(() => []),
      getProductOrders().catch(() => []),
    ])
    // 统一格式：加 type 字段区分来源，统一 status/pay_status
    const merged = [
      ...(materialOrders || []).map(o => ({ ...o, _type: 'material', _status: o.status || 'pending', _amount: o.goods_amount || o.total_amount || 0 })),
      ...(productOrders || []).map(o => ({ ...o, _type: 'product', _status: o.pay_status || 'unpaid', _amount: o.payable_amount || o.total_amount || 0 })),
    ]
    // 按创建时间倒序
    merged.sort((a, b) => new Date(b.created_at||0) - new Date(a.created_at||0))
    orders.value = merged
  } catch (e) {
    orders.value = []
    error.value = '加载失败，请检查网络连接'
  } finally {
    loading.value = false
  }
})

const filteredOrders = computed(() => {
  if (activeTab.value === 'all') return orders.value
  if (activeTab.value === 'pending') return orders.value.filter(o => o._status === 'pending' || o._status === 'unpaid')
  if (activeTab.value === 'paid') return orders.value.filter(o => o._status === 'paid')
  if (activeTab.value === 'completed') return orders.value.filter(o => o._status === 'completed')
  return orders.value
})

function statusLabel(s) {
  return { pending: '待付款', unpaid: '待付款', paid: '已付款', completed: '已完成', cancelled: '已取消' }[s] || s
}
function statusClass(s) {
  return { pending: 'warning', unpaid: 'warning', paid: 'info', completed: 'success', cancelled: 'muted' }[s] || ''
}
function goDetail(o) {
  if (o._type === 'product') {
    uni.navigateTo({ url: `/pages/product-order-detail/product-order-detail?id=${o.id}` })
  } else {
    uni.navigateTo({ url: `/pages/order-detail/order-detail?id=${o.id}` })
  }
}
</script>

<style scoped>
.orders-page { min-height:100vh; background:#f5f5f5; }
.tabs { display:flex; background:#fff; padding:20rpx; gap:10rpx; }
.tab { flex:1; text-align:center; font-size:26rpx; color:#666; padding:10rpx 0; border-radius:20rpx; }
.tab.active { background:#e8f5e9; color:#28a745; font-weight:bold; }
.empty { padding-top:150rpx; }
.order-card { background:#fff; margin:16rpx 20rpx; padding:24rpx; border-radius:12rpx; }
.card-hd { display:flex; justify-content:space-between; }
.order-no { font-size:26rpx; color:#666; }
.order-type { font-size:22rpx; color:#28a745; background:#e8f5e9; padding:2rpx 10rpx; border-radius:8rpx; }
.status { font-size:24rpx; }
.status.warning { color:#fd7e14; }
.status.info { color:#17a2b8; }
.status.success { color:#28a745; }
.status.muted { color:#999; }
.order-amount { font-size:36rpx; font-weight:bold; margin-top:12rpx; }
.order-time { font-size:24rpx; color:#999; margin-top:6rpx; }
.error-msg { text-align:center; color:#dc3545; padding:40rpx; font-size:26rpx; }
</style>
