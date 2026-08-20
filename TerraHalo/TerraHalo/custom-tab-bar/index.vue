<template>
  <view class="tab-bar" v-if="visible">
    <view v-for="(tab, idx) in tabs" :key="idx" class="tab-item"
          :class="{ active: current === idx }" @click="switchTab(idx, tab.pagePath)">
      <text class="tab-icon">{{ tab.icon }}</text>
      <text class="tab-text">{{ tab.text }}</text>
    </view>
  </view>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useUserStore } from '@/store/user'

const userStore = useUserStore()
const current = ref(0)
const visible = ref(true)

// 隐藏 TabBar 的页面路径
const hidePages = ['pages/login/login', 'pages/register/register', 'pages/order-create/order-create', 'pages/product-order-create/product-order-create']

// 角色 → Tab 映射
const roleTabs = {
  farmer: [
    { text: '首页', icon: '🏠', pagePath: '/pages/index/index' },
    { text: '原料', icon: '📦', pagePath: '/pages/materials/materials' },
    { text: '商城', icon: '🛒', pagePath: '/pages/shop/shop' },
    { text: '订单', icon: '📋', pagePath: '/pages/orders/orders' },
    { text: '我的', icon: '👤', pagePath: '/pages/mine/mine' },
  ],
  supplier: [
    { text: '首页', icon: '🏠', pagePath: '/pages/index/index' },
    { text: '原料', icon: '📦', pagePath: '/pages/materials/materials' },
    { text: '商城', icon: '🛒', pagePath: '/pages/shop/shop' },
    { text: '订单', icon: '📋', pagePath: '/pages/orders/orders' },
    { text: '我的', icon: '👤', pagePath: '/pages/mine/mine' },
  ],
  enterprise: [
    { text: '工作台', icon: '📊', pagePath: '/pages/enterprise/dashboard' },
    { text: '需求', icon: '📝', pagePath: '/pages/enterprise/demands' },
    { text: '匹配', icon: '🤝', pagePath: '/pages/enterprise/matches' },
    { text: '商品', icon: '🏷️', pagePath: '/pages/enterprise/products' },
    { text: '我的', icon: '👤', pagePath: '/pages/mine/mine' },
  ],
  driver: [
    { text: '任务', icon: '📋', pagePath: '/pages/driver/tasks' },
    { text: '历史', icon: '📜', pagePath: '/pages/driver/history' },
    { text: '我的', icon: '👤', pagePath: '/pages/mine/mine' },
  ],
}

// 从 store 驱动 tab 列表
const tabs = computed(() => roleTabs[userStore.currentRole] || roleTabs.farmer)

// 监听页面切换
watch(() => getCurrentPages(), () => {
  const pages = getCurrentPages()
  if (pages.length === 0) return
  const path = pages[pages.length - 1].route
  visible.value = !hidePages.includes(path)
  // 匹配当前 tab
  const idx = tabs.value.findIndex(t => t.pagePath === '/' + path)
  if (idx >= 0) current.value = idx
}, { immediate: true })

function switchTab(idx, path) {
  current.value = idx
  uni.switchTab({ url: path })
}
</script>

<style scoped>
.tab-bar {
  position: fixed; bottom: 0; left: 0; right: 0;
  display: flex; background: #fff;
  border-top: 1px solid #eee;
  padding-bottom: env(safe-area-inset-bottom);
  z-index: 999;
}
.tab-item { flex: 1; text-align: center; padding: 8rpx 0; }
.tab-icon { font-size: 40rpx; display: block; }
.tab-text { font-size: 20rpx; color: #999; }
.tab-item.active .tab-text { color: #28a745; font-weight: bold; }
</style>
