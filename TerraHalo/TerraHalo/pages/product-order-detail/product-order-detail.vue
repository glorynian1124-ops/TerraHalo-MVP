<template>
  <view class="order-detail">
    <up-navbar title="订单详情" bg-color="#1e7e34" title-color="#fff" :auto-back="true" />

    <view v-if="loading" class="loading-wrap"><text class="loading-text">加载中...</text></view>
    <text v-else-if="error" class="error-msg">{{ error }}</text>
    <up-empty v-else-if="!order" text="订单不存在" />
    <template v-else>
      <view class="card">
        <text class="no">订单号: {{ order.order_no }}</text>
        <view class="row"><text>状态</text><text :class="statusClass">{{ statusLabel }}</text></view>
        <view class="row"><text>金额</text><text class="price">¥{{ amount }}</text></view>
        <view class="row"><text>收货地址</text><text>{{ order.receiver_address || '-' }}</text></view>
        <view class="row"><text>创建时间</text><text>{{ (order.created_at||'').slice(0,16) }}</text></view>
      </view>

      <view class="card" v-if="order.items && order.items.length">
        <text class="section-title">商品明细</text>
        <view class="item" v-for="it in order.items" :key="it.id">
          <view>
            <text class="item-name">{{ it.product_name }}</text>
            <text class="item-spec" v-if="it.specification">{{ it.specification }}</text>
          </view>
          <view class="item-right">
            <text>¥{{ it.unit_price }} × {{ it.quantity }}</text>
            <text class="item-amount">¥{{ it.amount }}</text>
          </view>
        </view>
      </view>

      <up-button v-if="order.pay_status === 'unpaid'" type="error" :loading="paying"
                @click="pay" block shape="circle" custom-style="margin:30rpx 20rpx">立即付款</up-button>
    </template>
  </view>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getProductOrderDetail, payProductOrder } from '@/api/product-orders'

const order = ref(null)
const loading = ref(false)
const error = ref(null)
const paying = ref(false)

onMounted(async () => {
  const pages = getCurrentPages()
  const id = pages[pages.length - 1].$page.options.id
  if (!id) { error.value = '缺少订单 ID'; return }
  loading.value = true
  try { order.value = await getProductOrderDetail(id) } catch (e) { error.value = '加载失败' } finally { loading.value = false }
})

const amount = computed(() => {
  if (!order.value) return '0.00'
  return (order.value.payable_amount || order.value.total_amount || 0).toFixed(2)
})
const statusLabel = computed(() => ({ unpaid: '待付款', paid: '已付款', cancelled: '已取消' }[order.value?.pay_status] || order.value?.pay_status || '-'))
const statusClass = computed(() => ({ unpaid: 'warning', paid: 'success', cancelled: 'muted' }[order.value?.pay_status] || ''))

async function pay() {
  paying.value = true
  try {
    await payProductOrder(order.value.id)
    order.value.pay_status = 'paid'
    order.value.order_status = 'paid'
    uni.showToast({ title: '付款成功', icon: 'success' })
  } catch (e) {} finally { paying.value = false }
}
</script>

<style scoped>
.order-detail { min-height:100vh; background:#f5f5f5; }
.card { background:#fff; margin:20rpx; padding:24rpx; border-radius:12rpx; }
.no { font-size:26rpx; color:#666; display:block; margin-bottom:12rpx; }
.row { display:flex; justify-content:space-between; padding:12rpx 0; font-size:28rpx; border-bottom:1rpx solid #f0f0f0; }
.row:last-child { border-bottom:none; }
.price { color:#e53935; font-weight:bold; }
.section-title { font-size:28rpx; font-weight:bold; margin-bottom:12rpx; }
.item { display:flex; justify-content:space-between; padding:16rpx 0; border-bottom:1rpx solid #f0f0f0; }
.item:last-child { border-bottom:none; }
.item-name { font-size:28rpx; }
.item-spec { font-size:24rpx; color:#999; }
.item-right { text-align:right; font-size:26rpx; }
.item-amount { display:block; color:#e53935; font-weight:bold; }
.status { font-size:24rpx; }
.status.warning { color:#fd7e14; }
.status.success { color:#28a745; }
.status.muted { color:#999; }
.error-msg { text-align:center; color:#dc3545; padding:40rpx; font-size:26rpx; }
</style>
