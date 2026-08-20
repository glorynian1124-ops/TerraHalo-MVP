<template>
  <view class="detail-page">
    <view class="back-bar">
      <text class="back-btn" @click="goBack">← 返回</text>
    </view>

    <view v-if="loading" class="loading-wrap"><text class="loading-text">加载中...</text></view>
    <text v-else-if="error" class="error-msg">{{ error }}</text>
    <view v-else class="content">
      <!-- 图片 -->
      <view class="img-area">
        <text class="img-placeholder">🌿</text>
      </view>

      <!-- 商品信息 -->
      <view class="info-card">
        <text class="product-name">{{ product.product_name }}</text>
        <text class="product-spec">{{ product.specification || product.unit || '-' }}</text>

        <view class="price-row">
          <text class="price">¥{{ product.price }}</text>
          <text class="stock">库存：{{ product.stock_qty || 0 }}{{ product.unit || '袋' }}</text>
        </view>

        <view class="stars-row">
          <text class="stars">★★★★★</text>
          <text class="rating">4.8</text>
          <text class="sales">已售 {{ product.sales || 1286 }}</text>
        </view>

        <view class="desc-section">
          <text class="desc-title">商品详情</text>
          <text class="desc-text">{{ product.description || '高品质有机肥，采用纯天然原料发酵而成，富含有机质和有益微生物，能有效改善土壤结构，提高作物产量和品质。' }}</text>
        </view>
      </view>

      <!-- 操作 -->
      <view class="actions">
        <button class="btn-primary" @click="handleBuy">立即购买</button>
        <button class="btn-cart" @click="handleAddCart">加入购物车</button>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getProductById } from '@/api/user'

const product = ref({})
const loading = ref(false)
const error = ref(null)

onMounted(async () => {
  const pages = getCurrentPages()
  const id = pages[pages.length - 1].options?.id
  if (!id) { error.value = '缺少参数'; return }
  loading.value = true
  try { product.value = await getProductById(id) || {} } catch (e) { error.value = '加载失败' } finally { loading.value = false }
})

function goBack() { uni.navigateBack() }
function handleBuy() { uni.showToast({ title: '下单成功', icon: 'success' }) }
function handleAddCart() { uni.showToast({ title: '已加入购物车', icon: 'success' }) }
</script>

<style scoped>
.detail-page { background: #faf8f2; min-height: 100vh; padding-bottom: 40rpx; }
.back-bar { padding: 20rpx 30rpx; background: #fff; border-bottom: 1px solid #ede6d5; }
.back-btn { font-size: 28rpx; color: #8B6914; font-weight: 600; }
.img-area {
  width: 100%; height: 500rpx; background: linear-gradient(135deg, #fdf3d6, #ede6d5);
  display: flex; align-items: center; justify-content: center;
}
.img-placeholder { font-size: 140rpx; }
.content { padding: 24rpx; }
.info-card {
  background: #fff; border: 1px solid #ede6d5; border-radius: 24rpx;
  padding: 28rpx; margin-bottom: 24rpx;
}
.product-name { font-size: 36rpx; font-weight: 700; color: #2b2416; display: block; }
.product-spec { font-size: 26rpx; color: #a39887; margin-top: 8rpx; display: block; }
.price-row { display: flex; justify-content: space-between; align-items: baseline; margin-top: 20rpx; padding: 20rpx 0; border-top: 1px solid #ede6d5; border-bottom: 1px solid #ede6d5; }
.price { font-size: 44rpx; font-weight: 700; color: #8B6914; }
.stock { font-size: 24rpx; color: #a39887; }
.stars-row { display: flex; align-items: center; gap: 8rpx; margin-top: 16rpx; }
.stars { font-size: 24rpx; color: #e8b830; }
.rating { font-size: 24rpx; color: #8B6914; font-weight: 600; }
.sales { font-size: 24rpx; color: #a39887; }
.desc-section { margin-top: 24rpx; }
.desc-title { font-size: 28rpx; font-weight: 600; color: #2b2416; display: block; margin-bottom: 12rpx; }
.desc-text { font-size: 26rpx; color: #6e6456; line-height: 1.7; }
.actions { display: flex; gap: 20rpx; }
.btn-primary {
  flex: 1; height: 88rpx; border-radius: 44rpx; background: #8B6914;
  color: #fff; font-size: 30rpx; font-weight: 600; border: none;
}
.btn-cart {
  flex: 1; height: 88rpx; border-radius: 44rpx; background: transparent;
  color: #8B6914; font-size: 30rpx; font-weight: 600;
  border: 1px solid #8B6914;
}
.error-msg { text-align: center; color: #dc2626; padding: 80rpx; font-size: 28rpx; }
</style>