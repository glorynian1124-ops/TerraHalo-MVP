<template>
  <view class="order-create">
    <up-navbar title="确认下单" bg-color="#1e7e34" title-color="#fff" :auto-back="true" />

    <view v-if="fetchLoading" class="loading-wrap"><text class="loading-text">加载中...</text></view>
    <text v-else-if="fetchError" class="error-msg">{{ fetchError }}</text>
    <up-empty v-else-if="!items.length" text="购物车为空" />
    <template v-else>
    <view class="section">
      <text class="label">收货地址</text>
      <up-input v-model="address" placeholder="请输入收货地址" />
    </view>

    <view class="section">
      <text class="label">订单商品</text>
      <view class="item" v-for="(item, i) in items" :key="i">
        <text>{{ item.type }} × {{ item.quantity }}吨</text>
        <text class="price">¥{{ (item.price * item.quantity).toFixed(2) }}</text>
      </view>
      <view class="total-row">
        <text>合计</text>
        <text class="total-price">¥{{ total.toFixed(2) }}</text>
      </view>
    </view>

    <up-button type="success" :loading="loading" @click="submit" block shape="circle"
              custom-style="margin:40rpx 20rpx">提交订单</up-button>
    </template>
  </view>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { createOrderFromCart } from '@/api/orders'
import { getCart } from '@/api/cart'
import { useUserStore } from '@/store/user'

const userStore = useUserStore()
const items = ref([])
const address = ref('')
const loading = ref(false)
const fetchLoading = ref(false)
const fetchError = ref(null)

onMounted(async () => {
  fetchLoading.value = true
  try {
    const data = await getCart()
    items.value = data?.items || []
  } catch (e) { items.value = []; fetchError.value = '加载购物车失败' } finally { fetchLoading.value = false }
  if (userStore.currentUser) address.value = userStore.currentUser.address || ''
})

const total = computed(() => items.value.reduce((s, i) => s + i.price * i.quantity, 0))

async function submit() {
  if (!address.value) { uni.showToast({ title: '请输入收货地址', icon: 'none' }); return }
  loading.value = true
  try {
    await createOrderFromCart(address.value)
    uni.showToast({ title: '下单成功', icon: 'success' })
    setTimeout(() => uni.switchTab({ url: '/pages/orders/orders' }), 1000)
  } catch (e) {} finally { loading.value = false }
}
</script>

<style scoped>
.order-create { min-height:100vh; background:#f5f5f5; }
.section { background:#fff; margin:20rpx; padding:24rpx; border-radius:12rpx; }
.label { font-size:28rpx; font-weight:bold; display:block; margin-bottom:12rpx; }
.item { display:flex; justify-content:space-between; padding:12rpx 0; font-size:28rpx; }
.price { color:#e53935; }
.total-row { display:flex; justify-content:space-between; padding-top:16rpx; border-top:1rpx solid #eee; margin-top:8rpx; font-size:32rpx; font-weight:bold; }
.total-price { color:#e53935; }
.error-msg { text-align:center; color:#dc3545; padding:40rpx; font-size:26rpx; }
</style>
