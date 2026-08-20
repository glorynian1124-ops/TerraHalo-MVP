import http from './request'

export function login(username, password) {
  return http.post('/api/login', { username, password })
}

export function register(data) {
  return http.post('/api/register', data)
}

export function logout() {
  return http.get('/logout')
}

export function getUserProfile() {
  return http.get('/api/user/profile')
}

export function wechatLogin(code) {
  return http.post('/api/wechat-login', { code })
}
