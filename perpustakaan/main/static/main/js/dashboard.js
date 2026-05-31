const labels = [
    'Total Buku',
    'Total Anggota',
    'Total Peminjaman',
    'Sedang Dipinjam'
];

const dataStatistik = [
    totalBuku,
    totalAnggota,
    totalPeminjaman,
    totalDipinjam
];

const warnaStatistik = [
    '#3498db',
    '#2ecc71',
    '#f1c40f',
    '#e74c3c'
];

new Chart(document.getElementById('barChart'), {
    type: 'bar',
    data: {
        labels: labels,
        datasets: [{
            label: 'Jumlah Data',
            data: dataStatistik,
            backgroundColor: warnaStatistik,
            borderRadius: 8
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: {
                beginAtZero: true,
                ticks: {
                    stepSize: 1
                }
            }
        }
    }
});

new Chart(document.getElementById('pieChart'), {
    type: 'pie',
    data: {
        labels: labels,
        datasets: [{
            data: dataStatistik,
            backgroundColor: warnaStatistik
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false
    }
});