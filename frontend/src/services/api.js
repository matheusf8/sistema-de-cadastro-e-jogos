/**
 * Serviço de API para comunicação com o backend
 */

import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Criar instância do axios
const api = axios.create({
  baseURL: API_BASE_URL,
});

// Adicionar token ao header se disponível
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// ===== AUTH =====
export const authAPI = {
  register: (userData) => api.post('/auth/register', userData),
  login: (credentials) => api.post('/auth/login', credentials),
  getCurrentUser: () => api.get('/auth/me'),
};

// ===== NOTES =====
export const notesAPI = {
  createNote: (noteData) => api.post('/notes/', noteData),
  getNotes: (skip = 0, limit = 100) => api.get('/notes/', { params: { skip, limit } }),
  getNote: (noteId) => api.get(`/notes/${noteId}`),
  updateNote: (noteId, noteData) => api.put(`/notes/${noteId}`, noteData),
  deleteNote: (noteId) => api.delete(`/notes/${noteId}`),
};

export default api;
