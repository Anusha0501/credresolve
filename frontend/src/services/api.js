import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const chatAPI = {
  sendMessage: async (phoneNumber, message, language = 'hindi') => {
    const response = await api.post('/chat', {
      phone_number: phoneNumber,
      message,
      language,
    })
    return response.data
  },
}

export const metricsAPI = {
  getMetrics: async () => {
    const response = await api.get('/metrics')
    return response.data
  },
}

export const memoryAPI = {
  getMemory: async (phoneNumber) => {
    const response = await api.get(`/memory/${phoneNumber}`)
    return response.data
  },
}

export const toolAPI = {
  callTool: async (toolName, functionName, parameters) => {
    const response = await api.post('/tool', {
      tool_name: toolName,
      function: functionName,
      parameters,
    })
    return response.data
  },
}

export const knowledgeAPI = {
  retrieve: async (query, topK = 3) => {
    const response = await api.post('/knowledge/retrieve', null, {
      params: { query: query, top_k: topK }
    })
    return response.data
  },
}

export const customerAPI = {
  getCustomer: async (phoneNumber) => {
    const response = await api.get(`/customer/${phoneNumber}`)
    return response.data
  },
}

export default api
