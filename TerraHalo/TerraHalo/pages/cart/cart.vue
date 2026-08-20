<template>
  <view class="cart-page">
    <up-navbar title="购物车" bg-color="#1e7e34" title-color="#fff" :auto-back="true" />

    <!-- Tab 切换 -->
    <view class="tabs">
      <text :class="['tab', { active: tab === 'material' }]" @click="tab='material'">原料</text>
      <text :class="['tab', { active: tab === 'product' }]" @click="tab='product'">商品</text>
    </view>

    <view v-if="loading" class="loading-wrap"><text class="loading-text">加载中...</text></view>
    <text v-else-if="error" class="error-msg">{{ error }}</text>

    <!-- 原料购物车 -->
    <template v-if="tab==='material'">
      <view v-if="!materialItems.length && !loading" class="empty">
        <up-empty text="原料购物车空空如也" />
        <up-button type="primary" size="small" @click="goMaterials">去逛逛</up-button>
      </view>
      <view v-else>
        <view class="item" v-for="item in materialItems" :key="'m-'+item.material_id">
          <view class="item-info">
            <text class="item-name">{{ item.type }}</text>
            <text class="item-supplier">{{ item.supplier_name }}</text>
          </view>
          <view class="item-qty">
            <up-icon name="minus-circle" size="20" @click="changeQty(item, -1)" />
            <text class="qty-num">{{ item.quantity }}</text>
            <up-icon name="plus-circle" size="20" color="#28a745" @click="changeQty(item, 1)" />
          </view>
          <text class="item-price">¥{{ (item.price * item.quantity).toFixed(2) }}</text>
          <up-icon name="close" size="16" color="#999" @click="removeItem(item)" />
        </view>
      </view>
    </template>

    <!-- 商品购物车 -->
    <template v-else>
      <view v-if="!productItems.length && !loading" class="empty">
        <up-empty text="商品购物车空空如也" />
        <up-button type="primary" size="small" @click="goShop">去逛逛</up-button>
      </view>
      <view v-else>
        <view class="item" v-for="item in productItems" :key="'p-'+item.product_id">
          <view class="item-info">
            <text class="item-name">{{ item.product_name }}</text>
            <text class="item-supplier">{{ item.specification }}</text>
          </view>
          <view class="item-qty">
            <text class="qty-num">×{{ item.quantity }}</text>
          </view>
          <text class="item-price">¥{{ (item.price * item.quantity).toFixed(2) }}</text>
          <up-icon name="close" size="16" color="#999" @click="removeProduct(item.product_id)" />
        </view>
      </view>
    </template>

    <!-- 底部结算 -->
    <view class="footer" v-if="currentItems.length">
      <text>合计: <text class="total">¥{{ total.toFixed(2) }}</text></text>
      <up-button type="success" size="small" @click="checkout">去结算</up-button>
    </view>
  </view>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { removeFromCart, updateCart, getCart } from '@/api/cart'
import http from '@/api/request'

const tab = ref('material')
const materialItems = ref([])
const productItems = ref([])
const loading = ref(false)
const error = ref(null)

onMounted(() => loadAll())

async function loadAll() {
  loading.value = true
  try {
    const [matData, prodData] = await Promise.all([
      getCart().catch(() => ({ items: [] })),
      http.get('/api/product-cart').catch(() => ({ items: [] })),
    ])
    materialItems.value = matData?.items || []
    productItems.value = prodData?.items || []
  } catch (e) {
    error.value = '加载失败'
  } finally { loading.value = false }
}

const currentItems = computed(() => tab.value === 'material' ? materialItems.value : productItems.value)
const total = computed(() => currentItems.value.reduce((s, i) => s + i.price * i.quantity, 0))

async function changeQty(item, change) {
  await updateCart(item.material_id, change)
  item.quantity += change
  if (item.quantity <= 0) materialItems.value = materialItems.value.filter(x => x.material_id !== item.material_id)
}
async function removeItem(item) {
  await removeFromCart(item.material_id)
  materialItems.value = materialItems.value.filter(x => x.material_id !== item.material_id)
}
async function removeProduct(productId) {
  await http.post('/api/product-cart/remove', { product_id: productId })
  productItems.value = productItems.value.filter(x => x.product_id !== productId)
}
function checkout() {
  const url = tab.value === 'material' ? '/pages/order-create/order-create' : '/pages/order-create/order-create'
  uni.navigateTo({ url })
}
function goShop() { uni.switchTab({ url: '/pages/shop/shop' }) }
function goMaterials() { uni.switchTab({ url: '/pages/materials/materials' }) }
</script>

<style scoped>
.cart-page { min-height:100vh; background:#f5f5f5; }
.tabs { display:flex; background:#fff; margin:10rpx 20rpx; border-radius:12rpx; }
.tab { flex:1; text-align:center; padding:20rpx; font-size:28rpx; color:#666; }
.tab.active { color:#28a745; font-weight:bold; border-bottom:4rpx solid #28a745; }
.empty { display:flex; flex-direction:column; align-items:center; padding-top:150rpx; }
.item { display:flex; align-items:center; background:#fff; padding:20rpx; margin:10rpx 20rpx; border-radius:12rpx; }
.item-info { flex:1; }
.item-name { font-size:28rpx; font-weight:bold; }
.item-supplier { font-size:22rpx; color:#999; }
.item-qty { display:flex; align-items:center; gap:12rpx; margin:0 16rpx; }
.qty-num { font-size:28rpx; width:50rpx; text-align:center; }
.item-price { font-size:28rpx; color:#e53935; font-weight:bold; margin-right:16rpx; }
.footer { display:flex; justify-content:space-between; align-items:center; background:#fff; padding:20rpx; position:fixed; bottom:0; left:0; right:0; box-shadow:0 -2rpx 10rpx rgba(0,0,0,0.05); }
.total { color:#e53935; font-weight:bold; }
.error-msg { text-align:center; color:#dc3545; padding:40rpx; font-size:26rpx; }
</style>
