// Global JavaScript for Smart Solution

// Initialize tooltips
document.addEventListener('DOMContentLoaded', function() {
    // Enable Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Enable Bootstrap popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Confirm before deleting
    var deleteButtons = document.querySelectorAll('.delete-confirm');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });
    
    // Auto-hide alerts after 5 seconds
    var alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // Form validation
    var forms = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
    
    // Sidebar entrance animation
    var sidebar = document.getElementById('sidebar');
    if (sidebar && window.innerWidth < 768) {
        // Hide sidebar by default on smaller screens
        sidebar.classList.add('hidden');
    }
    
    // Sidebar toggle functionality with animations
    var sidebarCollapse = document.getElementById('sidebarCollapse');
    
    if (sidebarCollapse && sidebar) {
        sidebarCollapse.addEventListener('click', function() {
            sidebar.classList.toggle('hidden');
            
            // Force reflow to ensure animations work properly
            sidebar.offsetHeight;
            
            // Add ripple effect to the toggle button
            const ripple = document.createElement('span');
            ripple.classList.add('ripple');
            this.appendChild(ripple);
            
            // Remove ripple after animation completes
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    }
    
    // Theme toggle functionality
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        const themeIcon = themeToggle.querySelector('i');
        
        // Check for saved theme preference or respect OS preference
        const savedTheme = localStorage.getItem('theme');
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        const initialTheme = savedTheme || (prefersDark ? 'dark' : 'light');
        
        // Apply initial theme
        document.documentElement.setAttribute('data-theme', initialTheme);
        themeIcon.className = initialTheme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
        
        // Toggle theme on button click
        themeToggle.addEventListener('click', function() {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            themeIcon.className = newTheme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
        });
    }
    
    // Language selector functionality (placeholder for future implementation)
    const languageSelector = document.getElementById('languageSelector');
    if (languageSelector) {
        languageSelector.addEventListener('change', function() {
            const selectedLanguage = this.value;
            // In a real implementation, this would trigger a language change
            // For now, we'll just show an alert
            alert(`Language changed to: ${selectedLanguage}`);
            // Save preference to localStorage
            localStorage.setItem('language', selectedLanguage);
        });
        
        // Set initial language from localStorage
        const savedLanguage = localStorage.getItem('language') || 'en';
        languageSelector.value = savedLanguage;
    }
});

// Function to format currency
function formatCurrency(amount) {
    // Get currency symbol from business settings or default to FRW
    const currencySymbol = typeof business_settings !== 'undefined' && business_settings.currency_symbol 
        ? business_settings.currency_symbol 
        : 'FRW';
    
    // Format as currency with the specified symbol
    return currencySymbol + ' ' + parseFloat(amount).toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
}

// Function to format date
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
}

// Function to change language (placeholder for future implementation)
function changeLanguage(languageCode) {
    // In a real implementation, this would load the appropriate language files
    // and update all text on the page
    localStorage.setItem('language', languageCode);
    location.reload(); // Reload to apply changes
}

// Add CSS for ripple effect
const style = document.createElement('style');
style.innerHTML = `
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.7);
        transform: scale(0);
        animation: ripple 0.6s linear;
        pointer-events: none;
    }
    
    @keyframes ripple {
        to {
            transform: scale(2.5);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);