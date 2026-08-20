<template>
  <view class="shop-page">
    <!-- 顶部Banner -->
    <view class="hero-banner">
      <text class="banner-title">有机肥商城</text>
      <text class="banner-sub">优质有机肥，滋养每一寸土地</text>
    </view>

    <!-- 搜索 -->
    <view class="search-bar">
      <up-search v-model="search" placeholder="搜索有机肥产品..." @search="load" @clear="load" />
    </view>

    <!-- 分类筛选 -->
    <scroll-view scroll-x class="cat-scroll">
      <view class="cat-pill" :class="{ active: cat === '' }" @click="cat = ''; load()">全部</view>
      <view class="cat-pill" :class="{ active: cat === '生物有机肥' }" @click="cat = '生物有机肥'; load()">生物有机肥</view>
      <view class="cat-pill" :class="{ active: cat === '复合微生物肥' }" @click="cat = '复合微生物肥'; load()">复合微生物肥</view>
      <view class="cat-pill" :class="{ active: cat === '土壤调理剂' }" @click="cat = '土壤调理剂'; load()">土壤调理剂</view>
    </scroll-view>

    <!-- 排序 -->
    <view class="sort-row">
      <text class="sort-label">排序：</text>
      <picker mode="selector" :range="sortOptions" @change="onSortChange">
        <text class="sort-value">{{ sortOptions[sortIdx] }}</text>
      </picker>
      <text class="count-text"><text class="bold">{{ list.length }}</text> 件商品</text>
      <text class="cart-entry" @click="goCart">🛒</text>
    </view>

    <!-- 商品列表 -->
    <view v-if="loading" class="loading-wrap"><text class="loading-text">加载中...</text></view>
    <text v-else-if="error" class="error-msg">{{ error }}</text>
    <view v-else-if="!list.length" class="empty"><text>暂无商品</text></view>
    <view v-else class="grid">
      <view class="product-card" v-for="p in list" :key="p.id" @click="goDetail(p.id)">
        <view class="card-img">
          <text class="img-placeholder">🌿</text>
        </view>
        <view class="card-body">
          <text class="p-name">{{ p.product_name }}</text>
          <text class="p-spec">{{ p.specification || p.unit || '-' }}</text>
          <view class="p-footer">
            <text class="p-price">¥{{ p.price }}</text>
            <view class="p-stars">★★★★★</view>
          </view>
          <text class="p-sales" v-if="p.sales">已售 {{ p.sales }}</text>
          <button class="add-cart-btn" @click.stop="addToCart(p)">加入购物车</button>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getProducts } from '@/api/user'

const search = ref('')
const cat = ref('')
const sortIdx = ref(0)
const sortOptions = ['默认排序', '价格从低到高', '价格从高到低', '销量优先', '评分优先']
const list = ref([])
const loading = ref(false)
const error = ref(null)

onMounted(() => load())

async function load() {
  loading.value = true; error.value = null
  const params = {}
  if (search.value) params.search = search.value
  if (cat.value) params.type = cat.value
  try { list.value = await getProducts(params) || [] } catch (e) { list.value = []; error.value = '加载失败' } finally { loading.value = false }
}
function goDetail(id) { uni.navigateTo({ url: `/pages/product-detail/product-detail?id=${id}` }) }
function goCart() { uni.switchTab({ url: '/pages/cart/cart' }) }
function onSortChange(e) { sortIdx.value = e.detail.value }
function addToCart(p) { uni.showToast({ title: '已加入购物车', icon: 'success' }) }
</script>

<style scoped>
.shop-page { background: #faf8f2; min-height: 100vh; padding-bottom: 30rpx; }
.hero-banner {
  background: linear-gradient(135deg, #6B4F10 0%, #2D5A27 60%, #1B3D18 100%);
  padding: 50rpx 40rpx; text-align: center;
}
.banner-title { font-size: 40rpx; font-weight: 700; color: #fff; display: block; }
.banner-sub { font-size: 26rpx; color: rgba(255,255,255,0.75); margin-top: 8rpx; display: block; }
.search-bar { padding: 16rpx 20rpx; background: #fff; }
.cat-scroll { white-space: nowrap; padding: 16rpx 20rpx; background: #fff; border-bottom: 1px solid #ede6d5; }
.cat-pill {
  display: inline-block; padding: 12rpx 28rpx; border-radius: 36rpx;
  font-size: 26rpx; color: #6e6456; margin-right: 16rpx;
  border: 1px solid #ede6d5; background: transparent;
}
.cat-pill.active { background: #8B6914; color: #fff; border-color: #8B6914; }
.sort-row {
  display: flex; align-items: center; gap: 16rpx;
  padding: 16rpx 20rpx; background: #fff; font-size: 26rpx;
}
.sort-label { color: #6e6456; }
.sort-value { color: #2b2416; }
.count-text { color: #6e6456; flex: 1; text-align: right; }
.count-text .bold { font-weight: 700; color: #2b2416; }
.cart-entry { font-size: 36rpx; }
.empty { padding: 150rpx 0; text-align: center; color: #a39887; font-size: 26rpx; }
.grid { display: flex; flex-wrap: wrap; padding: 16rpx; }
.product-card {
  width: calc(50% - 12rpx); margin-right: 24rpx; margin-bottom: 20rpx;
  background: #fff; border-radius: 20rpx; overflow: hidden; border: 1px solid #ede6d5;
}
.product-card:nth-child(2n) { margin-right: 0; }
.card-img {
  width: 100%; height: 280rpx; background: linear-gradient(135deg, #fdf3d6, #f5f1e7);
  display: flex; align-items: center; justify-content: center;
}
.img-placeholder { font-size: 80rpx; }
.card-body { padding: 20rpx; display: flex; flex-direction: column; gap: 6rpx; }
.p-name { font-size: 28rpx; font-weight: 700; color: #2b2416; }
.p-spec { font-size: 22rpx; color: #a39887; }
.p-footer { display: flex; justify-content: space-between; align-items: center; margin-top: 8rpx; }
.p-price { font-size: 34rpx; font-weight: 700; color: #8B6914; }
.p-stars { font-size: 20rpx; color: #e8b830; }
.p-sales { font-size: 20rpx; color: #a39887; }
.add-cart-btn {
  width: 100%; height: 64rpx; border-radius: 20rpx; background: transparent;
  border: 1px solid #ede6d5; color: #2b2416; font-size: 24rpx;
  font-weight: 600; margin-top: 10rpx;
}
.error-msg { text-align: center; color: #dc2626; padding: 40rpx; font-size: 26rpx; }
</style>