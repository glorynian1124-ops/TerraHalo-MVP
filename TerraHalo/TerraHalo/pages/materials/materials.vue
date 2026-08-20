<template>
  <view class="materials-page">
    <!-- 页头 -->
    <view class="page-header">
      <text class="header-title">原料市场</text>
      <text class="header-sub">浏览全国优质农业废弃物原料供给</text>
    </view>

    <!-- 搜索 -->
    <view class="search-box">
      <text class="search-icon">🔍</text>
      <input class="search-input" v-model="search" placeholder="搜索原料名称、产地或品类..." @confirm="load" />
    </view>

    <!-- 分类筛选 -->
    <scroll-view scroll-x class="cat-scroll">
      <view class="cat-pill" :class="{ active: cat === '' }" @click="cat = ''; load()">全部</view>
      <view class="cat-pill" :class="{ active: cat === '鸡粪' }" @click="cat = '鸡粪'; load()">鸡粪</view>
      <view class="cat-pill" :class="{ active: cat === '牛粪' }" @click="cat = '牛粪'; load()">牛粪</view>
      <view class="cat-pill" :class="{ active: cat === '秸秆' }" @click="cat = '秸秆'; load()">秸秆</view>
      <view class="cat-pill" :class="{ active: cat === '其他' }" @click="cat = '其他'; load()">其他</view>
    </scroll-view>

    <!-- 排序 -->
    <view class="sort-row">
      <text class="sort-label">排序</text>
      <picker mode="selector" :range="sortOptions" @change="onSortChange">
        <text class="sort-value">{{ sortOptions[sortIdx] }} ▼</text>
      </picker>
    </view>

    <!-- 列表 -->
    <view v-if="loading" class="loading-wrap"><text class="loading-text">加载中...</text></view>
    <text v-else-if="error" class="error-msg">{{ error }}</text>
    <view v-else-if="!list.length" class="empty"><text>暂无原料信息</text></view>
    <view v-else class="material-list">
      <view class="material-card" v-for="m in list" :key="m.id" @click="goDetail(m.id)">
        <view class="card-img">
          <text class="img-placeholder">🌾</text>
        </view>
        <view class="card-body">
          <view class="card-top">
            <text class="m-title">{{ m.type }}</text>
            <text class="m-status" :class="m.status === '待收购' ? 'status-open' : 'status-transit'">{{ m.status || '待收购' }}</text>
          </view>
          <view class="m-meta">
            <text>{{ m.quantity }}吨</text>
            <text class="dot">·</text>
            <text>{{ m.city || m.location }}</text>
            <text class="dot">·</text>
            <text class="m-price">¥{{ m.price }}/吨</text>
          </view>
          <view class="card-bottom">
            <text class="m-time">{{ m.time || '刚刚' }}</text>
            <text class="m-detail-link">查看详情 →</text>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getMaterials } from '@/api/materials'

const search = ref('')
const cat = ref('')
const sortIdx = ref(0)
const sortOptions = ['最新发布', '价格从低到高', '价格从高到低', '距离最近']
const list = ref([])
const loading = ref(false)
const error = ref(null)

onMounted(() => load())

async function load() {
  loading.value = true; error.value = null
  const params = {}
  if (search.value) params.search = search.value
  if (cat.value) params.type = cat.value
  try { list.value = await getMaterials(params) || [] } catch (e) { list.value = []; error.value = '加载失败' } finally { loading.value = false }
}
function goDetail(id) { uni.navigateTo({ url: `/pages/material-detail/material-detail?id=${id}` }) }
function onSortChange(e) { sortIdx.value = e.detail.value }
</script>

<style scoped>
.materials-page { background: #faf8f2; min-height: 100vh; padding-bottom: 30rpx; }
.page-header { padding: 32rpx 30rpx 10rpx; }
.header-title { font-size: 38rpx; font-weight: 700; color: #2b2416; display: block; }
.header-sub { font-size: 26rpx; color: #6e6456; margin-top: 6rpx; display: block; }
.search-box {
  display: flex; align-items: center; height: 80rpx; margin: 16rpx 30rpx;
  background: #fff; border: 1px solid #ede6d5; border-radius: 24rpx; padding: 0 24rpx;
}
.search-icon { font-size: 32rpx; margin-right: 12rpx; }
.search-input { flex: 1; font-size: 28rpx; color: #2b2416; }
.cat-scroll { white-space: nowrap; padding: 0 30rpx 16rpx; }
.cat-pill {
  display: inline-block; padding: 12rpx 28rpx; border-radius: 36rpx;
  font-size: 26rpx; color: #6e6456; margin-right: 16rpx;
  border: 1px solid #ede6d5; background: transparent;
}
.cat-pill.active { background: #8B6914; color: #fff; border-color: #8B6914; }
.sort-row {
  display: flex; align-items: center; gap: 12rpx; padding: 8rpx 30rpx 20rpx;
  font-size: 26rpx;
}
.sort-label { color: #6e6456; }
.sort-value { color: #2b2416; }
.empty { padding: 150rpx 0; text-align: center; color: #a39887; font-size: 26rpx; }
.material-list { padding: 0 20rpx; display: flex; flex-direction: column; gap: 20rpx; }
.material-card {
  background: #fff; border: 1px solid #ede6d5; border-radius: 24rpx; overflow: hidden;
}
.card-img {
  width: 100%; height: 320rpx;
  background: linear-gradient(135deg, #fdf3d6, #f5f1e7);
  display: flex; align-items: center; justify-content: center;
}
.img-placeholder { font-size: 80rpx; }
.card-body { padding: 24rpx; display: flex; flex-direction: column; gap: 12rpx; }
.card-top { display: flex; justify-content: space-between; align-items: center; }
.m-title { font-size: 30rpx; font-weight: 700; color: #2b2416; }
.m-status { font-size: 22rpx; padding: 4rpx 16rpx; border-radius: 24rpx; }
.status-open { background: #eef5ec; color: #2D5A27; }
.status-transit { background: #fdf3d6; color: #7a5c11; }
.m-meta { font-size: 24rpx; color: #6e6456; display: flex; gap: 8rpx; align-items: center; }
.m-meta .dot { color: #ede6d5; }
.m-price { color: #8B6914; font-weight: 700; }
.card-bottom { display: flex; justify-content: space-between; align-items: center; padding-top: 16rpx; border-top: 1px solid #ede6d5; }
.m-time { font-size: 22rpx; color: #a39887; }
.m-detail-link { font-size: 24rpx; color: #8B6914; font-weight: 600; }
.error-msg { text-align: center; color: #dc2626; padding: 40rpx; font-size: 26rpx; }
</style>