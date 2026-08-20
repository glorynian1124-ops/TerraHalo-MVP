<template>
  <view class="ent-demands">
    <view class="header-row">
      <text class="title">采购需求</text>
      <up-button type="primary" size="small" @click="showForm = true">新建</up-button>
    </view>

    <view v-if="!list.length" class="empty"><up-empty text="暂无需求" /></view>

    <view class="card" v-for="d in list" :key="d.id">
      <view class="card-hd">
        <text class="d-no">{{ d.demand_no }}</text>
        <text :class="['badge', statusClass(d.status)]">{{ statusLabel(d.status) }}</text>
      </view>
      <text class="d-type">{{ d.category_name }} | {{ d.target_weight }}吨</text>
      <text class="d-price" v-if="d.expected_price_min">¥{{ d.expected_price_min }}-{{ d.expected_price_max }}/吨</text>
      <view class="card-ft">
        <up-button size="mini" @click="viewMatches(d.id)">查看匹配</up-button>
        <up-button v-if="d.status!=='closed'" size="mini" type="error" plain @click="closeDemand(d.id)">关闭</up-button>
      </view>
    </view>

    <!-- 新建弹窗 -->
    <up-popup :show="showForm" @close="showForm=false" mode="bottom" round="20">
      <view class="form-popup">
        <text class="form-title">新建采购需求</text>
        <up-input v-model="form.category_name" placeholder="原料品类(如:牛粪)" custom-style="margin-bottom:16rpx" />
        <up-input v-model="form.target_weight" type="number" placeholder="目标数量(吨)" custom-style="margin-bottom:16rpx" />
        <up-input v-model="form.min_weight" type="number" placeholder="最低收购量(吨)" custom-style="margin-bottom:16rpx" />
        <up-input v-model="form.expected_price_min" type="digit" placeholder="最低期望价" />
        <up-input v-model="form.expected_price_max" type="digit" placeholder="最高期望价" custom-style="margin-top:16rpx" />
        <up-button type="primary" :loading="saving" @click="submit" block custom-style="margin-top:30rpx">发布需求</up-button>
      </view>
    </up-popup>
  </view>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { getDemands, createDemand, closeDemand as closeApi } from '@/api/enterprise'

const list = ref([])
const loading = ref(false)
const error = ref(null)
const showForm = ref(false)
const saving = ref(false)
const form = reactive({ category_name: '', target_weight: '', min_weight: '', expected_price_min: '', expected_price_max: '' })

onMounted(async () => {
  loading.value = true
  try { list.value = await getDemands() || [] } catch (e) { error.value = '加载失败' } finally { loading.value = false }
})

async function submit() {
  if (!form.category_name || !form.target_weight) { uni.showToast({ title: '请填写必填项', icon: 'none' }); return }
  saving.value = true
  try { await createDemand(form); showForm.value = false; list.value = await getDemands() || []; uni.showToast({ title: '发布成功' }) }
  catch (e) {} finally { saving.value = false }
}

async function closeDemand(id) {
  await closeApi(id)
  list.value = await getDemands() || []
  uni.showToast({ title: '已关闭' })
}

function viewMatches(id) { uni.navigateTo({ url: `/pages/enterprise/matches?demand_id=${id}` }) }

function statusLabel(s) { return { active: '进行中', matching: '匹配中', matched: '已匹配', closed: '已关闭' }[s] || s }
function statusClass(s) { return { active: 'success', matching: 'info', matched: 'primary', closed: 'secondary' }[s] || '' }
</script>

<style scoped>
.ent-demands { padding:20rpx; }
.header-row { display:flex; justify-content:space-between; align-items:center; margin-bottom:20rpx; }
.title { font-size:36rpx; font-weight:bold; }
.empty { padding-top:150rpx; }
.card { background:#fff; border-radius:12rpx; padding:24rpx; margin-bottom:16rpx; }
.card-hd { display:flex; justify-content:space-between; margin-bottom:8rpx; }
.d-no { font-size:24rpx; color:#999; }
.badge { font-size:22rpx; padding:4rpx 12rpx; border-radius:8rpx; }
.badge.success { background:#e8f5e9; color:#2e7d32; }
.badge.info { background:#e3f2fd; color:#1565c0; }
.badge.primary { background:#e8eaf6; color:#283593; }
.badge.secondary { background:#f5f5f5; color:#666; }
.d-type { font-size:30rpx; font-weight:bold; }
.d-price { font-size:26rpx; color:#e53935; margin-top:6rpx; }
.card-ft { display:flex; gap:16rpx; margin-top:16rpx; }
.form-popup { padding:40rpx 30rpx; }
.form-title { font-size:34rpx; font-weight:bold; text-align:center; display:block; margin-bottom:30rpx; }
</style>
