// Global chart instances
let charts = {};

// Load all data when page loads
document.addEventListener('DOMContentLoaded', function() {
    loadOverview();
    loadCharts();
    loadInsights();
    loadTransactions();
    setupNavigation();
});

// Setup smooth navigation
function setupNavigation() {
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            // Update active link
            document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
            this.classList.add('active');
            
            // Smooth scroll
            targetElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
    });
}

// Load overview statistics
async function loadOverview() {
    try {
        const response = await fetch('/api/overview');
        const data = await response.json();
        
        document.getElementById('total-customers').textContent = data.total_customers.toLocaleString();
        document.getElementById('total-revenue').textContent = '$' + data.total_revenue.toLocaleString(undefined, {maximumFractionDigits: 0});
        document.getElementById('avg-purchase').textContent = '$' + data.avg_purchase_amount.toFixed(2);
        document.getElementById('avg-rating').textContent = data.avg_rating.toFixed(2) + '/5.0';
        document.getElementById('subscription-rate').textContent = data.subscription_rate.toFixed(1) + '%';
        document.getElementById('discount-usage').textContent = data.discount_usage.toFixed(1) + '%';
        
        // Animate stat cards
        animateStats();
    } catch (error) {
        console.error('Error loading overview:', error);
    }
}

// Animate stat cards on load
function animateStats() {
    const statCards = document.querySelectorAll('.stat-card');
    statCards.forEach((card, index) => {
        setTimeout(() => {
            card.style.animation = 'fadeInUp 0.6s ease forwards';
        }, index * 100);
    });
}

// Load all charts
async function loadCharts() {
    await loadCategoryChart();
    await loadSeasonalChart();
    await loadAgeChart();
    await loadPaymentChart();
    await loadTopItemsChart();
    await loadClusterChart();
}

// Category Chart
async function loadCategoryChart() {
    try {
        const response = await fetch('/api/purchase_by_category');
        const data = await response.json();
        
        const ctx = document.getElementById('categoryChart').getContext('2d');
        charts.category = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.map(d => d.category),
                datasets: [{
                    label: 'Average Purchase ($)',
                    data: data.map(d => d.avg_purchase),
                    backgroundColor: 'rgba(99, 102, 241, 0.8)',
                    borderColor: 'rgba(99, 102, 241, 1)',
                    borderWidth: 2,
                    borderRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        padding: 12,
                        titleFont: { size: 14, weight: 'bold' },
                        bodyFont: { size: 13 }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: { color: 'rgba(0, 0, 0, 0.05)' }
                    },
                    x: {
                        grid: { display: false }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error loading category chart:', error);
    }
}

// Seasonal Chart
async function loadSeasonalChart() {
    try {
        const response = await fetch('/api/seasonal_trends');
        const data = await response.json();
        
        const ctx = document.getElementById('seasonalChart').getContext('2d');
        charts.seasonal = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.map(d => d.season),
                datasets: [{
                    label: 'Average Purchase ($)',
                    data: data.map(d => d.avg_purchase),
                    borderColor: 'rgba(236, 72, 153, 1)',
                    backgroundColor: 'rgba(236, 72, 153, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 6,
                    pointHoverRadius: 8,
                    pointBackgroundColor: 'rgba(236, 72, 153, 1)'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        padding: 12
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: { color: 'rgba(0, 0, 0, 0.05)' }
                    },
                    x: {
                        grid: { display: false }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error loading seasonal chart:', error);
    }
}

// Age Distribution Chart
async function loadAgeChart() {
    try {
        const response = await fetch('/api/age_distribution');
        const data = await response.json();
        
        const ctx = document.getElementById('ageChart').getContext('2d');
        charts.age = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: data.map(d => d.age_group),
                datasets: [{
                    data: data.map(d => d.count),
                    backgroundColor: [
                        'rgba(99, 102, 241, 0.8)',
                        'rgba(236, 72, 153, 0.8)',
                        'rgba(16, 185, 129, 0.8)',
                        'rgba(245, 158, 11, 0.8)',
                        'rgba(239, 68, 68, 0.8)'
                    ],
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { padding: 15, font: { size: 12 } }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        padding: 12
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error loading age chart:', error);
    }
}

// Payment Methods Chart
async function loadPaymentChart() {
    try {
        const response = await fetch('/api/payment_methods');
        const data = await response.json();
        
        const ctx = document.getElementById('paymentChart').getContext('2d');
        charts.payment = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: data.map(d => d.method),
                datasets: [{
                    data: data.map(d => d.count),
                    backgroundColor: [
                        'rgba(99, 102, 241, 0.8)',
                        'rgba(236, 72, 153, 0.8)',
                        'rgba(16, 185, 129, 0.8)',
                        'rgba(245, 158, 11, 0.8)',
                        'rgba(139, 92, 246, 0.8)',
                        'rgba(59, 130, 246, 0.8)'
                    ],
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { padding: 15, font: { size: 12 } }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        padding: 12
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error loading payment chart:', error);
    }
}

// Top Items Chart
async function loadTopItemsChart() {
    try {
        const response = await fetch('/api/top_items');
        const data = await response.json();
        
        const ctx = document.getElementById('topItemsChart').getContext('2d');
        charts.topItems = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.map(d => d.item),
                datasets: [{
                    label: 'Sales Count',
                    data: data.map(d => d.count),
                    backgroundColor: 'rgba(16, 185, 129, 0.8)',
                    borderColor: 'rgba(16, 185, 129, 1)',
                    borderWidth: 2,
                    borderRadius: 8
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        padding: 12
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        grid: { color: 'rgba(0, 0, 0, 0.05)' }
                    },
                    y: {
                        grid: { display: false }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error loading top items chart:', error);
    }
}

// Cluster Chart
async function loadClusterChart() {
    try {
        const response = await fetch('/api/cluster_data');
        const data = await response.json();
        
        if (data.length === 0) return;
        
        const ctx = document.getElementById('clusterChart').getContext('2d');
        charts.cluster = new Chart(ctx, {
            type: 'bubble',
            data: {
                datasets: data.map((cluster, index) => ({
                    label: `Segment ${cluster.cluster}`,
                    data: [{
                        x: cluster.avg_age,
                        y: cluster.avg_purchase,
                        r: Math.sqrt(cluster.customer_count) / 2
                    }],
                    backgroundColor: [
                        'rgba(99, 102, 241, 0.6)',
                        'rgba(236, 72, 153, 0.6)',
                        'rgba(16, 185, 129, 0.6)',
                        'rgba(245, 158, 11, 0.6)'
                    ][index],
                    borderColor: [
                        'rgba(99, 102, 241, 1)',
                        'rgba(236, 72, 153, 1)',
                        'rgba(16, 185, 129, 1)',
                        'rgba(245, 158, 11, 1)'
                    ][index],
                    borderWidth: 2
                }))
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { padding: 15, font: { size: 12 } }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        padding: 12,
                        callbacks: {
                            label: function(context) {
                                const cluster = data[context.datasetIndex];
                                return [
                                    `Avg Age: ${cluster.avg_age}`,
                                    `Avg Purchase: $${cluster.avg_purchase}`,
                                    `Customers: ${cluster.customer_count}`
                                ];
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        title: { display: true, text: 'Average Age' },
                        grid: { color: 'rgba(0, 0, 0, 0.05)' }
                    },
                    y: {
                        title: { display: true, text: 'Average Purchase ($)' },
                        grid: { color: 'rgba(0, 0, 0, 0.05)' }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error loading cluster chart:', error);
    }
}

// Make prediction
async function makePrediction() {
    const data = {
        age: parseInt(document.getElementById('age').value),
        gender: document.getElementById('gender').value,
        category: document.getElementById('category').value,
        season: document.getElementById('season').value,
        previous_purchases: parseInt(document.getElementById('previous-purchases').value),
        review_rating: parseFloat(document.getElementById('review-rating').value),
        frequency: document.getElementById('frequency').value,
        is_subscriber: document.getElementById('is-subscriber').checked,
        discount_used: document.getElementById('discount-used').checked,
        promo_used: document.getElementById('promo-used').checked
    };
    
    try {
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        // Update prediction results with animation
        document.getElementById('predicted-amount').textContent = '$' + result.predicted_purchase_amount;
        document.getElementById('subscription-prob').textContent = result.subscription_probability + '%';
        document.getElementById('subscription-progress').style.width = result.subscription_probability + '%';
        
        // Add animation
        document.querySelectorAll('.prediction-card').forEach(card => {
            card.style.animation = 'none';
            setTimeout(() => {
                card.style.animation = 'fadeInUp 0.6s ease';
            }, 10);
        });
    } catch (error) {
        console.error('Error making prediction:', error);
        alert('Error making prediction. Please try again.');
    }
}

// Load insights
async function loadInsights() {
    try {
        const response = await fetch('/api/overview');
        const data = await response.json();
        
        // Demographics insights
        const demographics = [
            `Average customer age: ${data.avg_age.toFixed(0)} years`,
            `Male customers: ${data.male_percentage.toFixed(1)}%`,
            `Female customers: ${data.female_percentage.toFixed(1)}%`,
            `Total customer base: ${data.total_customers.toLocaleString()}`
        ];
        document.getElementById('demographics-list').innerHTML = demographics.map(i => `<li>${i}</li>`).join('');
        
        // Revenue insights
        const revenue = [
            `Total revenue: $${data.total_revenue.toLocaleString(undefined, {maximumFractionDigits: 0})}`,
            `Average purchase: $${data.avg_purchase_amount.toFixed(2)}`,
            `Average rating: ${data.avg_rating.toFixed(2)}/5.0`,
            `Customer satisfaction is ${data.avg_rating >= 4 ? 'high' : data.avg_rating >= 3 ? 'moderate' : 'needs improvement'}`
        ];
        document.getElementById('revenue-insights').innerHTML = revenue.map(i => `<li>${i}</li>`).join('');
        
        // Marketing insights
        const marketing = [
            `${data.subscription_rate.toFixed(1)}% subscription rate`,
            `${data.discount_usage.toFixed(1)}% customers use discounts`,
            `${(100 - data.subscription_rate).toFixed(1)}% growth opportunity for subscriptions`,
            `Focus on discount strategies for conversion`
        ];
        document.getElementById('marketing-insights').innerHTML = marketing.map(i => `<li>${i}</li>`).join('');
        
        // Satisfaction insights
        const satisfaction = [
            `Average rating: ${data.avg_rating.toFixed(2)} out of 5.0`,
            `Customer satisfaction is ${data.avg_rating >= 4 ? 'excellent' : 'good'}`,
            `${data.subscription_rate > 25 ? 'Strong' : 'Growing'} customer loyalty`,
            `Positive shopping experience indicated`
        ];
        document.getElementById('satisfaction-insights').innerHTML = satisfaction.map(i => `<li>${i}</li>`).join('');
    } catch (error) {
        console.error('Error loading insights:', error);
    }
}

// Load transactions table
async function loadTransactions() {
    try {
        const response = await fetch('/api/recent_transactions');
        const data = await response.json();
        
        const tbody = document.getElementById('transactions-body');
        tbody.innerHTML = data.slice(0, 20).map(row => `
            <tr>
                <td>${row['Customer ID']}</td>
                <td>${row['Age']}</td>
                <td>${row['Gender']}</td>
                <td>${row['Item Purchased']}</td>
                <td>${row['Category']}</td>
                <td>$${row['Purchase Amount (USD)']}</td>
                <td>${row['Review Rating']}</td>
                <td><span class="badge ${row['Subscription Status'] === 'Yes' ? 'badge-success' : 'badge-secondary'}">${row['Subscription Status']}</span></td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Error loading transactions:', error);
    }
}
