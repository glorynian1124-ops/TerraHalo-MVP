<template>
  <view class="login-page">
    <!-- Logo区 -->
    <view class="logo-area">
      <text class="logo-icon">🌱</text>
      <text class="logo-title">沃土之环</text>
      <text class="logo-sub">绿色农业 · 循环经济</text>
    </view>

    <!-- 表单卡片 -->
    <view class="form-card">
      <!-- Tab切换 -->
      <view class="tab-row">
        <view class="tab-item" :class="{ active: tab === 'login' }" @click="tab = 'login'">登录</view>
        <view class="tab-item" :class="{ active: tab === 'register' }" @click="tab = 'register'">注册</view>
      </view>

      <!-- 登录表单 -->
      <view v-if="tab === 'login'" class="form-wrap">
        <view class="input-group">
          <text class="input-label">用户名</text>
          <view class="input-box">
            <text class="input-icon">👤</text>
            <input class="input-field" v-model="form.username" placeholder="请输入用户名" />
          </view>
        </view>
        <view class="input-group">
          <text class="input-label">密码</text>
          <view class="input-box">
            <text class="input-icon">🔒</text>
            <input class="input-field" v-model="form.password" type="password" placeholder="请输入密码" />
          </view>
        </view>
        <view class="form-extra">
          <label class="remember-row">
            <checkbox :checked="rememberMe" @click="rememberMe = !rememberMe" style="transform:scale(0.7)" />
            <text class="remember-text">记住我</text>
          </label>
          <text class="forgot-link">忘记密码？</text>
        </view>
        <button class="submit-btn" :loading="loading" @click="handleLogin">登录</button>
        <view class="wx-section">
          <view class="divider"><text>或</text></view>
          <button class="wx-btn" :loading="wxLoading" @click="handleWechatLogin">微信一键登录</button>
        </view>
      </view>

      <!-- 注册表单 -->
      <view v-if="tab === 'register'" class="form-wrap">
        <view class="input-group">
          <text class="input-label">角色</text>
          <view class="role-row">
            <view class="role-pill" :class="{ active: regRole === 'farmer' }" @click="regRole = 'farmer'">农户</view>
            <view class="role-pill" :class="{ active: regRole === 'enterprise' }" @click="regRole = 'enterprise'">企业</view>
            <view class="role-pill" :class="{ active: regRole === 'driver' }" @click="regRole = 'driver'">司机</view>
          </view>
        </view>
        <view class="input-group">
          <text class="input-label">用户名</text>
          <view class="input-box">
            <text class="input-icon">👤</text>
            <input class="input-field" v-model="regForm.username" placeholder="请输入用户名" />
          </view>
        </view>
        <view class="input-group">
          <text class="input-label">手机号</text>
          <view class="input-box">
            <text class="input-icon">📱</text>
            <input class="input-field" v-model="regForm.phone" type="number" placeholder="请输入手机号" />
          </view>
        </view>
        <view class="input-group">
          <text class="input-label">密码</text>
          <view class="input-box">
            <text class="input-icon">🔒</text>
            <input class="input-field" v-model="regForm.password" type="password" placeholder="请输入密码" />
          </view>
        </view>
        <view class="input-group">
          <text class="input-label">确认密码</text>
          <view class="input-box">
            <text class="input-icon">🔒</text>
            <input class="input-field" v-model="regForm.confirmPassword" type="password" placeholder="请再次输入密码" />
          </view>
        </view>
        <button class="submit-btn" @click="handleRegister">注册</button>
      </view>
    </view>

    <text class="agreement-text">登录即表示同意 <text class="link">服务条款</text> 和 <text class="link">隐私政策</text></text>
  </view>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useUserStore } from '@/store/user'

const userStore = useUserStore()
const tab = ref('login')
const loading = ref(false)
const wxLoading = ref(false)
const rememberMe = ref(false)
const regRole = ref('farmer')
const form = reactive({ username: '', password: '' })
const regForm = reactive({ username: '', phone: '', password: '', confirmPassword: '' })

async function handleLogin() {
  if (!form.username || !form.password) {
    uni.showToast({ title: '请输入用户名和密码', icon: 'none' })
    return
  }
  loading.value = true
  try {
    await userStore.login(form.username, form.password)
    uni.showToast({ title: '登录成功', icon: 'success' })
    const role = userStore.currentRole
    const homeMap = { admin: '/pages/index/index', farmer: '/pages/index/index', supplier: '/pages/index/index', enterprise: '/pages/enterprise/dashboard', driver: '/pages/driver/tasks' }
    setTimeout(() => uni.switchTab({ url: homeMap[role] || '/pages/index/index' }), 800)
  } catch (e) {} finally { loading.value = false }
}

function handleRegister() {
  uni.showToast({ title: '注册功能开发中', icon: 'none' })
}

async function handleWechatLogin() {
  wxLoading.value = true
  try {
    const [err, loginRes] = await uni.login({ provider: 'weixin' })
    if (err || !loginRes.code) {
      await userStore.login('微信用户', 'wechat_dev')
      uni.showToast({ title: '开发模式微信登录', icon: 'success' })
    } else {
      const { wechatLogin: apiWechatLogin } = await import('@/api/auth')
      const res = await apiWechatLogin(loginRes.code)
      userStore.user = res.user
      userStore.isLoggedIn = true
      uni.setStorageSync('userInfo', res.user)
      uni.showToast({ title: '登录成功', icon: 'success' })
      const role = userStore.currentRole
      const homeMap = { admin: '/pages/index/index', farmer: '/pages/index/index', supplier: '/pages/index/index', enterprise: '/pages/enterprise/dashboard', driver: '/pages/driver/tasks' }
      setTimeout(() => uni.switchTab({ url: homeMap[role] || '/pages/index/index' }), 800)
    }
  } catch (e) {} finally { wxLoading.value = false }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60rpx 40rpx;
  background: linear-gradient(135deg, #6B4F10 0%, #2D5A27 60%, #1B3D18 100%);
}
.logo-area { text-align: center; margin-bottom: 50rpx; }
.logo-icon { font-size: 100rpx; }
.logo-title { display: block; font-size: 48rpx; color: #fff; font-weight: bold; margin-top: 10rpx; }
.logo-sub { display: block; font-size: 26rpx; color: rgba(255,255,255,0.7); margin-top: 8rpx; }
.form-card {
  width: 100%;
  background: #fff;
  border-radius: 24rpx;
  padding: 40rpx 36rpx;
}
.tab-row { display: flex; border-bottom: 1px solid #ede6d5; margin-bottom: 36rpx; }
.tab-item {
  flex: 1; text-align: center; padding-bottom: 16rpx; font-size: 30rpx; font-weight: 600;
  color: #6e6456; border-bottom: 2px solid transparent;
}
.tab-item.active { color: #2b2416; border-bottom-color: #8B6914; }
.form-wrap { display: flex; flex-direction: column; gap: 28rpx; }
.input-group { display: flex; flex-direction: column; gap: 8rpx; }
.input-label { font-size: 26rpx; color: #2b2416; font-weight: 500; }
.input-box {
  display: flex; align-items: center; height: 88rpx; border: 1px solid #ddd2ba;
  border-radius: 24rpx; background: #faf8f2; padding: 0 20rpx;
}
.input-icon { font-size: 32rpx; margin-right: 16rpx; }
.input-field { flex: 1; font-size: 28rpx; color: #2b2416; }
.form-extra { display: flex; justify-content: space-between; align-items: center; }
.remember-row { display: flex; align-items: center; }
.remember-text { font-size: 26rpx; color: #6e6456; }
.forgot-link { font-size: 26rpx; color: #8B6914; }
.submit-btn {
  width: 100%; height: 96rpx; border-radius: 48rpx; background: #8B6914;
  color: #fff; font-size: 32rpx; font-weight: 600; border: none; margin-top: 10rpx;
}
.wx-section { margin-top: 20rpx; }
.divider { display: flex; align-items: center; gap: 16rpx; margin: 20rpx 0; }
.divider::before, .divider::after { content: ''; flex: 1; height: 1px; background: #ede6d5; }
.divider text { font-size: 24rpx; color: #a39887; }
.wx-btn {
  width: 100%; height: 96rpx; border-radius: 48rpx; background: #07c160;
  color: #fff; font-size: 30rpx; font-weight: 600; border: none;
}
.role-row { display: flex; gap: 16rpx; }
.role-pill {
  flex: 1; height: 72rpx; display: flex; align-items: center; justify-content: center;
  border-radius: 36rpx; border: 1px solid #ede6d5; font-size: 26rpx; color: #6e6456;
  background: transparent;
}
.role-pill.active { background: #8B6914; color: #fff; border-color: #8B6914; }
.agreement-text { margin-top: 30rpx; font-size: 24rpx; color: rgba(255,255,255,0.6); }
.link { color: rgba(255,255,255,0.9); text-decoration: underline; }
</style>