<template>
  <view class="order-create">
    <up-navbar title="确认下单" bg-color="#1e7e34" title-color="#fff" :auto-back="true" />

    <view v-if="loading" class="loading-wrap"><text class="loading-text">加载中...</text></view>
    <text v-else-if="error" class="error-msg">{{ error }}</text>
    <up-empty v-else-if="!product" text="商品不存在" />
    <template v-else>
      <view class="section">
        <text class="label">商品信息</text>
        <view class="product-info">
          <text class="p-name">{{ product.product_name }}</text>
          <text class="p-spec">{{ product.specification || product.unit || '-' }}</text>
          <view class="p-row">
            <text class="p-price">¥{{ product.price }}</text>
            <text class="p-stock">库存 {{ product.stock_qty }}</text>
          </view>
        </view>
      </view>

      <view class="section">
        <text class="label">购买数量</text>
        <view class="qty-row">
          <text class="qty-btn" @click="qty > 1 ? qty-- : null">−</text>
          <text class="qty-num">{{ qty }}</text>
          <text class="qty-btn" @click="qty < maxQty ? qty++ : null">+</text>
        </view>
        <text class="hint">起订 {{ product.min_order_qty }}{{ product.unit || '袋' }}，当前库存 {{ product.stock_qty }}</text>
      </view>

      <view class="section">
        <text class="label">收货地址</text>
        <up-input v-model="address" placeholder="请输入收货地址" />
      </view>

      <view class="total-row">
        <text>合计</text>
        <text class="total-price">¥{{ total.toFixed(2) }}</text>
      </view>

      <up-button type="success" :loading="submitting" @click="submit" block shape="circle"
                custom-style="margin:40rpx 20rpx">立即下单</up-button>
    </template>
  </view>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getProductDetail } from '@/api/user'
import { createProductOrder } from '@/api/product-orders'
import { useUserStore } from '@/store/user'

const userStore = useUserStore()
const product = ref(null)
const loading = ref(false)
const error = ref(null)
const qty = ref(1)
const address = ref('')
const submitting = ref(false)

const maxQty = computed(() => product.value?.stock_qty || 1)

onMounted(async () => {
  const pages = getCurrentPages()
  const id = pages[pages.length - 1].$page.options.id
  if (!id) { error.value = '缺少商品 ID'; return }

  loading.value = true
  try {
    product.value = await getProductDetail(id)
    if (!product.value) { error.value = '商品不存在或已下架'; return }
    qty.value = product.value.min_order_qty || 1
    if (userStore.currentUser) address.value = userStore.currentUser.address || ''
  } catch (e) { error.value = '加载失败' } finally { loading.value = false }
})

const total = computed(() => {
  if (!product.value) return 0
  return (parseFloat(product.value.price) || 0) * qty.value
})

async function submit() {
  if (!address.value) { uni.showToast({ title: '请输入收货地址', icon: 'none' }); return }
  if (qty.value < (product.value.min_order_qty || 1)) {
    uni.showToast({ title: `起订 ${product.value.min_order_qty}${product.value.unit||'袋'}`, icon: 'none' })
    return
  }
  submitting.value = true
  try {
    const res = await createProductOrder({
      product_id: product.value.id,
      quantity: qty.value,
      address: address.value,
    })
    uni.showToast({ title: '下单成功', icon: 'success' })
    setTimeout(() => {
      uni.redirectTo({ url: `/pages/product-order-detail/product-order-detail?id=${res.order_id}` })
    }, 800)
  } catch (e) {} finally { submitting.value = false }
}
</script>

<style scoped>
.order-create { min-height:100vh; background:#f5f5f5; padding-bottom:40rpx; }
.section { background:#fff; margin:20rpx; padding:24rpx; border-radius:12rpx; }
.label { font-size:28rpx; font-weight:bold; display:block; margin-bottom:12rpx; }
.product-info { padding:10rpx 0; }
.p-name { font-size:32rpx; font-weight:bold; display:block; }
.p-spec { font-size:24rpx; color:#999; margin-top:4rpx; }
.p-row { display:flex; justify-content:space-between; margin-top:12rpx; }
.p-price { font-size:30rpx; color:#e53935; font-weight:bold; }
.p-stock { font-size:24rpx; color:#999; }
.qty-row { display:flex; align-items:center; gap:20rpx; }
.qty-btn { width:60rpx; height:60rpx; line-height:60rpx; text-align:center; background:#e8f5e9; border-radius:10rpx; font-size:36rpx; font-weight:bold; color:#28a745; }
.qty-num { font-size:36rpx; font-weight:bold; min-width:60rpx; text-align:center; }
.hint { font-size:22rpx; color:#bbb; margin-top:8rpx; }
.total-row { display:flex; justify-content:space-between; padding:24rpx; background:#fff; margin:20rpx; border-radius:12rpx; font-size:32rpx; font-weight:bold; }
.total-price { color:#e53935; }
.error-msg { text-align:center; color:#dc3545; padding:40rpx; font-size:26rpx; }
</style>
