import http from './request'

const BASE = '/driver/api'

export function getTaskPool() {
  return http.get(`${BASE}/tasks/pool`)
}

export function getActiveTasks() {
  return http.get(`${BASE}/tasks`, { status: 'accepted' })
}

export function getHistoryTasks() {
  return http.get(`${BASE}/tasks`, { status: 'completed' })
}

export function acceptTask(taskId) {
  return http.post(`${BASE}/tasks/${taskId}/accept`)
}

export function completeTask(taskId) {
  return http.post(`${BASE}/tasks/${taskId}/complete`)
}
