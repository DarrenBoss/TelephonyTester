// Dashboard functionality for the telephony testing application

// Global variables
let callListElement;
let callCountElement;
let callChartInstance;
let lastCallCount = 0;
let callData = [];

// Initialize the dashboard when the DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('Dashboard initializing...');
    
    // Get DOM elements
    callListElement = document.getElementById('active-calls-list');
    callCountElement = document.getElementById('call-count');
    
    // Initialize the call chart
    initializeCallChart();
    
    // Initialize real-time updates
    initializeEventSource();
    
    // Initial data load
    fetchInitialData();
});

// Initialize the call history chart
function initializeCallChart() {
    const ctx = document.getElementById('callHistoryChart').getContext('2d');
    
    callChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Active Calls',
                data: [],
                borderColor: '#3a86ff',
                backgroundColor: 'rgba(58, 134, 255, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4
            }]
        },
        options: callChartOptions  // Defined in chart-config.js
    });
}

// Set up server-sent events for real-time updates
function initializeEventSource() {
    const eventSource = new EventSource('/api/stream');
    
    eventSource.addEventListener('message', function(event) {
        const data = JSON.parse(event.data);
        updateDashboard(data);
    });
    
    eventSource.addEventListener('error', function(error) {
        console.error('EventSource error:', error);
        // Attempt to reconnect after a delay
        setTimeout(() => {
            console.log('Attempting to reconnect EventSource...');
            initializeEventSource();
        }, 5000);
    });
}

// Fetch initial data for the dashboard
function fetchInitialData() {
    // Get active calls
    fetch('/api/calls')
        .then(response => response.json())
        .then(calls => {
            // Get call count
            fetch('/api/call_count')
                .then(response => response.json())
                .then(countData => {
                    // Update dashboard with initial data
                    updateDashboard({
                        calls: calls,
                        count: countData.count,
                        timestamp: new Date().toISOString()
                    });
                })
                .catch(error => console.error('Error fetching call count:', error));
        })
        .catch(error => console.error('Error fetching calls:', error));
}

// Update the dashboard with new data
function updateDashboard(data) {
    // Update call count
    const count = data.count || 0;
    callCountElement.textContent = count;
    
    // Update call count appearance based on capacity
    updateCallCountAppearance(count);
    
    // Update active calls list
    updateCallsList(data.calls || []);
    
    // Update chart with new data point
    updateCallChart(count, data.timestamp);
    
    // Record the last call count
    lastCallCount = count;
}

// Update the calls list in the UI
function updateCallsList(calls) {
    // Clear existing content
    callListElement.innerHTML = '';
    
    if (calls.length === 0) {
        // Show a message when no active calls
        const noCallsMessage = document.createElement('div');
        noCallsMessage.className = 'text-center py-4 text-muted';
        noCallsMessage.innerHTML = '<i class="fas fa-phone-slash me-2"></i>No active calls';
        callListElement.appendChild(noCallsMessage);
        return;
    }
    
    // Sort calls by start time (newest first)
    calls.sort((a, b) => new Date(b.start_time) - new Date(a.start_time));
    
    // Create list items for each call
    calls.forEach(call => {
        const callItem = document.createElement('div');
        callItem.className = 'call-item p-3 mb-2 border rounded';
        callItem.setAttribute('data-call-sid', call.call_sid);
        
        // Format the phone numbers for display
        const fromNumber = formatPhoneNumber(call.from_number);
        const toNumber = formatPhoneNumber(call.to_number);
        
        // Format duration
        const duration = call.duration ? formatDuration(call.duration) : '00:00';
        
        // Determine IVR selection text and icon
        let ivrSelectionText = 'Waiting for selection...';
        let ivrSelectionIcon = '<i class="fas fa-question-circle text-warning"></i>';
        
        if (call.ivr_selection === 'music') {
            ivrSelectionText = 'Playing Music';
            ivrSelectionIcon = '<i class="fas fa-music text-primary"></i>';
        } else if (call.ivr_selection === 'beep') {
            ivrSelectionText = 'Playing Beep (3s)';
            ivrSelectionIcon = '<i class="fas fa-volume-up text-info"></i>';
        }
        
        // Build the call item HTML
        callItem.innerHTML = `
            <div class="d-flex justify-content-between align-items-center">
                <div class="call-info">
                    <div class="call-number mb-1">
                        <i class="fas fa-phone-alt me-2 text-success"></i>
                        <span class="fw-bold">${fromNumber}</span> → ${toNumber}
                    </div>
                    <div class="call-details d-flex align-items-center">
                        <span class="me-3 text-muted small">
                            <i class="far fa-clock me-1"></i>${duration}
                        </span>
                        <span class="ivr-selection small">
                            ${ivrSelectionIcon} ${ivrSelectionText}
                        </span>
                    </div>
                </div>
                <span class="call-sid small text-muted">${call.call_sid.substr(-8)}</span>
            </div>
        `;
        
        callListElement.appendChild(callItem);
    });
}

// Update the call count appearance based on capacity
function updateCallCountAppearance(count) {
    const countElement = document.getElementById('call-count');
    const capacityElement = document.querySelector('.capacity-indicator');
    
    // Remove existing classes
    countElement.classList.remove('text-success', 'text-warning', 'text-danger');
    
    // Add appropriate class based on capacity
    if (count < 10) {
        countElement.classList.add('text-success');
        capacityElement.textContent = 'Low Load';
        capacityElement.className = 'capacity-indicator badge bg-success';
    } else if (count < 18) {
        countElement.classList.add('text-warning');
        capacityElement.textContent = 'Medium Load';
        capacityElement.className = 'capacity-indicator badge bg-warning';
    } else {
        countElement.classList.add('text-danger');
        capacityElement.textContent = 'High Load';
        capacityElement.className = 'capacity-indicator badge bg-danger';
    }
}

// Update the call history chart with new data
function updateCallChart(count, timestamp) {
    const label = formatTimestamp(timestamp);
    
    // Add new data point
    callChartInstance.data.labels.push(label);
    callChartInstance.data.datasets[0].data.push(count);
    
    // Keep only the last 20 data points
    if (callChartInstance.data.labels.length > 20) {
        callChartInstance.data.labels.shift();
        callChartInstance.data.datasets[0].data.shift();
    }
    
    // Update chart
    callChartInstance.update();
}

// Format a phone number for display
function formatPhoneNumber(phone) {
    if (!phone || phone === 'unknown') return 'Unknown';
    
    // Remove any non-digit characters
    const cleaned = ('' + phone).replace(/\D/g, '');
    
    // Format based on length
    if (cleaned.length === 10) {
        return `(${cleaned.substring(0, 3)}) ${cleaned.substring(3, 6)}-${cleaned.substring(6, 10)}`;
    } else if (cleaned.length === 11 && cleaned.startsWith('1')) {
        return `+1 (${cleaned.substring(1, 4)}) ${cleaned.substring(4, 7)}-${cleaned.substring(7, 11)}`;
    } else {
        return phone; // Return original if we can't format it
    }
}

// Format a timestamp for chart display
function formatTimestamp(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit', second:'2-digit'});
}

// Format duration in seconds to MM:SS format
function formatDuration(seconds) {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = Math.floor(seconds % 60);
    return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
}
