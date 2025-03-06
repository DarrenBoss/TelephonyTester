// Configuration options for the call history chart

const callChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
        x: {
            grid: {
                display: false
            },
            ticks: {
                maxRotation: 0,
                autoSkip: true,
                maxTicksLimit: 10,
                color: 'rgba(255, 255, 255, 0.7)'
            }
        },
        y: {
            beginAtZero: true,
            max: 20,
            grid: {
                color: 'rgba(255, 255, 255, 0.1)'
            },
            ticks: {
                stepSize: 5,
                color: 'rgba(255, 255, 255, 0.7)'
            },
            title: {
                display: true,
                text: 'Number of Calls',
                color: 'rgba(255, 255, 255, 0.9)'
            }
        }
    },
    plugins: {
        legend: {
            display: false
        },
        tooltip: {
            backgroundColor: 'rgba(0, 0, 0, 0.7)',
            titleColor: '#ffffff',
            bodyColor: '#ffffff',
            borderColor: '#3a86ff',
            borderWidth: 1,
            caretSize: 6,
            caretPadding: 10,
            cornerRadius: 6,
            displayColors: false,
            callbacks: {
                title: function(tooltipItems) {
                    return 'Time: ' + tooltipItems[0].label;
                },
                label: function(context) {
                    return 'Active Calls: ' + context.parsed.y;
                }
            }
        },
        annotation: {
            annotations: {
                line1: {
                    type: 'line',
                    yMin: 20,
                    yMax: 20,
                    borderColor: 'rgba(255, 0, 0, 0.5)',
                    borderWidth: 2,
                    borderDash: [6, 6],
                    label: {
                        enabled: true,
                        content: 'Max Capacity',
                        position: 'end',
                        backgroundColor: 'rgba(255, 0, 0, 0.8)'
                    }
                }
            }
        }
    },
    animation: {
        duration: 800,
        easing: 'easeOutQuart'
    },
    elements: {
        point: {
            radius: 3,
            hoverRadius: 5,
            backgroundColor: '#3a86ff',
            borderWidth: 2,
            borderColor: '#ffffff'
        },
        line: {
            tension: 0.4
        }
    },
    layout: {
        padding: {
            top: 20,
            right: 20,
            bottom: 10,
            left: 10
        }
    },
    interaction: {
        mode: 'index',
        intersect: false
    }
};
