import http from './request'

export function getMaterials(params = {}) {
  return http.get('/api/materials', params)
}

export function getMaterialDetail(id) {
  return http.get('/api/materials', { id })
}

export function createMaterial(data) {
  return http.post('/api/materials', data)
}

export function toggleMaterial(materialId) {
  return http.post('/api/materials/toggle', { material_id: materialId })
}
