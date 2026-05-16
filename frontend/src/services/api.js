import axios from 'axios'

const API_URL = 'http://localhost:8000/api'

// Instance axios configurée
const api = axios.create({
  baseURL: API_URL,
})

// Ajoute automatiquement le token JWT à chaque requête
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Auth
export const login = (username, password) =>
  api.post('/accounts/login/', { username, password })

export const register = (username, email, password) =>
  api.post('/accounts/register/', { username, email, password })

export const getMe = () =>
  api.get('/accounts/me/')

export const updateProfile = (data) =>
  api.patch('/accounts/profile/', data)

// Posts
export const getPosts = () =>
  api.get('/posts/')

export const generatePost = (subject, tone) =>
  api.post('/posts/generate/', { subject, tone })

export const suggestSubjects = () =>
  api.post('/posts/suggest/')

export const schedulePost = (id, scheduled_at) =>
  api.patch(`/posts/${id}/schedule/`, { scheduled_at })

export default api