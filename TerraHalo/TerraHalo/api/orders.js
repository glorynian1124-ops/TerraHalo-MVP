import http from './request'

export function createOrder(data) {
  return http.post('/api/order/create', data)
}

export function createOrderFromCart(address) {
  return http.post('/api/order/create_from_cart', { shipping_address: address })
}

export function payOrder(orderId) {
  return http.post('/api/order/pay', { order_id: orderId })
}

export function getOrders() {
  return http.get('/api/orders')
}

export function getOrderDetail(id) {
  return http.get(`/api/order/${id}`)
}

export function updateOrderStatus(id, status) {
  return http.post(`/api/order/${id}/status`, { status })
}
