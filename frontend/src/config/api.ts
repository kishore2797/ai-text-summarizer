// API Configuration
export const API_CONFIG = {
  // Development
  development: {
    apiUrl: 'http://localhost:8000'
  },
  // Production - Update this with your Render URL
  production: {
    apiUrl: 'https://your-render-url.onrender.com'
  }
}

// Get current environment
export const getApiUrl = () => {
  const env = process.env.NODE_ENV || 'development'
  return API_CONFIG[env as keyof typeof API_CONFIG].apiUrl
}

// Export base URL
export const API_BASE_URL = getApiUrl()
