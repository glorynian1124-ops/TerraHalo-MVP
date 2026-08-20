<template>
  <view class="driver-history">
    <text class="title">历史任务</text>
    <view v-if="loading" class="loading-wrap"><text class="loading-text">加载中...</text></view>
    <text v-else-if="error" class="error-msg">{{ error }}</text>
    <view v-else-if="!list.length" class="empty"><up-empty text="暂无历史任务" /></view>
    <view v-else class="card" v-for="t in list" :key="t.id">
      <text class="task-no">{{ t.task_no }}</text>
      <text class="addr">{{ t.pickup_address }} → {{ t.delivery_address }}</text>
      <text class="date">{{ (t.created_at||'').slice(0,10) }}</text>
      <text class="status completed">已完成</text>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getHistoryTasks } from '@/api/driver'

const list = ref([])
const loading = ref(false)
const error = ref(null)
onMounted(async () => {
  loading.value = true
  try { list.value = await getHistoryTasks() || [] } catch (e) { error.value = '加载失败' } finally { loading.value = false }
})
</script>

<style scoped>
.driver-history { padding:20rpx; }
.title { font-size:36rpx; font-weight:bold; margin-bottom:20rpx; }
.empty { padding-top:100rpx; }
.card { background:#fff; border-radius:12rpx; padding:24rpx; margin-bottom:16rpx; }
.task-no { font-size:24rpx; color:#999; }
.addr { font-size:26rpx; margin-top:6rpx; }
.date { font-size:22rpx; color:#bbb; margin-top:6rpx; }
.status.completed { color:#28a745; font-weight:bold; }
.error-msg { text-align:center; color:#dc3545; padding:40rpx; font-size:26rpx; }
</style>
