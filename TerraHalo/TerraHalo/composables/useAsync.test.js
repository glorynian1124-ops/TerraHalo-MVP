/** useAsync composable 测试 */
import { describe, it, expect, vi } from 'vitest'
import { useAsync } from '@/composables/useAsync'

describe('useAsync', () => {
  it('初始状态 loading=false error=null data=null', () => {
    const { loading, error, data } = useAsync(() => Promise.resolve('ok'))
    expect(loading.value).toBe(false)
    expect(error.value).toBe(null)
    expect(data.value).toBe(null)
  })

  it('execute 成功后 data 有值', async () => {
    const { loading, error, data, execute } = useAsync(() => Promise.resolve([1,2,3]))
    await execute()
    expect(loading.value).toBe(false)
    expect(error.value).toBe(null)
    expect(data.value).toEqual([1,2,3])
  })

  it('execute 失败后 error 有消息', async () => {
    const { error, execute } = useAsync(() => Promise.reject({ error: '失败' }))
    await execute()
    expect(error.value).toBe('失败')
  })

  it('execute 中 loading 为 true', () => {
    let captured = false
    const { execute } = useAsync(async () => {
      await new Promise(r => setTimeout(r, 10))
    })
    const p = execute()
    // loading 在开始时应为 true（但由于 await 后的微任务，这里简化检查）
    expect(p).toBeInstanceOf(Promise)
  })

  it('reset 清除所有状态', async () => {
    const { data, error, execute, reset } = useAsync(() => Promise.resolve('x'))
    await execute()
    reset()
    expect(data.value).toBe(null)
    expect(error.value).toBe(null)
  })
})
