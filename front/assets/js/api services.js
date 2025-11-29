/* ===================================
   MEDCORE - API Service
   Handles all backend API calls
   =================================== */

'use strict';

class ApiService {
    constructor() {
        // Configure based on environment
        this.baseURL = window.location.hostname === 'localhost' 
            ? 'http://localhost:8000'
            : 'https://your-production-url.com';
        
        this.token = this.getToken();
    }

    /* ===================================
       TOKEN MANAGEMENT
       =================================== */
    
    getToken() {
        return localStorage.getItem('auth_token');
    }

    setToken(token) {
        localStorage.setItem('auth_token', token);
        this.token = token;
    }

    clearToken() {
        localStorage.removeItem('auth_token');
        this.token = null;
    }

    /* ===================================
       HTTP REQUEST WRAPPER
       =================================== */
    
    async request(endpoint, options = {}) {
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };

        // Add auth token if available
        if (this.token) {
            config.headers['Authorization'] = `Bearer ${this.token}`;
        }

        try {
            const response = await fetch(`${this.baseURL}${endpoint}`, config);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Request failed');
            }

            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    /* ===================================
       AUTHENTICATION ENDPOINTS
       =================================== */
    
    async signup(userData) {
        try {
            const response = await this.request('/auth/signup', {
                method: 'POST',
                body: JSON.stringify({
                    username: userData.name.replace(/\s+/g, '_').toLowerCase(),
                    email: userData.email,
                    password: userData.password,
                    full_name: userData.name,
                    role: userData.role // 'customer' or 'distributor'
                })
            });

            // Supabase returns session with access_token
            if (response.session?.access_token) {
                this.setToken(response.session.access_token);
            }

            return response;
        } catch (error) {
            console.error('Signup error:', error);
            throw error;
        }
    }

    async login(credentials) {
        try {
            const response = await this.request('/auth/login', {
                method: 'POST',
                body: JSON.stringify({
                    email: credentials.email,
                    password: credentials.password
                })
            });

            // Supabase returns session with access_token
            if (response.session?.access_token) {
                this.setToken(response.session.access_token);
            }

            return response;
        } catch (error) {
            console.error('Login error:', error);
            throw error;
        }
    }

    async getCurrentUser() {
        try {
            return await this.request('/auth/me');
        } catch (error) {
            console.error('Get user error:', error);
            this.clearToken();
            throw error;
        }
    }

    logout() {
        this.clearToken();
        window.location.href = '/front/index.html';
    }

    /* ===================================
       PRODUCT ENDPOINTS
       =================================== */
    
    async getProducts(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        return await this.request(`/products?${queryString}`);
    }

    async getProduct(productId) {
        return await this.request(`/products/${productId}`);
    }

    async createProduct(productData) {
        return await this.request('/products/create', {
            method: 'POST',
            body: JSON.stringify(productData)
        });
    }

    async updateProduct(productId, productData) {
        return await this.request(`/products/${productId}`, {
            method: 'PUT',
            body: JSON.stringify(productData)
        });
    }

    async deleteProduct(productId) {
        return await this.request(`/products/${productId}`, {
            method: 'DELETE'
        });
    }

    /* ===================================
       UTILITY METHODS
       =================================== */
    
    isAuthenticated() {
        return !!this.token;
    }

    async checkAuth() {
        if (!this.isAuthenticated()) {
            return false;
        }

        try {
            await this.getCurrentUser();
            return true;
        } catch {
            return false;
        }
    }
}

// Create singleton instance
const api = new ApiService();

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = api;
}