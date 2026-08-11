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

// ===== DOCUMENTS =====
export const documentsAPI = {
  upload: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/documents/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  list: () => api.get('/documents/'),
  remove: (documentId) => api.delete(`/documents/${documentId}`),
};

// ===== CHAT =====
export const chatAPI = {
  createSession: (documentId, title) =>
    api.post('/chat/sessions', { document_id: documentId, title }),
  listSessions: () => api.get('/chat/sessions'),
  listMessages: (sessionId) => api.get(`/chat/sessions/${sessionId}/messages`),
  sendMessage: (sessionId, content) =>
    api.post(`/chat/sessions/${sessionId}/messages`, { content }),
};

export default api;
