import { ref, unref } from 'vue'

/**
 * 统一异步状态管理 composable
 * 
 * @param {Function} fn - 异步函数，返回 Promise
 * @returns {{ loading, error, data, execute, reset }}
 * 
 * 用法：
 *   const { loading, error, data, execute } = useAsync(() => getMaterials(params))
 *   onMounted(() => execute())
 * 
 * 模板中使用：
 *   <up-loading v-if="loading" />
 *   <text v-else-if="error" class="error">{{ error }}</text>
 *   <up-empty v-else-if="!data?.length" text="暂无数据" />
 *   <view v-else>...数据展示...</view>
 */
export function useAsync(fn) {
  const loading = ref(false)
  const error = ref(null)
  const data = ref(null)

  async function execute(...args) {
    loading.value = true
    error.value = null
    try {
      const result = await fn(...args)
      data.value = result
      return result
    } catch (e) {
      const msg = typeof e === 'string' ? e : (e?.error || e?.message || '请求失败')
      error.value = msg
      data.value = null
      return null
    } finally {
      loading.value = false
    }
  }

  function reset() {
    loading.value = false
    error.value = null
    data.value = null
  }

  return { loading, error, data, execute, reset }
}
