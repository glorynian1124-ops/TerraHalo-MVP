<script setup>
import { onLaunch } from '@dcloudio/uni-app'
import { useUserStore } from '@/store/user'

onLaunch(() => {
  console.log('沃土之环 App 启动')

  // 从 localStorage 恢复登录态
  const userStore = useUserStore()
  userStore.initFromStorage()
})

// ==================== 全局路由守卫 ====================
// 需要登录才能访问的页面（模糊匹配前缀）
const authRequired = [
  'pages/publish/publish',
  'pages/cart/cart',
  'pages/order-create/order-create',
  'pages/orders/orders',
  'pages/order-detail/order-detail',
  'pages/mine/mine',           // 虽然自带登录提示，但拦截更安全
  'pages/enterprise/',
  'pages/driver/',
]

// 登录/注册页已登录则跳走
const guestOnly = [
  'pages/login/login',
  'pages/register/register',
]

function needAuth(path) {
  return authRequired.some(p => path.startsWith(p))
}

function isGuestPage(path) {
  return guestOnly.some(p => path.startsWith(p))
}

// 截获 navigateTo
uni.addInterceptor('navigateTo', {
  invoke(args) {
    const userStore = useUserStore()
    const path = args.url?.split('?')[0] || ''

    if (needAuth(path) && !userStore.isLoggedIn) {
      uni.showToast({ title: '请先登录', icon: 'none' })
      uni.navigateTo({ url: '/pages/login/login' })
      return false  // 阻止原跳转
    }
    if (isGuestPage(path) && userStore.isLoggedIn) {
      // 已登录用户访问登录/注册页，跳回首页
      uni.switchTab({ url: '/pages/index/index' })
      return false
    }
    return true
  },
})

// 截获 switchTab（Tab 页除了 mine 都可以看，但 mine 需要登录提示）
uni.addInterceptor('switchTab', {
  invoke(args) {
    const userStore = useUserStore()
    const path = args.url?.split('?')[0] || ''

    if (path === 'pages/mine/mine' && !userStore.isLoggedIn) {
      // 不阻止进入 mine 页，因为 mine 自带未登录 UI
      return true
    }
    return true
  },
})
</script>

<style lang="scss">
@import "uview-plus/index.scss";

page {
  background-color: #f5f5f5;
  font-family: -apple-system, BlinkMacSystemFont, 'Helvetica Neue', sans-serif;
}

:root {
  --u-primary: #28a745;
  --u-success: #28a745;
  --u-warning: #fd7e14;
  --u-error: #dc3545;
  --u-info: #17a2b8;
}
</style>
