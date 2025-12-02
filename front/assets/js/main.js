/* ===================================
   MEDCORE - Main JavaScript
   ===================================
   TABLE OF CONTENTS:
   1. Navigation Component
   2. Footer Component
   3. Carousel Component
   4. Authentication Forms
   5. Dropdown Handlers
   6. Utility Functions
   =================================== */

'use strict';

/* ===================================
   1. NAVIGATION COMPONENT
   =================================== */
const Navigation = {
    init() {
        const header = document.querySelector('header');
        if (!header || header.querySelector('.navbar')) return;
        
        this.render(header);
        this.attachEventListeners();
    },

    render(container) {
        const currentPage = window.location.pathname.split('/').pop() || 'index.html';
        
        container.innerHTML = `
            <nav class="navbar">
                <div class="logo">
                    <a href="/index.html">MedCore</a>
                </div>
                <ul class="nav-links">
                    <li><a href="/index.html">Home</a></li>
                    <li><a href="/pages/products/products.html">Products</a></li>
                    <li><a href="/pages/contact/contact.html">Contact</a></li>
                </ul>
                <div class="search-bar">
                    <input type="text" placeholder="Search medical devices..." id="searchInput">
                    <button id="searchBtn"><i class="fas fa-search"></i></button>
                </div>
                <div class="user-actions">
                    <div class="account-dropdown-container">
                        <a href="#" class="account-dropdown-trigger">
                            <i class="fas fa-user"></i> My Account 
                            <i class="fas fa-chevron-down dropdown-arrow"></i>
                        </a>
                        <div class="account-dropdown-menu" id="accountMenu">
                            <a href="/pages/customer/customer.html">Customer</a>
                            <a href="/pages/distributor/distributor.html">Distributor</a>
                            <hr>
                            <a href="/pages/products/products.html">Continue as Guest</a>
                        </div>
                    </div>
                    <a href="/pages/cart/cart.html" class="cart-icon">
                        <i class="fas fa-shopping-cart"></i> Cart (<span id="cart-count">0</span>)
                    </a>
                </div>
            </nav>
        `;
    },

    attachEventListeners() {
        // Dropdown toggle
        const dropdownTrigger = document.querySelector('.account-dropdown-trigger');
        const dropdownMenu = document.getElementById('accountMenu');
        const dropdownArrow = document.querySelector('.dropdown-arrow');
        
        if (dropdownTrigger && dropdownMenu) {
            dropdownTrigger.addEventListener('click', (e) => {
                e.preventDefault();
                this.toggleDropdown(dropdownMenu, dropdownArrow);
            });

            // Close on outside click
            document.addEventListener('click', (e) => {
                if (!e.target.closest('.account-dropdown-container')) {
                    dropdownMenu.classList.remove('show');
                    if (dropdownArrow) {
                        dropdownArrow.style.transform = 'rotate(0deg)';
                    }
                }
            });
        }

        // Search functionality
        const searchBtn = document.getElementById('searchBtn');
        const searchInput = document.getElementById('searchInput');
        
        if (searchBtn && searchInput) {
            searchBtn.addEventListener('click', () => this.handleSearch(searchInput.value));
            searchInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.handleSearch(searchInput.value);
                }
            });
        }
    },

    toggleDropdown(menu, arrow) {
        menu.classList.toggle('show');
        if (arrow) {
            arrow.style.transform = menu.classList.contains('show') 
                ? 'rotate(180deg)' 
                : 'rotate(0deg)';
        }
    },

    handleSearch(query) {
        if (query.trim()) {
            console.log('Searching for:', query);
            // Implement search functionality here
            window.location.href = `/pages/products/products.html?search=${encodeURIComponent(query)}`;
        }
    }
};

/* ===================================
   2. FOOTER COMPONENT
   =================================== */
const Footer = {
    init() {
        const footer = document.querySelector('footer');
        if (!footer || footer.querySelector('.footer-content')) return;
        
        this.render(footer);
    },

    render(container) {
        container.innerHTML = `
            <div class="footer-content">
                <div class="footer-section about">
                    <h3>About MedCore</h3>
                    <p>MedCore is your trusted partner for high-quality medical devices, committed to supporting healthcare professionals globally.</p>
                </div>
                <div class="footer-section links">
                    <h3>Quick Links</h3>
                    <ul>
                        <li><a href="/pages/products/products.html">Browse Products</a></li>
                        <li><a href="/pages/account/account.html">My Account</a></li>
                        <li><a href="/pages/cart/cart.html">View Cart</a></li>
                    </ul>
                </div>
                <div class="footer-section contact">
                    <h3>Contact Us</h3>
                    <p><i class="fas fa-envelope"></i> Code&Tea@gmail.com</p>
                    <p><i class="fas fa-phone"></i> +964 0770 743 1234</p>
                </div>
            </div>
            <div class="footer-bottom">
                &copy; 2025 MedCore. All rights reserved.
            </div>
        `;
    }
};

/* ===================================
   3. CAROUSEL COMPONENT
   =================================== */
const Carousel = {
    currentIndex: 0,
    visibleSlides: 4,
    autoSlideInterval: null,

products: [
    {
        id: 1,
        name: "Portable Oxygen Cylinder Tank",
        price: "$210",
        rating: 4.4,
        image: "/front/assets/images/oxygen.cylinder.jpg",  // Changed path
        link: "/front/products/product-detail4.html"
    },
    {
        id: 2,
        name: "Blood Pressure Monitor",
        price: "$55.54",
        rating: 5.0,
        image: "/front/assets/images/bloodpressure.jpg",  // Changed path
        link: "/front/products/product-detail3.html"
    },
    {
        id: 3,
        name: "Gun Infrared Thermometer",
        price: "$49.55",
        rating: 3.0,
        image: "/front/assets/images/thermometer.jpg",  // Changed path
        link: "/front/products/product-detail2.html"
    },
    {
        id: 4,
        name: "Professional First Aid Kit",
        price: "$55.99",
        rating: 4.8,
        image: "/front/assets/images/first.aid.jpg",  // Changed path
        link: "#"
    },
    {
        id: 5,
        name: "Compact Portable Ultrasound",
        price: "$450",
        rating: 4.1,
        image: "/front/assets/images/ultrasound.png",  // Changed path
        link: "#"
    },
    {
        id: 6,
        name: "Box of 50 N95 Respirator Masks",
        price: "$15",
        rating: 5.0,
        image: "/front/assets/images/mask.webp",  // Changed path
        link: "#"
    }
],

    init() {
        const container = document.getElementById('carouselTrack');
        if (!container) return;
        
        this.render();
        this.attachEventListeners();
        this.startAutoSlide();
    },

    render() {
        const carouselContainer = document.querySelector('.carousel-container');
        if (!carouselContainer) return;

        let html = `
            <button class="carousel-btn prev" id="carouselPrev">
                <i class="fas fa-chevron-left"></i>
            </button>
            <div class="carousel-track" id="carouselTrack">
        `;

        this.products.forEach((product) => {
            html += `
                <a href="${product.link}" class="product-card slide">
                    <img src="${product.image}" alt="${product.name}">
                    <h3>${product.name}</h3>
                    <p class="price">${product.price}</p>
                    <div class="rating">${this.renderStars(product.rating)}</div>
                    <button class="btn-secondary">View Details</button>
                </a>
            `;
        });

        html += `
            </div>
            <button class="carousel-btn next" id="carouselNext">
                <i class="fas fa-chevron-right"></i>
            </button>
        `;

        carouselContainer.innerHTML = html;
    },

    renderStars(rating) {
        let stars = '';
        for (let i = 1; i <= 5; i++) {
            if (i <= Math.floor(rating)) {
                stars += '<i class="fas fa-star"></i>';
            } else if (i === Math.ceil(rating) && rating % 1 !== 0) {
                stars += '<i class="fas fa-star-half-alt"></i>';
            } else {
                stars += '<i class="far fa-star"></i>';
            }
        }
        return `${stars} (${rating})`;
    },

    attachEventListeners() {
        const prevBtn = document.getElementById('carouselPrev');
        const nextBtn = document.getElementById('carouselNext');
        const track = document.getElementById('carouselTrack');

        if (prevBtn) {
            prevBtn.addEventListener('click', () => this.slide(-1));
        }
        
        if (nextBtn) {
            nextBtn.addEventListener('click', () => this.slide(1));
        }

        // Pause on hover
        if (track) {
            track.addEventListener('mouseenter', () => this.stopAutoSlide());
            track.addEventListener('mouseleave', () => this.startAutoSlide());
        }
    },

    slide(direction) {
        const totalSlides = this.products.length;
        this.currentIndex += direction;

        if (this.currentIndex > totalSlides - this.visibleSlides) {
            this.currentIndex = 0;
        } else if (this.currentIndex < 0) {
            this.currentIndex = totalSlides - this.visibleSlides;
        }

        this.updatePosition();
    },

    updatePosition() {
        const track = document.getElementById('carouselTrack');
        const slides = track?.querySelectorAll('.slide');
        
        if (!slides || slides.length === 0) return;

        const slideWidth = slides[0].offsetWidth + 30; // 30px gap
        const offset = this.currentIndex * slideWidth;
        
        track.style.transform = `translateX(-${offset}px)`;
    },

    startAutoSlide() {
        this.stopAutoSlide();
        this.autoSlideInterval = setInterval(() => this.slide(1), 5000);
    },

    stopAutoSlide() {
        if (this.autoSlideInterval) {
            clearInterval(this.autoSlideInterval);
            this.autoSlideInterval = null;
        }
    }
};

/* ===================================
   4. AUTHENTICATION FORMS
   =================================== */
const AuthForms = {
    init() {
        const loginForm = document.getElementById('login-form');
        const signupForm = document.getElementById('signup-form');

        if (loginForm || signupForm) {
            this.attachEventListeners();
            this.initializeRoleSelectors();
        }
    },

    attachEventListeners() {
        // Tab switching
        const tabButtons = document.querySelectorAll('.tab-button');
        tabButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                const tabName = e.target.textContent.toLowerCase().includes('log in') ? 'login' : 'signup';
                this.showTab(tabName);
            });
        });

        // Form submissions
        const loginForm = document.getElementById('login-form');
        const signupForm = document.getElementById('signup-form');

        if (loginForm) {
            loginForm.addEventListener('submit', (e) => this.handleLogin(e));
        }

        if (signupForm) {
            signupForm.addEventListener('submit', (e) => this.handleSignup(e));
        }
    },

    showTab(tabName) {
        const tabs = document.querySelectorAll('.tab-button');
        const forms = document.querySelectorAll('.auth-form');

        tabs.forEach(tab => tab.classList.remove('active'));
        forms.forEach(form => form.classList.remove('active'));

        const activeTab = Array.from(tabs).find(tab => 
            tab.textContent.toLowerCase().includes(tabName)
        );
        
        if (activeTab) activeTab.classList.add('active');

        const activeForm = document.getElementById(`${tabName}-form`);
        if (activeForm) {
            activeForm.classList.add('active');
            
            // Re-evaluate distributor fields
            const roleInput = activeForm.querySelector(`input[name="${tabName}_role"]:checked`);
            if (roleInput) {
                this.toggleDistributorFields(tabName, roleInput.value === 'distributor');
            }
        }
    },

    initializeRoleSelectors() {
        // Initialize login form
        const loginRoles = document.querySelectorAll('input[name="login_role"]');
        loginRoles.forEach(radio => {
            radio.addEventListener('change', (e) => {
                this.toggleDistributorFields('login', e.target.value === 'distributor');
            });
        });

        // Initialize signup form
        const signupRoles = document.querySelectorAll('input[name="signup_role"]');
        signupRoles.forEach(radio => {
            radio.addEventListener('change', (e) => {
                this.toggleDistributorFields('signup', e.target.value === 'distributor');
            });
        });

        // Set initial state
        const loginChecked = document.querySelector('input[name="login_role"]:checked');
        if (loginChecked) {
            this.toggleDistributorFields('login', loginChecked.value === 'distributor');
        }

        const signupChecked = document.querySelector('input[name="signup_role"]:checked');
        if (signupChecked) {
            this.toggleDistributorFields('signup', signupChecked.value === 'distributor');
        }
    },

    toggleDistributorFields(formPrefix, isDistributor) {
        const fieldsDiv = document.getElementById(`${formPrefix}-distributor-fields`);
        if (!fieldsDiv) return;

        const inputs = fieldsDiv.querySelectorAll('input');

        if (isDistributor) {
            fieldsDiv.classList.add('active');
            inputs.forEach(input => input.required = true);
        } else {
            fieldsDiv.classList.remove('active');
            inputs.forEach(input => input.required = false);
        }
    },

    handleLogin(e) {
        e.preventDefault();
        const email = document.getElementById('login-email')?.value;
        const password = document.getElementById('login-password')?.value;
        const role = document.querySelector('input[name="login_role"]:checked')?.value;

        console.log('Login attempt:', { email, role });
        
        // Implement actual login logic here
        alert('Login functionality would be implemented here');
    },

    handleSignup(e) {
        e.preventDefault();
        const name = document.getElementById('signup-name')?.value;
        const email = document.getElementById('signup-email')?.value;
        const password = document.getElementById('signup-password')?.value;
        const confirmPassword = document.getElementById('signup-confirm-password')?.value;
        const role = document.querySelector('input[name="signup_role"]:checked')?.value;

        if (password !== confirmPassword) {
            alert('Passwords do not match!');
            return;
        }

        console.log('Signup attempt:', { name, email, role });
        
        // Implement actual signup logic here
        alert('Signup functionality would be implemented here');
    }
};

/* ===================================
   5. DROPDOWN HANDLERS (Global)
   =================================== */
window.toggleDropdown = function() {
    const menu = document.getElementById('accountMenu');
    const arrow = document.querySelector('.dropdown-arrow');
    
    if (menu) {
        menu.classList.toggle('show');
        
        if (arrow) {
            arrow.style.transform = menu.classList.contains('show') 
                ? 'rotate(180deg)' 
                : 'rotate(0deg)';
        }
    }
};

/* ===================================
   6. UTILITY FUNCTIONS
   =================================== */
const Utils = {
    // Update cart count
    updateCartCount(count) {
        const cartCountElement = document.getElementById('cart-count');
        if (cartCountElement) {
            cartCountElement.textContent = count;
        }
    },

    // Format price
    formatPrice(price) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(price);
    },

    // Show notification
    showNotification(message, type = 'info') {
        // Simple notification system
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            background: ${type === 'success' ? '#28a745' : '#dc3545'};
            color: white;
            border-radius: 5px;
            z-index: 10000;
            animation: slideIn 0.3s ease;
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }
};

/* ===================================
   7. INITIALIZATION
   =================================== */
document.addEventListener('DOMContentLoaded', () => {
    // Initialize components based on page content
    Navigation.init();
    Footer.init();
    
    // Initialize carousel if it exists
    if (document.getElementById('carouselTrack')) {
        Carousel.init();
    }
    
    // Initialize auth forms if they exist
    if (document.querySelector('.auth-form')) {
        AuthForms.init();
    }

    // Window resize handler for carousel
    let resizeTimeout;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(() => {
            if (Carousel.currentIndex !== undefined) {
                Carousel.updatePosition();
            }
        }, 250);
    });
});

// Export for potential module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { Navigation, Footer, Carousel, AuthForms, Utils };
}