// Main JavaScript for Harkrishan Gallery and Services

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Auto-dismiss alerts after 5 seconds
    var alerts = document.querySelectorAll('.alert-dismissible');
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
    
    // Auto-format phone numbers
    var phoneInputs = document.querySelectorAll('input[type="tel"]');
    phoneInputs.forEach(function(input) {
        input.addEventListener('input', function(e) {
            var x = e.target.value.replace(/\D/g, '').match(/(\d{0,3})(\d{0,3})(\d{0,4})/);
            e.target.value = !x[2] ? x[1] : '(' + x[1] + ') ' + x[2] + (x[3] ? '-' + x[3] : '');
        });
    });
    
    // Auto-format currency inputs
    var currencyInputs = document.querySelectorAll('.currency-input');
    currencyInputs.forEach(function(input) {
        input.addEventListener('input', function(e) {
            // Remove all non-digit characters
            let value = e.target.value.replace(/[^\d.]/g, '');
            
            // Ensure only one decimal point
            let parts = value.split('.');
            if (parts.length > 2) {
                value = parts[0] + '.' + parts.slice(1).join('');
            }
            
            // Format as currency
            if (value) {
                let num = parseFloat(value);
                if (!isNaN(num)) {
                    e.target.value = num.toLocaleString('en-IN', {
                        maximumFractionDigits: 2,
                        minimumFractionDigits: 2
                    });
                    return;
                }
            }
            
            e.target.value = value;
        });
    });
    
    // Auto-submit forms when pressing Enter in search fields
    var searchForms = document.querySelectorAll('.search-form');
    searchForms.forEach(function(form) {
        var input = form.querySelector('input[type="search"]');
        if (input) {
            input.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    form.submit();
                }
            });
        }
    });
    
    // Initialize datepickers
    var dateInputs = document.querySelectorAll('.datepicker');
    dateInputs.forEach(function(input) {
        // You can initialize a datepicker library here if needed
        // For example, if using flatpickr:
        // flatpickr(input, {
        //     dateFormat: "Y-m-d",
        //     allowInput: true
        // });
    });
    
    // Toggle password visibility
    var togglePasswordBtns = document.querySelectorAll('.toggle-password');
    togglePasswordBtns.forEach(function(btn) {
        btn.addEventListener('click', function() {
            var input = document.querySelector(btn.getAttribute('toggle'));
            if (input) {
                var type = input.getAttribute('type') === 'password' ? 'text' : 'password';
                input.setAttribute('type', type);
                
                // Toggle icon
                var icon = btn.querySelector('i');
                if (icon) {
                    icon.classList.toggle('bi-eye');
                    icon.classList.toggle('bi-eye-slash');
                }
            }
        });
    });
    
    // Handle file upload preview
    var fileInputs = document.querySelectorAll('.custom-file-input');
    fileInputs.forEach(function(input) {
        input.addEventListener('change', function(e) {
            var fileName = e.target.files[0] ? e.target.files[0].name : 'Choose file';
            var nextElement = input.nextElementSibling;
            if (nextElement && nextElement.classList.contains('custom-file-label')) {
                nextElement.textContent = fileName;
            }
            
            // If there's a preview element, show the image
            var previewId = input.getAttribute('data-preview');
            if (previewId && e.target.files && e.target.files[0]) {
                var reader = new FileReader();
                var preview = document.getElementById(previewId);
                
                reader.onload = function(e) {
                    preview.src = e.target.result;
                    preview.style.display = 'block';
                }
                
                reader.readAsDataURL(e.target.files[0]);
            }
        });
    });
    
    // Initialize data tables if DataTables is included
    if (typeof $.fn.DataTable === 'function') {
        $('.datatable').DataTable({
            responsive: true,
            pageLength: 25,
            order: [[0, 'desc']],
            language: {
                search: "_INPUT_",
                searchPlaceholder: "Search...",
                lengthMenu: "Show _MENU_ entries",
                info: "Showing _START_ to _END_ of _TOTAL_ entries",
                infoEmpty: "No entries found",
                infoFiltered: "(filtered from _MAX_ total entries)",
                paginate: {
                    first: "First",
                    last: "Last",
                    next: "Next",
                    previous: "Previous"
                }
            }
        });
    }
    
    // Handle print buttons
    var printButtons = document.querySelectorAll('.btn-print');
    printButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            window.print();
        });
    });
    
    // Handle back to top button
    var backToTopButton = document.querySelector('.back-to-top');
    if (backToTopButton) {
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                backToTopButton.classList.add('show');
            } else {
                backToTopButton.classList.remove('show');
            }
        });
        
        backToTopButton.addEventListener('click', function(e) {
            e.preventDefault();
            window.scrollTo({top: 0, behavior: 'smooth'});
        });
    }
    
    // Handle confirm dialogs for delete actions
    var deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });
    
    // Initialize any charts if Chart.js is included
    if (typeof Chart !== 'undefined') {
        var chartElements = document.querySelectorAll('.chart');
        chartElements.forEach(function(chartElement) {
            var ctx = chartElement.getContext('2d');
            var chartType = chartElement.dataset.chartType || 'bar';
            var chartData = JSON.parse(chartElement.dataset.chartData || '{}');
            var chartOptions = JSON.parse(chartElement.dataset.chartOptions || '{}');
            
            new Chart(ctx, {
                type: chartType,
                data: chartData,
                options: chartOptions
            });
        });
    }
});

// Utility function to format dates
function formatDate(dateString) {
    if (!dateString) return '';
    
    const options = { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    
    return new Date(dateString).toLocaleDateString('en-US', options);
}

// Utility function to format currency
function formatCurrency(amount) {
    if (amount === null || amount === undefined) return '₹0.00';
    
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR',
        minimumFractionDigits: 2
    }).format(amount);
}

// Export functions to global scope if needed
window.HGS = window.HGS || {};
window.HGS.formatDate = formatDate;
window.HGS.formatCurrency = formatCurrency;
