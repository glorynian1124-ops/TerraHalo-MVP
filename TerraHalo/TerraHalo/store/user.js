import { defineStore } from 'pinia'
import { login as apiLogin, register as apiRegister, logout as apiLogout } from '@/api/auth'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null,           // { id, username, role, avatar, credit_score, … }
    isLoggedIn: false,
    initReady: false,     // 首次 localStorage 恢复完成标记
  }),

  getters: {
    currentUser: (state) => state.user,
    currentRole: (state) => {
      if (!state.user) return 'farmer'
      return state.user.role === 'buyer' ? 'farmer' : state.user.role
    },
    roleLabel: (state) => {
      const m = { admin: '管理员', supplier: '供应商', enterprise: '企业', driver: '司机', buyer: '买家', farmer: '农户' }
      return m[state.user?.role] || '农户'
    },
    isFarmer: (state) => ['farmer', 'supplier', 'admin', 'buyer'].includes(state.user?.role),
    isEnterprise: (state) => state.user?.role === 'enterprise',
    isDriver: (state) => state.user?.role === 'driver',
    isAdmin: (state) => state.user?.role === 'admin',
    creditScore: (state) => state.user?.credit_score ?? '-',
  },

  actions: {
    /** 从 localStorage 恢复登录态（App.vue onLaunch 调用） */
    initFromStorage() {
      try {
        const info = uni.getStorageSync('userInfo')
        if (info && info.id) {
          this.user = info
          this.isLoggedIn = true
          const role = info.role === 'buyer' ? 'farmer' : info.role
          uni.$emit('roleChanged', role)
        }
      } catch (e) { /* ignore */ }
      this.initReady = true
    },

    /** 登录 */
    async login(username, password) {
      const res = await apiLogin(username, password)
      this.user = res.user
      this.isLoggedIn = true
      uni.setStorageSync('userInfo', res.user)
      const role = res.user.role === 'buyer' ? 'farmer' : res.user.role
      uni.$emit('roleChanged', role)
      return res
    },

    /** 注册（成功后返回，不自动登录） */
    async register(data) {
      const res = await apiRegister(data)
      return res
    },

    /** 退出登录 */
    async logout() {
      try { await apiLogout() } catch (e) { /* 忽略网络错误 */ }
      this.user = null
      this.isLoggedIn = false
      uni.removeStorageSync('userInfo')
      uni.$emit('roleChanged', 'farmer')
    },
  },
})
