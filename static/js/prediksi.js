console.log("prediksi.js loaded");

const chartData = document.getElementById("chart-data");
console.log(chartData);

const ctx = document.getElementById("historyChart");
console.log(ctx);

if (chartData) {
    const tanggal = JSON.parse(chartData.dataset.tanggal);
    const historis = JSON.parse(chartData.dataset.historis);
    const prediksi = JSON.parse(chartData.dataset.prediksi);

    console.log(tanggal);
    console.log(historis);
    console.log(prediksi)


    // Hapus chart lama jika ada
    const oldChart = Chart.getChart(ctx);

    if (oldChart) {
        oldChart.destroy();
    }

    new Chart(ctx, {
        type: "line",
        data: {
            labels: tanggal,
            datasets: [
                {
                    label: "Harga Aktual",
                    data: historis,
                    borderColor: "#2563eb",
                    backgroundColor: "rgba(37,99,235,0.15)",
                    fill: true,
                    tension: 0.15,
                    borderWidth: 3,
                    pointRadius: 5,
                    pointHoverRadius: 7,
                    pointBackgroundColor: "#2563eb",
                    pointBorderColor: "#ffffff",
                    pointBorderWidth: 2
                },

                {
                    label: "Prediksi AI",
                    data: prediksi,
                    borderColor: "#22c55e",
                    backgroundColor: "rgba(34,197,94,0.18)",
                    fill: true,
                    borderDash: [8,5],
                    tension: 0,
                    spanGaps: false,
                    borderWidth: 3,
                    pointRadius: 6,
                    pointHoverRadius: 6,
                    pointBackgroundColor: "#22c55e",
                    pointBorderColor: "#ffffff",
                    pointBorderWidth: 2
                }
            ]
        },

        options: {
            responsive: true,
            maintainAspectRatio: true,
            animation: false,
            scales: {
                x: {
                    grid: {display: false}
                },

                y: {
                    beginAtZero: false,
                    grace: "15%",
                    ticks: {callback: function(value){return "Rp " + value.toLocaleString("id-ID");}}
                }
            },

            plugins: {
                legend: {position: "top"},
                tooltip: {
                    callbacks: {
                        label: function(context){
                            if(context.parsed.y == null){return "";}
                            return context.dataset.label +" : Rp " + context.parsed.y.toLocaleString("id-ID");}
                    }
                }
            }
        }
    });
}