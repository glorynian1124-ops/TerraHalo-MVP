import http from './request'

export function getUserProfile() {
  return http.get('/api/user/profile')
}

export function getProducts(params = {}) {
  return http.get('/api/products', params)
}

export function getProductDetail(id) {
  return http.get(`/api/products/${id}`)
}
