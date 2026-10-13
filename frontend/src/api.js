import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

export const api = {
  // Doctor Endpoints
  getDoctors: async () => {
    const res = await apiClient.get('/doctors/');
    return res.data;
  },

  getDoctorById: async (id) => {
    const res = await apiClient.get(`/doctors/${id}`);
    return res.data;
  },

  addDoctor: async (doctorData) => {
    const res = await apiClient.post('/doctors/', doctorData);
    return res.data;
  },

  updateDoctor: async (id, doctorData) => {
    const res = await apiClient.put(`/doctors/${id}`, doctorData);
    return res.data;
  },

  deleteDoctor: async (id) => {
    const res = await apiClient.delete(`/doctors/${id}`);
    return res.data;
  },

  getDoctorAvailability: async (doctorId, dateString) => {
    const params = dateString ? { query_date: dateString } : {};
    const res = await apiClient.get(`/doctors/${doctorId}/availability`, { params });
    return res.data;
  },

  // Appointment Endpoints
  getAppointments: async (params = {}) => {
    const res = await apiClient.get('/appointments/', { params });
    return res.data;
  },

  bookAppointment: async (appointmentData) => {
    const res = await apiClient.post('/appointments/', appointmentData);
    return res.data;
  },

  cancelAppointment: async (appointmentId) => {
    const res = await apiClient.delete(`/appointments/${appointmentId}`);
    return res.data;
  },

  // Analytics Stats
  getStats: async () => {
    const res = await apiClient.get('/stats');
    return res.data;
  },
};

export default apiClient;
