import http from './request'

const BASE = '/enterprise/api'

export function getDemands(params = {}) {
  return http.get(`${BASE}/demands`, params)
}

export function createDemand(data) {
  return http.post(`${BASE}/demands`, data)
}

export function updateDemand(id, data) {
  return http.put(`${BASE}/demands/${id}`, data)
}

export function closeDemand(id) {
  return http.post(`${BASE}/demands/${id}/close`)
}

export function getMatches(demandId) {
  return http.get(`${BASE}/demands/${demandId}/matches`)
}

export function confirmMatch(matchId) {
  return http.post(`${BASE}/matches/${matchId}/confirm`)
}

export function getTasks() {
  return http.get(`${BASE}/tasks`)
}

export function getProducts() {
  return http.get(`${BASE}/products`)
}

export function createProduct(data) {
  return http.post(`${BASE}/products`, data)
}

export function updateProduct(id, data) {
  return http.put(`${BASE}/products/${id}`, data)
}

export function toggleProduct(id) {
  return http.post(`${BASE}/products/${id}/toggle`)
}
