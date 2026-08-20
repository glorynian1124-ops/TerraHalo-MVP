import http from './request'

export function getCart() {
  return http.get('/api/cart')  // 注意：后端 cart 数据在 session 中，通过页面路由返回
}

export function addToCart(materialId, quantity = 1) {
  return http.post('/api/cart/add', { material_id: materialId, quantity })
}

export function updateCart(materialId, change) {
  return http.post('/api/cart/update', { material_id: materialId, change })
}

export function removeFromCart(materialId) {
  return http.post('/api/cart/remove', { material_id: materialId })
}
