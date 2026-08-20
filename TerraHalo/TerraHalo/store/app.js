import { defineStore } from 'pinia'

export const useAppStore = defineStore('app', {
  state: () => ({
    /** 全局加载计数（>0 时显示 loading，支持嵌套） */
    loadingCount: 0,
    /** 全局错误信息（null = 无错误） */
    error: null,
    /** 网络是否在线 */
    online: true,
  }),

  getters: {
    isLoading: (state) => state.loadingCount > 0,
  },

  actions: {
    /** 开始加载（自动计数，支持并发请求） */
    startLoading() {
      this.loadingCount++
    },
    /** 结束加载 */
    stopLoading() {
      if (this.loadingCount > 0) this.loadingCount--
    },
    /** 显示错误 */
    setError(msg) {
      this.error = msg
    },
    /** 清除错误 */
    clearError() {
      this.error = null
    },
    /** 设置网络状态 */
    setOnline(val) {
      this.online = !!val
    },
  },
})
