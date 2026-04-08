// utils/api.js — Axios instance
// In production: API is on same server, use /api prefix
// In development: API is on localhost:8000
import axios from 'axios';

const baseURL = process.env.REACT_APP_API_URL
  ? process.env.REACT_APP_API_URL + '/api'
  : '/api';

const api = axios.create({
  baseURL,
  timeout: 10000,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('sf_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      localStorage.removeItem('sf_user');
      localStorage.removeItem('sf_token');
      window.location.href = '/login';
    }
    return Promise.reject(err);
  }
);

export default api;
