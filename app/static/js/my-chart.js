function drawCateChart(labels, data) {
    const ctx = document.getElementById('cateChart');

    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                label: 'Số lượng',
                data: data,
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function drawRevenueChart(labels, data) {
    const ctx = document.getElementById('cateChart');

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Số lượng',
                data: data,
                borderWidth: 1,
                backgroundColor: ['red', 'green', 'blue', 'rgba(144, 180, 90, 0.8)', 'rgba(255, 180, 90, 0.8)']
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}