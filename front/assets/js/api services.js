/* ===================================
   MEDCORE - API Service (Fixed)
   Handles all backend API calls
   =================================== */

'use strict';

class ApiService {
    constructor() {
        // Use the correct backend URL
        this.baseURL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
            ? 'http://127.0.0.1:8000'
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
        localStorage.removeItem('user_data');
        this.token = null;
    }

    getUserData() {
        const userData = localStorage.getItem('user_data');
        return userData ? JSON.parse(userData) : null;
    }

    setUserData(userData) {
        localStorage.setItem('user_data', JSON.stringify(userData));
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
            
            // Handle empty responses
            const text = await response.text();
            const data = text ? JSON.parse(text) : {};

            if (!response.ok) {
                throw new Error(data.detail || `Request failed with status ${response.status}`);
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
                    username: userData.username || userData.name.replace(/\s+/g, '_').toLowerCase(),
                    email: userData.email,
                    password: userData.password,
                    full_name: userData.name || userData.full_name,
                    role: userData.role // 'customer' or 'distributor'
                })
            });

            // Store token and user data
            if (response.access_token) {
                this.setToken(response.access_token);
                this.setUserData(response.user);
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

            // Store token and user data
            if (response.access_token) {
                this.setToken(response.access_token);
                this.setUserData(response.user);
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
        return await this.request(`/products${queryString ? '?' + queryString : ''}`);
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
       USER ENDPOINTS
       =================================== */
    
    async getAllUsers() {
        return await this.request('/users/');
    }

    async updateUser(userId, userData) {
        return await this.request(`/users/${userId}`, {
            method: 'PUT',
            body: JSON.stringify(userData)
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

    isDistributor() {
        const userData = this.getUserData();
        return userData && (userData.role === 'distributor' || userData.roles?.includes('distributor'));
    }
}

// Create singleton instance
const api = new ApiService();

// Make it globally available
window.api = api;