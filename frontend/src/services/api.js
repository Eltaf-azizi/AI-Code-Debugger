// API Service for Frontend
// Handles all API calls to the backend

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

class ApiService {
  constructor(baseUrl = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseUrl}${endpoint}`;
    
    const config = {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.detail || `HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  }

  // Health check
  async healthCheck() {
    return this.request('/health');
  }

  // Summarize code
  async summarize(code, language = 'auto', structured = true) {
    return this.request('/summarize', {
      method: 'POST',
      body: JSON.stringify({ code, language, structured }),
    });
  }

  // Debug code
  async debug(code, language = 'auto', includeStaticAnalysis = true) {
    return this.request('/debug', {
      method: 'POST',
      body: JSON.stringify({ 
        code, 
        language, 
        include_static_analysis: includeStaticAnalysis 
      }),
    });
  }

  // Explain code
  async explain(code, language = 'auto', detailLevel = 'medium') {
    return this.request('/explain', {
      method: 'POST',
      body: JSON.stringify({ code, language, detail_level: detailLevel }),
    });
  }

  // Optimize code
  async optimize(code, language = 'auto', focus = null) {
    return this.request('/optimize', {
      method: 'POST',
      body: JSON.stringify({ code, language, focus }),
    });
  }

  // Security analysis
  async security(code, language = 'auto', includeOwasp = true) {
    return this.request('/security', {
      method: 'POST',
      body: JSON.stringify({ 
        code, 
        language, 
        include_owasp: includeOwasp 
      }),
    });
  }
}

export const apiService = new ApiService();
export default apiService;
