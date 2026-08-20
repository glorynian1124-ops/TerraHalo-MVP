<template>
  <view class="ent-products">
    <view class="header-row">
      <text class="title">商品管理</text>
      <up-button type="success" size="small" @click="showForm = true">上架</up-button>
    </view>

    <view v-if="!list.length" class="empty"><up-empty text="暂无商品" /></view>

    <view class="grid">
      <view class="p-card" v-for="p in list" :key="p.id">
        <text class="p-name">{{ p.product_name }}</text>
        <text class="p-spec">{{ p.specification || '-' }}</text>
        <text class="p-price">¥{{ p.price }}</text>
        <text class="p-stock">库存:{{ p.stock_qty }}</text>
        <text :class="['badge', p.status==='on_shelf'?'success':'secondary']">
          {{ p.status==='on_shelf'?'在售':'下架' }}
        </text>
        <up-button size="mini" @click="toggle(p)">{{ p.status==='on_shelf'?'下架':'上架' }}</up-button>
      </view>
    </view>

    <up-popup :show="showForm" @close="showForm=false" mode="bottom" round="20">
      <view class="form-popup">
        <text class="form-title">上架商品</text>
        <up-input v-model="form.product_name" placeholder="商品名称" />
        <up-input v-model="form.specification" placeholder="规格(如:40kg/袋)" custom-style="margin-top:16rpx" />
        <up-input v-model="form.price" type="digit" placeholder="单价(元)" custom-style="margin-top:16rpx" />
        <up-input v-model="form.stock_qty" type="number" placeholder="库存" custom-style="margin-top:16rpx" />
        <up-button type="success" :loading="saving" @click="submit" block custom-style="margin-top:30rpx">上架</up-button>
      </view>
    </up-popup>
  </view>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { getProducts, createProduct, toggleProduct } from '@/api/enterprise'

const list = ref([])
const loading = ref(false)
const error = ref(null)
const showForm = ref(false)
const saving = ref(false)
const form = reactive({ product_name: '', specification: '', price: '', stock_qty: '' })

onMounted(async () => {
  loading.value = true
  try { list.value = await getProducts() || [] } catch (e) { error.value = '加载失败' } finally { loading.value = false }
})

async function submit() {
  if (!form.product_name || !form.price) { uni.showToast({ title: '请填写必填项', icon: 'none' }); return }
  saving.value = true
  try { await createProduct(form); showForm.value = false; list.value = await getProducts() || []; uni.showToast({ title: '上架成功' }) }
  catch (e) {} finally { saving.value = false }
}

async function toggle(p) {
  await toggleProduct(p.id)
  list.value = await getProducts() || []
}
</script>

<style scoped>
.ent-products { padding:20rpx; }
.header-row { display:flex; justify-content:space-between; align-items:center; margin-bottom:20rpx; }
.title { font-size:36rpx; font-weight:bold; }
.empty { padding-top:150rpx; }
.grid { display:flex; flex-wrap:wrap; gap:16rpx; }
.p-card { width:calc(50% - 8rpx); background:#fff; border-radius:12rpx; padding:20rpx; }
.p-name { font-size:28rpx; font-weight:bold; }
.p-spec { font-size:22rpx; color:#999; }
.p-price { font-size:30rpx; color:#e53935; font-weight:bold; margin-top:8rpx; }
.p-stock { font-size:24rpx; color:#666; }
.badge { font-size:20rpx; padding:4rpx 10rpx; border-radius:6rpx; margin-top:8rpx; display:inline-block; }
.badge.success { background:#e8f5e9; color:#2e7d32; }
.badge.secondary { background:#f5f5f5; color:#999; }
.form-popup { padding:40rpx 30rpx; }
.form-title { font-size:34rpx; font-weight:bold; text-align:center; display:block; margin-bottom:30rpx; }
</style>
