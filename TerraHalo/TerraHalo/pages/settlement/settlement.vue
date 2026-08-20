<template>
  <view class="settlement-page">
    <up-navbar title="结算账单" bg-color="#1e7e34" title-color="#fff" :auto-back="true" />
    <view v-if="loading" class="loading-wrap"><text class="loading-text">加载中...</text></view>
    <text v-else-if="error" class="error-msg">{{ error }}</text>
    <up-empty v-else-if="!bills.length" text="暂无结算账单" />
    <view v-else class="bill-card" v-for="b in bills" :key="b.id">
      <text class="bill-no">{{ b.bill_no }}</text>
      <view class="bill-row"><text>类型</text><text>{{ b.biz_type==='material'?'原料':'商品' }}</text></view>
      <view class="bill-row"><text>金额</text><text class="price">¥{{ (b.amount || 0).toFixed(2) }}</text></view>
      <view class="bill-row"><text>服务费</text><text>¥{{ (b.fee_amount || 0).toFixed(2) }}</text></view>
      <view class="bill-row"><text>状态</text><text :class="statusClass(b.settle_status)">{{ statusLabel(b.settle_status) }}</text></view>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import http from '@/api/request'

const bills = ref([])
const loading = ref(false)
const error = ref(null)

onMounted(async () => {
  loading.value = true
  try { bills.value = await http.get('/api/settlements') || [] } catch (e) { error.value = '加载失败' } finally { loading.value = false }
})

function statusLabel(s) { return { pending:'待结算', paid:'已结算', cancelled:'已取消' }[s]||s }
function statusClass(s) { return { pending:'warning', paid:'success', cancelled:'muted' }[s]||'' }
</script>

<style scoped>
.settlement-page { min-height:100vh; background:#f5f5f5; padding:20rpx; }
.loading-wrap { display:flex; justify-content:center; padding:80rpx 0; }
.loading-text { font-size:28rpx; color:#999; }
.bill-card { background:#fff; padding:24rpx; border-radius:12rpx; margin-bottom:16rpx; }
.bill-no { font-size:24rpx; color:#666; display:block; margin-bottom:12rpx; }
.bill-row { display:flex; justify-content:space-between; padding:10rpx 0; font-size:26rpx; border-bottom:1rpx solid #f0f0f0; }
.price { color:#e53935; font-weight:bold; }
.warning { color:#fd7e14; }
.success { color:#28a745; }
.muted { color:#999; }
.error-msg { text-align:center; color:#dc3545; padding:40rpx; font-size:26rpx; }
</style>
