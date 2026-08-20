import http from './request'

export function createProductOrder(data) {
  return http.post('/api/product-order/create', data)
}

export function getProductOrders() {
  return http.get('/api/product-orders')
}

export function getProductOrderDetail(id) {
  return http.get(`/api/product-order/${id}`)
}

export function payProductOrder(orderId) {
  return http.post(`/api/product-order/${orderId}/pay`)
}
