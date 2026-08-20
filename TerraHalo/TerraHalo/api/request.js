// 统一请求封装 — 对接 Flask 后端
// H5 浏览器模式自动用 127.0.0.1，APP 模拟器用 10.0.2.2
// #ifdef H5
const BASE_URL = 'http://127.0.0.1:5000'
// #endif
// #ifdef APP-PLUS
const BASE_URL = 'http://10.0.2.2:5000'
// #endif
// #ifndef H5 || APP-PLUS
const BASE_URL = 'http://127.0.0.1:5000'
// #endif

function request(options) {
  return new Promise((resolve, reject) => {
    uni.request({
      url: BASE_URL + options.url,
      method: options.method || 'GET',
      data: options.data || {},
      header: {
        'Content-Type': 'application/json'
      },
      // H5 跨域请求需要携带 cookie
      withCredentials: true,
      success: (res) => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data)
        } else {
          const msg = res.data?.error || `请求失败(${res.statusCode})`
          uni.showToast({ title: msg, icon: 'none' })
          reject(res.data)
        }
      },
      fail: (err) => {
        uni.showToast({ title: '网络连接失败，请确认后端已启动', icon: 'none' })
        reject(err)
      }
    })
  })
}

export default {
  get: (url, data) => request({ url, method: 'GET', data }),
  post: (url, data) => request({ url, method: 'POST', data }),
  put: (url, data) => request({ url, method: 'PUT', data }),
  delete: (url, data) => request({ url, method: 'DELETE', data }),

  /** 上传文件（multipart） */
  upload: (url, filePath, formData = {}) => {
    return new Promise((resolve, reject) => {
      uni.uploadFile({
        url: BASE_URL + url,
        filePath,
        name: 'file',
        formData,
        withCredentials: true,
        success: (res) => {
          try {
            const data = JSON.parse(res.data)
            if (res.statusCode >= 200 && res.statusCode < 300) {
              resolve(data)
            } else {
              uni.showToast({ title: data?.error || '上传失败', icon: 'none' })
              reject(data)
            }
          } catch (e) {
            reject(e)
          }
        },
        fail: (err) => {
          uni.showToast({ title: '网络连接失败，请确认后端已启动', icon: 'none' })
          reject(err)
        },
      })
    })
  },
}
