import axios from 'axios';

const API_URL = 'http://localhost:8000'; // Change this for production

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export default {
  // Get all locations
  async getLocations() {
    const response = await api.get('/locations');
    return response.data.locations;
  },

  // Predict house price
  async predictPrice(data) {
    const response = await api.post('/predict', data);
    return response.data;
  },

  // Check if backend is running
  async healthCheck() {
    try {
      const response = await api.get('/');
      return response.data;
    } catch (error) {
      throw new Error('Backend is not responding');
    }
  }
};