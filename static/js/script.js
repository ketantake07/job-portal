// Job Portal JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
});

// Function to set apply form action
function setApplyForm(jobId) {
    const form = document.getElementById('applyForm');
    if (form) {
        form.action = '/apply/' + jobId;
    }
}

// Function to copy job description
function copyJobDescription() {
    const url = document.querySelector('input[name="company_url"]').value;
    if (!url) {
        alert('Please enter the company job post URL first');
        return;
    }
    
    // Placeholder for job description copying functionality
    const description = prompt('Paste the job description from the company website:');
    if (description) {
        document.querySelector('textarea[name="description"]').value = description;
    }
}

// Function to show cover letter in modal
function showCoverLetter(content) {
    const modalContent = document.getElementById('coverLetterContent');
    if (modalContent) {
        modalContent.innerHTML = content.replace(/\n/g, '<br>');
        const modal = new bootstrap.Modal(document.getElementById('coverLetterModal'));
        modal.show();
    }
}

// Function to view application details
function viewApplication(applicationId) {
    // In a real application, you would fetch application details via AJAX
    const modal = new bootstrap.Modal(document.getElementById('applicationModal'));
    modal.show();
}

// Search functionality (if needed)
function searchJobs(query) {
    const jobCards = document.querySelectorAll('.card');
    jobCards.forEach(function(card) {
        const title = card.querySelector('.card-title').textContent.toLowerCase();
        const company = card.querySelector('.card-subtitle').textContent.toLowerCase();
        const description = card.querySelector('.card-text').textContent.toLowerCase();
        
        if (title.includes(query.toLowerCase()) || 
            company.includes(query.toLowerCase()) || 
            description.includes(query.toLowerCase())) {
            card.parentElement.style.display = 'block';
        } else {
            card.parentElement.style.display = 'none';
        }
    });
}