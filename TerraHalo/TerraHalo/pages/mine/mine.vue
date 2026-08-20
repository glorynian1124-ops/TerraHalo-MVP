<template>
  <view class="mine-page">
    <view class="user-card">
      <image class="avatar" :src="user.avatar || defaultAvatar" />
      <view class="user-info">
        <text class="username">{{ user.username || '未登录' }}</text>
        <text class="role">{{ roleLabel }}</text>
      </view>
      <text class="credit">信用 {{ user.credit_score || '-' }}</text>
    </view>

    <!-- 农户/供应商菜单 -->
    <view class="menu" v-if="isFarmer">
      <view class="menu-item" @click="goPage('/pages/publish/publish')"><text>发布原料</text><up-icon name="arrow-right" /></view>
      <view class="menu-item" @click="goPage('/pages/materials/materials')"><text>原料市场</text><up-icon name="arrow-right" /></view>
      <view class="menu-item" @click="goTab('/pages/shop/shop')"><text>商品商城</text><up-icon name="arrow-right" /></view>
      <view class="menu-item" @click="goTab('/pages/orders/orders')"><text>我的订单</text><up-icon name="arrow-right" /></view>
      <view class="menu-item" @click="goPage('/pages/cart/cart')"><text>购物车</text><up-icon name="arrow-right" /></view>
      <view class="menu-item" @click="goPage('/pages/settlement/settlement')"><text>结算账单</text><up-icon name="arrow-right" /></view>
    </view>

    <!-- 企业菜单 -->
    <view class="menu" v-if="isEnterprise">
      <view class="menu-item" @click="goTab('/pages/enterprise/dashboard')"><text>工作台</text><up-icon name="arrow-right" /></view>
      <view class="menu-item" @click="goTab('/pages/enterprise/demands')"><text>采购需求</text><up-icon name="arrow-right" /></view>
      <view class="menu-item" @click="goTab('/pages/enterprise/matches')"><text>匹配确认</text><up-icon name="arrow-right" /></view>
      <view class="menu-item" @click="goTab('/pages/enterprise/products')"><text>商品管理</text><up-icon name="arrow-right" /></view>
      <view class="menu-item" @click="goPage('/pages/settlement/settlement')"><text>结算账单</text><up-icon name="arrow-right" /></view>
    </view>

    <!-- 司机菜单 -->
    <view class="menu" v-if="isDriver">
      <view class="menu-item" @click="goTab('/pages/driver/tasks')"><text>任务管理</text><up-icon name="arrow-right" /></view>
      <view class="menu-item" @click="goPage('/pages/driver/history')"><text>历史任务</text><up-icon name="arrow-right" /></view>
    </view>

    <view class="menu">
      <view class="menu-item" @click="goProfile"><text>个人资料</text><up-icon name="arrow-right" /></view>
      <view class="menu-item" @click="goAbout"><text>关于我们</text><up-icon name="arrow-right" /></view>
    </view>

    <up-button v-if="!user.username" type="primary" @click="goLogin" block
              shape="circle" custom-style="margin:40rpx 20rpx">登录/注册</up-button>
    <up-button v-else type="default" @click="logout" block
              shape="circle" custom-style="margin:40rpx 20rpx">退出登录</up-button>
  </view>
</template>

<script setup>
import { computed } from 'vue'
import { useUserStore } from '@/store/user'

const userStore = useUserStore()
const defaultAvatar = 'https://api.dicebear.com/7.x/avataaars/svg?seed=default'

const user = computed(() => userStore.currentUser || {})
const isFarmer = computed(() => userStore.isFarmer)
const isEnterprise = computed(() => userStore.isEnterprise)
const isDriver = computed(() => userStore.isDriver)
const roleLabel = computed(() => userStore.roleLabel)

function goLogin() { uni.navigateTo({ url: '/pages/login/login' }) }
function goPage(url) { uni.navigateTo({ url }) }
function goTab(url) { uni.switchTab({ url }) }
function goProfile() { uni.showToast({ title: '功能开发中', icon: 'none' }) }
function goAbout() { uni.showToast({ title: '沃土之环 v1.0', icon: 'none' }) }
async function logout() {
  await userStore.logout()
  uni.showToast({ title: '已退出', icon: 'success' })
}
</script>

<style scoped>
.mine-page { min-height:100vh; background:#f5f5f5; padding-bottom:30rpx; }
.user-card { display:flex; align-items:center; background:linear-gradient(135deg,#155724,#1e7e34); padding:50rpx 30rpx; color:#fff; }
.avatar { width:100rpx; height:100rpx; border-radius:50%; background:#fff; margin-right:20rpx; }
.username { font-size:36rpx; font-weight:bold; }
.role { font-size:24rpx; opacity:0.8; }
.credit { margin-left:auto; font-size:24rpx; }
.menu { background:#fff; margin:20rpx; border-radius:16rpx; }
.menu-item { display:flex; justify-content:space-between; padding:24rpx; border-bottom:1rpx solid #f0f0f0; font-size:28rpx; }
</style>
