/* UrbanPulse JavaScript for interactive features */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl)
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Add active class to current nav item based on URL
    const currentLocation = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navLinks.forEach(link => {
        const linkPath = link.getAttribute('href');
        if (linkPath && currentLocation.includes(linkPath) && linkPath !== '/') {
            link.classList.add('active');
        } else if (currentLocation === '/' && linkPath === '/') {
            link.classList.add('active');
        }
    });

    // Data visualization initialization (placeholder for chart.js or other libraries)
    const chartElements = document.querySelectorAll('.chart-container');
    if (chartElements.length > 0) {
        initializeCharts();
    }

    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Mobile menu toggle behavior enhancement
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
        document.addEventListener('click', function(event) {
            const isClickInside = navbarToggler.contains(event.target) || navbarCollapse.contains(event.target);
            
            if (!isClickInside && navbarCollapse.classList.contains('show')) {
                navbarToggler.click();
            }
        });
    }

    // Back to top button
    const backToTopButton = document.getElementById('back-to-top');
    if (backToTopButton) {
        window.addEventListener('scroll', () => {
            if (window.pageYOffset > 300) {
                backToTopButton.classList.add('show');
            } else {
                backToTopButton.classList.remove('show');
            }
        });
        
        backToTopButton.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
});

// Function to initialize charts (placeholder)
function initializeCharts() {
    // This would be replaced with actual chart initialization code
    console.log('Charts would be initialized here with real data');
    
    // Example of what might be included for a real implementation:
    /*
    const demographicsChart = document.getElementById('demographics-chart');
    if (demographicsChart) {
        new Chart(demographicsChart, {
            type: 'bar',
            data: {
                labels: ['0-18', '19-35', '36-50', '51-65', '65+'],
                datasets: [{
                    label: 'Age Distribution',
                    data: [15, 30, 25, 18, 12],
                    backgroundColor: [
                        'rgba(54, 162, 235, 0.5)',
                        'rgba(75, 192, 192, 0.5)',
                        'rgba(255, 206, 86, 0.5)',
                        'rgba(255, 159, 64, 0.5)',
                        'rgba(153, 102, 255, 0.5)'
                    ],
                    borderColor: [
                        'rgba(54, 162, 235, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(255, 159, 64, 1)',
                        'rgba(153, 102, 255, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Percentage'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Age Group'
                        }
                    }
                }
            }
        });
    }
    */
}

// Function for investment opportunity filtering (placeholder)
function filterInvestmentOpportunities(filters) {
    // This would be replaced with actual filtering logic
    console.log('Filtering investment opportunities with:', filters);
    
    // In a real implementation, this might make an AJAX call to the server
    // or filter client-side data and update the DOM
}

// Function for hazard risk assessment (placeholder)
function calculateHazardRisk(location, factors) {
    // This would be replaced with actual risk calculation logic
    console.log('Calculating hazard risk for:', location, 'with factors:', factors);
    
    // In a real implementation, this might make an AJAX call to the server
    // or perform calculations based on pre-loaded data
}

// Function to handle contact form submission via AJAX (placeholder)
function submitContactForm(formData) {
    // This would be replaced with actual form submission logic
    console.log('Submitting contact form with data:', formData);
    
    // Example of what might be included for a real implementation:
    /*
    fetch('/contact/submit/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showSuccessMessage('Your message has been sent successfully!');
            resetForm();
        } else {
            showErrorMessage('There was an error sending your message. Please try again.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showErrorMessage('There was an error sending your message. Please try again.');
    });
    */
}

// Helper function to get CSRF token from cookies (for Django form submissions)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Helper functions for showing success/error messages
function showSuccessMessage(message) {
    const alertContainer = document.getElementById('alert-container');
    if (alertContainer) {
        alertContainer.innerHTML = `
            <div class="alert alert-success alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        `;
    }
}

function showErrorMessage(message) {
    const alertContainer = document.getElementById('alert-container');
    if (alertContainer) {
        alertContainer.innerHTML = `
            <div class="alert alert-danger alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        `;
    }
}

// Responsive behavior enhancements
window.addEventListener('resize', function() {
    // Adjust UI elements based on screen size if needed
    const width = window.innerWidth;
    
    // Example of responsive behavior adjustment
    const dataCards = document.querySelectorAll('.data-card');
    if (dataCards.length > 0) {
        if (width < 768) {
            dataCards.forEach(card => {
                card.classList.add('compact-view');
            });
        } else {
            dataCards.forEach(card => {
                card.classList.remove('compact-view');
            });
        }
    }
});
