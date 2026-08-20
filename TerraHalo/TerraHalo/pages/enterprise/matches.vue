<template>
  <view class="ent-matches">
    <view class="picker-row">
      <picker :range="demandOptions" range-key="label" @change="onDemandChange">
        <text class="picker-text">{{ selectedLabel || '选择需求' }}</text>
      </picker>
    </view>

    <view v-if="!matches.length" class="empty"><up-empty text="请选择需求查看匹配" /></view>

    <view class="match-card" v-for="m in matches" :key="m.match_id">
      <view class="card-hd">
        <text class="score">{{ m.match_score.toFixed(0) }}分</text>
        <text :class="['badge', m.status==='pending'?'warning':'success']">{{ m.status==='pending'?'待确认':'已确认' }}</text>
      </view>
      <text class="type">{{ m.supply?.type }} | {{ m.supply?.location }}</text>
      <text class="info">库存:{{ m.supply?.quantity }}t | ¥{{ m.supply?.price }}/t</text>
      <up-button v-if="m.status==='pending'" type="success" size="mini" @click="confirm(m.match_id)">确认收购</up-button>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getDemands, getMatches, confirmMatch } from '@/api/enterprise'

const demandOptions = ref([])
const selectedLabel = ref('')
const selectedDemandId = ref(null)
const matches = ref([])
const loading = ref(false)
const error = ref(null)

onMounted(async () => {
  loading.value = true
  try {
    const demands = await getDemands()
    demandOptions.value = (demands || []).filter(d => d.status !== 'closed').map(d => ({ id: d.id, label: `${d.demand_no} - ${d.category_name}` }))
    const pages = getCurrentPages()
    const did = pages[pages.length - 1].$page.options.demand_id
    if (did) { selectedDemandId.value = parseInt(did); await loadMatches() }
  } catch (e) { error.value = '加载失败' } finally { loading.value = false }
})

async function loadMatches() {
  if (!selectedDemandId.value) return
  const data = await getMatches(selectedDemandId.value)
  matches.value = data.matches || []
}

function onDemandChange(e) {
  const item = demandOptions.value[e.detail.value]
  selectedDemandId.value = item.id
  selectedLabel.value = item.label
  loadMatches()
}

async function confirm(matchId) {
  await confirmMatch(matchId)
  uni.showToast({ title: '已确认，收运任务已生成' })
  loadMatches()
}
</script>

<style scoped>
.ent-matches { padding:20rpx; }
.picker-row { background:#fff; padding:20rpx; border-radius:12rpx; margin-bottom:16rpx; }
.picker-text { font-size:28rpx; color:#28a745; }
.empty { padding-top:100rpx; }
.match-card { background:#fff; border-radius:12rpx; padding:24rpx; margin-bottom:16rpx; }
.card-hd { display:flex; justify-content:space-between; }
.score { font-size:36rpx; font-weight:bold; color:#28a745; }
.badge { font-size:22rpx; padding:4rpx 12rpx; border-radius:8rpx; }
.badge.warning { background:#fff3e0; color:#e65100; }
.badge.success { background:#e8f5e9; color:#2e7d32; }
.type { font-size:30rpx; font-weight:bold; margin-top:8rpx; }
.info { font-size:26rpx; color:#666; margin:8rpx 0; }
</style>
