<template>
  <view class="driver-tasks">
    <view class="tabs">
      <text :class="['tab', { active: tab === 'pending' }]" @click="tab='pending'">待接单</text>
      <text :class="['tab', { active: tab === 'active' }]" @click="tab='active'">进行中</text>
    </view>

    <view v-if="loading" class="loading-wrap"><text class="loading-text">加载中...</text></view>
    <text v-else-if="error" class="error-msg">{{ error }}</text>
    <template v-else>

    <view v-if="tab==='pending'">
      <view v-if="!pendingList.length" class="empty"><up-empty text="暂无待接单任务" /></view>
      <view class="card" v-for="t in pendingList" :key="t.id">
        <text class="task-no">{{ t.task_no }}</text>
        <text class="addr">提: {{ t.pickup_address }}</text>
        <text class="addr">达: {{ t.delivery_address }}</text>
        <text class="cargo" v-if="t.supply">{{ t.supply.type }} {{ t.supply.estimated_weight||t.supply.quantity }}{{ t.supply.weight_unit||'kg' }}</text>
        <up-button type="success" @click="accept(t.id)" :loading="accepting===t.id">接单</up-button>
      </view>
    </view>

    <view v-else>
      <view v-if="!activeList.length" class="empty"><up-empty text="暂无进行中任务" /></view>
      <view class="card active-card" v-for="t in activeList" :key="t.id">
        <text class="task-no">{{ t.task_no }}</text>
        <text class="addr">提: {{ t.pickup_address }}</text>
        <text class="addr">达: {{ t.delivery_address }}</text>
        <up-button type="primary" @click="complete(t.id)" :loading="completing===t.id">确认送达</up-button>
      </view>
    </view>
    </template>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getTaskPool, getActiveTasks, acceptTask, completeTask } from '@/api/driver'

const tab = ref('pending')
const pendingList = ref([])
const activeList = ref([])
const loading = ref(false)
const error = ref(null)
const accepting = ref(null)
const completing = ref(null)

onMounted(() => loadAll())
async function loadAll() {
  loading.value = true
  error.value = null
  try {
    const [pool, active] = await Promise.all([getTaskPool(), getActiveTasks()])
    pendingList.value = pool || []
    activeList.value = active || []
  } catch (e) { error.value = '加载失败' } finally { loading.value = false }
}

async function accept(id) {
  accepting.value = id
  try { await acceptTask(id); uni.showToast({ title: '接单成功' }); loadAll() }
  catch (e) {} finally { accepting.value = null }
}

async function complete(id) {
  completing.value = id
  try { await completeTask(id); uni.showToast({ title: '已送达' }); loadAll() }
  catch (e) {} finally { completing.value = null }
}
</script>

<style scoped>
.driver-tasks { padding:20rpx; }
.tabs { display:flex; background:#fff; border-radius:12rpx; margin-bottom:16rpx; }
.tab { flex:1; text-align:center; padding:20rpx; font-size:28rpx; color:#666; }
.tab.active { color:#28a745; font-weight:bold; border-bottom:4rpx solid #28a745; }
.empty { padding-top:100rpx; }
.card { background:#fff; border-radius:12rpx; padding:24rpx; margin-bottom:16rpx; }
.active-card { border-left:6rpx solid #28a745; }
.task-no { font-size:24rpx; color:#999; }
.addr { font-size:26rpx; color:#333; margin-top:8rpx; }
.cargo { font-size:26rpx; color:#28a745; margin:8rpx 0; }
.error-msg { text-align:center; color:#dc3545; padding:40rpx; font-size:26rpx; }
</style>
