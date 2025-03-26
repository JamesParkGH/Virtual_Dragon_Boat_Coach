document.addEventListener('DOMContentLoaded', function() {
    // Initialize components
    initializeFeedbackComponents();
    initializeProcessForm();
});

function initializeFeedbackComponents() {
    const feedbackForm = document.getElementById('feedbackForm');
    if (feedbackForm) {
        feedbackForm.addEventListener('submit', generateGraph);
        
        // Clear graph when leaving the page
        window.addEventListener('beforeunload', function() {
            const graphContainer = document.getElementById('graph-container');
            if (graphContainer) {
                graphContainer.style.display = 'none';
            }
        });
    }
}

function initializeProcessForm() {
    const processForm = document.getElementById('processForm');
    if (processForm) {
        processForm.addEventListener('submit', function() {
            const loadingMessage = document.getElementById('loadingMessage');
            if (loadingMessage) {
                loadingMessage.style.display = 'block';
                
                animateProcessingSteps();
            }
            
            const submitBtn = processForm.querySelector('button[type="submit"]');
            if (submitBtn) {
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin loading-indicator"></i> Processing...';
                submitBtn.disabled = true;
                submitBtn.classList.add('processing');
                
                setTimeout(function() {
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                    submitBtn.classList.remove('processing');
                }, 30000); 
            }
        });
    }
}

function animateProcessingSteps() {
    const steps = document.querySelectorAll('.loading-steps .step');
    if (!steps.length) return;
    
    steps.forEach(step => step.classList.remove('active'));
    steps[0].classList.add('active');
    setTimeout(() => {
        steps[0].classList.remove('active');
        steps[1].classList.add('active');
    }, 5000);

    setTimeout(() => {
        steps[1].classList.remove('active'); 
        steps[2].classList.add('active');
        
        const progressBarFill = document.querySelector('.progress-bar-fill');
        const progressPaddle = document.querySelector('.progress-paddle');
        
        if (progressBarFill) {
            progressBarFill.style.animation = 'none';
            progressBarFill.style.width = '100%';
        }
        
        if (progressPaddle) {
            progressPaddle.style.animation = 'none';
            progressPaddle.style.left = 'calc(100% - 15px)';
        }
    }, 10000);
}

/**
 * @param {Event} event - form submission event
 */
function generateGraph(event) {
    event.preventDefault();
    
    const formData = new FormData(document.getElementById('feedbackForm'));
    const submitButton = event.submitter;
    const originalButtonText = submitButton.innerHTML;
    
    submitButton.innerHTML = '<i class="fas fa-spinner fa-spin loading-indicator"></i> Generating...';
    submitButton.disabled = true;
    submitButton.classList.add('processing');
    
    // Clear previous graph
    const graphContainer = document.getElementById('graph-container');
    if (graphContainer) {
        graphContainer.style.display = 'none';
    }
    
    fetch('/generate-graph', {
        method: 'POST',
        body: formData,
        credentials: 'same-origin'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        submitButton.innerHTML = originalButtonText;
        submitButton.disabled = false;
        submitButton.classList.remove('processing');
        
        if (data.success) {
            const graphImage = document.getElementById('graph-image');
            const timestamp = new Date().getTime();
            
            graphImage.onload = function() {
                if (graphContainer) {
                    graphContainer.style.display = 'block';
                    
                    graphContainer.scrollIntoView({ 
                        behavior: 'smooth', 
                        block: 'start' 
                    });
                }
            };
            
            graphImage.src = data.graph_url + '?t=' + timestamp;
            
            const graphTitle = document.getElementById('graph-title');
            if (graphTitle) {
                graphTitle.textContent = `${data.angle_name} Analysis`;
            }
        } else {
            alert(data.error || 'Failed to generate graph');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        submitButton.innerHTML = originalButtonText;
        submitButton.disabled = false;
        submitButton.classList.remove('processing');
        alert('An error occurred while generating the graph. Please try again.');
    });
}