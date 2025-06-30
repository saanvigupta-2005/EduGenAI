// Main JavaScript file for AI Educational Content Generator

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the application
    initializeApp();
});

function initializeApp() {
    // Set up form validation
    setupFormValidation();
    
    // Set up loading states
    setupLoadingStates();
    
    // Set up accessibility features
    setupAccessibility();
    
    // Set up print functionality
    setupPrintFunctionality();
}

function setupFormValidation() {
    const courseForm = document.getElementById('courseForm');
    const courseTitleInput = document.getElementById('course_title');
    const generateBtn = document.getElementById('generateBtn');
    
    if (!courseForm || !courseTitleInput || !generateBtn) {
        return;
    }
    
    // Real-time validation
    courseTitleInput.addEventListener('input', function(e) {
        const value = e.target.value.trim();
        const isValid = value.length >= 3 && value.length <= 200;
        
        // Update button state
        generateBtn.disabled = !isValid;
        
        // Update input styling
        if (value.length > 0) {
            if (isValid) {
                courseTitleInput.classList.remove('is-invalid');
                courseTitleInput.classList.add('is-valid');
            } else {
                courseTitleInput.classList.remove('is-valid');
                courseTitleInput.classList.add('is-invalid');
            }
        } else {
            courseTitleInput.classList.remove('is-valid', 'is-invalid');
        }
        
        // Update character counter
        updateCharacterCounter(value.length);
    });
    
    // Form submission handling
    courseForm.addEventListener('submit', function(e) {
        const courseTitleValue = courseTitleInput.value.trim();
        
        // Final validation
        if (courseTitleValue.length < 3) {
            e.preventDefault();
            showError('Course title must be at least 3 characters long.');
            return;
        }
        
        if (courseTitleValue.length > 200) {
            e.preventDefault();
            showError('Course title must be less than 200 characters.');
            return;
        }
        
        // Show loading state
        showLoadingState();
    });
}

function setupLoadingStates() {
    const courseForm = document.getElementById('courseForm');
    
    if (!courseForm) return;
    
    courseForm.addEventListener('submit', function() {
        const loadingState = document.getElementById('loadingState');
        const generateBtn = document.getElementById('generateBtn');
        
        if (loadingState && generateBtn) {
            // Show loading state
            loadingState.style.display = 'block';
            generateBtn.disabled = true;
            generateBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Generating...';
            
            // Scroll to loading state
            setTimeout(() => {
                loadingState.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }, 100);
        }
    });
}

function setupAccessibility() {
    // Add keyboard navigation support
    document.addEventListener('keydown', function(e) {
        // Escape key to close alerts
        if (e.key === 'Escape') {
            const alerts = document.querySelectorAll('.alert .btn-close');
            alerts.forEach(alert => alert.click());
        }
        
        // Enter key to submit form when focused on course title input
        if (e.key === 'Enter' && e.target.id === 'course_title') {
            const generateBtn = document.getElementById('generateBtn');
            if (generateBtn && !generateBtn.disabled) {
                generateBtn.click();
            }
        }
    });
    
    // Add focus indicators for better accessibility
    const focusableElements = document.querySelectorAll('button, input, a, [tabindex]:not([tabindex="-1"])');
    focusableElements.forEach(element => {
        element.addEventListener('focus', function() {
            this.style.outline = '2px solid #007bff';
            this.style.outlineOffset = '2px';
        });
        
        element.addEventListener('blur', function() {
            this.style.outline = '';
            this.style.outlineOffset = '';
        });
    });
}

function setupPrintFunctionality() {
    // Handle print button clicks
    const printButtons = document.querySelectorAll('[onclick*="print"]');
    printButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            window.print();
        });
    });
    
    // Optimize print layout
    window.addEventListener('beforeprint', function() {
        document.body.classList.add('printing');
    });
    
    window.addEventListener('afterprint', function() {
        document.body.classList.remove('printing');
    });
}

function updateCharacterCounter(length) {
    let counter = document.getElementById('characterCounter');
    
    if (!counter) {
        counter = document.createElement('div');
        counter.id = 'characterCounter';
        counter.className = 'form-text mt-1';
        
        const courseTitleInput = document.getElementById('course_title');
        if (courseTitleInput && courseTitleInput.parentNode) {
            courseTitleInput.parentNode.appendChild(counter);
        }
    }
    
    const remaining = 200 - length;
    counter.innerHTML = `<i class="fas fa-info-circle me-1"></i>${length}/200 characters`;
    
    if (remaining < 20) {
        counter.classList.add('text-warning');
        counter.classList.remove('text-muted');
    } else {
        counter.classList.add('text-muted');
        counter.classList.remove('text-warning');
    }
}

function showLoadingState() {
    const loadingState = document.getElementById('loadingState');
    const generateBtn = document.getElementById('generateBtn');
    
    if (loadingState) {
        loadingState.style.display = 'block';
        loadingState.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
    
    if (generateBtn) {
        generateBtn.disabled = true;
        generateBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Generating...';
    }
}

function showError(message) {
    // Create error alert
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-danger alert-dismissible fade show';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    // Insert alert at the top of the container
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }
}

function showSuccess(message) {
    // Create success alert
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-success alert-dismissible fade show';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    // Insert alert at the top of the container
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }
}

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Export functions for testing (if needed)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        initializeApp,
        setupFormValidation,
        setupLoadingStates,
        setupAccessibility,
        showError,
        showSuccess,
        debounce,
        throttle
    };
}
