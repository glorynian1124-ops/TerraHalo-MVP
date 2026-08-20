<template>
  <view class="ent-dashboard">
    <view class="header">
      <text class="title">企业工作台</text>
      <text class="sub">华东有机肥有限公司</text>
    </view>
    <view v-if="loading" class="loading-wrap"><text class="loading-text">加载中...</text></view>
    <text v-else-if="error" class="error-msg">{{ error }}</text>
    <template v-else>
    <view class="stats">
      <view class="stat" @click="goPage('/pages/enterprise/demands')">
        <text class="num">{{ stats.demand_count }}</text><text class="label">采购需求</text>
      </view>
      <view class="stat" @click="goPage('/pages/enterprise/matches')">
        <text class="num">{{ stats.active_demand_count }}</text><text class="label">进行中</text>
      </view>
      <view class="stat">
        <text class="num">{{ stats.task_count }}</text><text class="label">收运任务</text>
      </view>
      <view class="stat" @click="goPage('/pages/enterprise/products')">
        <text class="num">{{ stats.product_count }}</text><text class="label">上架商品</text>
      </view>
    </view>
    <view class="quick">
      <up-button type="primary" @click="goPage('/pages/enterprise/demands')">管理采购需求</up-button>
      <up-button type="success" @click="goPage('/pages/enterprise/matches')" custom-style="margin-top:16rpx">查看匹配结果</up-button>
    </view>
    </template>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getDemands, getProducts, getTasks } from '@/api/enterprise'

const stats = ref({ demand_count: 0, active_demand_count: 0, task_count: 0, product_count: 0 })
const loading = ref(false)
const error = ref(null)

onMounted(async () => {
  loading.value = true
  try {
    const [demands, products, tasks] = await Promise.all([
      getDemands(),
      getProducts(),
      getTasks().catch(() => []),
    ])
    stats.value.demand_count = (demands || []).length
    stats.value.active_demand_count = (demands || []).filter(d => d.status !== 'closed').length
    stats.value.task_count = (tasks || []).length
    stats.value.product_count = (products || []).length
  } catch (e) { error.value = '加载失败' } finally { loading.value = false }
})

function goPage(url) { uni.navigateTo({ url }) }
</script>

<style scoped>
.ent-dashboard { min-height:100vh; background:#f5f5f5; }
.header { background:linear-gradient(135deg,#155724,#1e7e34); padding:50rpx 30rpx; color:#fff; }
.title { font-size:40rpx; font-weight:bold; }
.sub { font-size:24rpx; opacity:0.8; margin-top:8rpx; display:block; }
.stats { display:flex; flex-wrap:wrap; margin:20rpx; gap:16rpx; }
.stat { flex:1; min-width:calc(50% - 8rpx); background:#fff; border-radius:12rpx; padding:30rpx; text-align:center; }
.num { font-size:44rpx; font-weight:bold; color:#28a745; display:block; }
.label { font-size:24rpx; color:#999; margin-top:6rpx; }
.quick { margin:20rpx; }
.error-msg { text-align:center; color:#dc3545; padding:40rpx; font-size:26rpx; }
</style>
