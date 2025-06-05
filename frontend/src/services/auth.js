import axios from "axios";
import { ACCESS_TOKEN, BASE_URL } from "./constants";

const apiUrl = "http://localhost:8000/";

const api = axios.create({
  baseURL: BASE_URL ? BASE_URL : apiUrl,
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem(ACCESS_TOKEN);
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

api.isAuthenticated = () => {
    const accessToken = localStorage.getItem(ACCESS_TOKEN);
    return !!accessToken;
  };

export default api;