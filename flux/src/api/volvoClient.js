import axios from 'axios';

const BASE_URL = import.meta.env.VITE_VCC_API_BASE;
const API_KEY = import.meta.env.VITE_VCC_API_KEY;
const VIN = import.meta.env.VITE_VEHICLE_VIN;

// Create axios instance with default headers
const client = axios.create({
  baseURL: BASE_URL,
  headers: {
    'vcc-api-key': API_KEY,
    'Content-Type': 'application/json'
  }
});

// Add token interceptor (for OAuth token when available)
client.interceptors.request.use((config) => {
  const token = localStorage.getItem('volvo_access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// API Functions
export const volvoAPI = {
  // Vehicle Info
  getVehicleList: () => client.get('/vehicles'),
  getVehicleDetails: (vin = VIN) => client.get(`/vehicles/${vin}`),
  
  // Battery & Fuel (relevant for EVs)
  getFuelStatus: (vin = VIN) => client.get(`/vehicles/${vin}/fuel`),
  
  // Status
  getDoorStatus: (vin = VIN) => client.get(`/vehicles/${vin}/doors`),
  getWindowStatus: (vin = VIN) => client.get(`/vehicles/${vin}/windows`),
  getEngineStatus: (vin = VIN) => client.get(`/vehicles/${vin}/engine-status`),
  
  // Diagnostics & Stats
  getStatistics: (vin = VIN) => client.get(`/vehicles/${vin}/statistics`),
  getOdometer: (vin = VIN) => client.get(`/vehicles/${vin}/odometer`),
  getDiagnostics: (vin = VIN) => client.get(`/vehicles/${vin}/diagnostics`),
  getTyreStatus: (vin = VIN) => client.get(`/vehicles/${vin}/tyres`),
  
  // Commands - Control
  lock: (vin = VIN) => client.post(`/vehicles/${vin}/commands/lock`, {}),
  unlock: (vin = VIN) => client.post(`/vehicles/${vin}/commands/unlock`, {}),
  honk: (vin = VIN) => client.post(`/vehicles/${vin}/commands/honk`, {}),
  flash: (vin = VIN) => client.post(`/vehicles/${vin}/commands/flash`, {}),
  honkFlash: (vin = VIN) => client.post(`/vehicles/${vin}/commands/honk-flash`, {}),
  
  // Engine
  engineStart: (runtimeMinutes = 5, vin = VIN) => 
    client.post(`/vehicles/${vin}/commands/engine-start`, { runtimeMinutes }),
  engineStop: (vin = VIN) => 
    client.post(`/vehicles/${vin}/commands/engine-stop`, {}),
  
  // Climate
  climatizationStart: (vin = VIN) => 
    client.post(`/vehicles/${vin}/commands/climatization-start`, {}),
  climatizationStop: (vin = VIN) => 
    client.post(`/vehicles/${vin}/commands/climatization-stop`, {}),
  
  // Command info
  getAvailableCommands: (vin = VIN) => 
    client.get(`/vehicles/${vin}/commands`),
  getCommandAccessibility: (vin = VIN) => 
    client.get(`/vehicles/${vin}/command-accessibility`),
};

export const setAccessToken = (token) => {
  if (token) {
    localStorage.setItem('volvo_access_token', token);
  }
};

export const clearAccessToken = () => {
  localStorage.removeItem('volvo_access_token');
};

export default volvoAPI;
