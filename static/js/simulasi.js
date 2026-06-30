let donutChart = null;

// HITUNG TOTAL + UPDATE CHART + INSIGHT
function hitungTotal() {
    let totalSekarang = 0;
    let totalPrediksi = 0;
    const labels = [];
    const values = [];

    document.querySelectorAll(".jumlah").forEach(input => {
        const jumlah = Number(input.value);
        const harga = Number(input.dataset.harga);
        const prediksi = Number(input.dataset.prediksi);
        totalSekarang += jumlah * harga;
        totalPrediksi += jumlah * prediksi;

        if (jumlah > 0) {
            const nama = input.parentElement.parentElement
                .querySelector("label").innerText;
            labels.push(nama);
            values.push(jumlah * harga);
        }
    });

    // UPDATE RINGKASAN
    document.getElementById("totalSekarang").innerHTML =
        "Rp " + Math.round(totalSekarang).toLocaleString("id-ID");

    document.getElementById("totalPrediksi").innerHTML =
        "Rp " + Math.round(totalPrediksi).toLocaleString("id-ID");

    const selisih = totalPrediksi - totalSekarang;
    const elemenSelisih = document.getElementById("selisih");

    elemenSelisih.innerHTML =
        "Rp " + Math.round(selisih).toLocaleString("id-ID");

    if (selisih > 0) {
        elemenSelisih.className = "text-danger";

    } else if (selisih < 0) {
        elemenSelisih.className = "text-primary";

    } else {
        elemenSelisih.className = "text-success";

    }

    // UPDATE DONUT CHART
    const ctx = document.getElementById("pengeluaranChart");

    if (donutChart) {donutChart.destroy();}

    if (ctx && values.length > 0) {
        donutChart = new Chart(ctx, {
            type: "doughnut",
            data: {
                labels: labels,
                datasets: [{
                    data: values,
                    backgroundColor: [
                        "#2563eb",
                        "#22c55e",
                        "#f59e0b",
                        "#ef4444",
                        "#8b5cf6",
                        "#06b6d4",
                        "#84cc16",
                        "#ec4899"
                    ],

                    borderColor: "#ffffff",
                    borderWidth: 2
                }]
            },

            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: "65%",
                plugins: {
                    legend: {position: "right"},
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return context.label +
                                    " : Rp " +
                                    context.parsed.toLocaleString("id-ID");
                            }
                        }
                    }
                }
            }
        });
    }

    // GARDA AI INSIGHT
    const insight = document.getElementById("insightAI");
    if (!insight) return;

    if (values.length === 0) {
        insight.className = "alert alert-secondary";
        insight.innerHTML = `
            <h5>GARDA AI</h5>
            Masukkan jumlah komoditas untuk memperoleh analisis pengeluaran.
        `;
        return;
    }

    const terbesar = Math.max(...values);
    const index = values.indexOf(terbesar);
    const namaTerbesar = labels[index];
    const kontribusi = ((terbesar / totalSekarang) * 100).toFixed(1);
    const persen =
        totalSekarang == 0
        ? 0
        : ((Math.abs(selisih) / totalSekarang) * 100).toFixed(2);

    // LEVEL RISIKO
    let level = "";
    let emoji = "";
    let rekomendasi = "";

    if (persen < 2){
        level = "Rendah";
        emoji = "🟢";
        rekomendasi = "Belanja dapat dilakukan sesuai kebutuhan karena perubahan harga relatif kecil.";
    }

    else if (persen < 5){
        level = "Sedang";
        emoji = "🟡";
        rekomendasi ="Pertimbangkan membeli lebih awal apabila komoditas utama sering dikonsumsi.";
    }

    else{
        level = "Tinggi";
        emoji = "🔴";
        rekomendasi ="Disarankan melakukan pembelian lebih awal untuk mengurangi dampak kenaikan harga.";
    }

    // NARASI
    if (selisih > 0){
        insight.className = "alert alert-danger";
        insight.innerHTML = `
            <h5>GARDA AI Insight</h5>

            <p>
            Total pengeluaran diprediksi
            <strong>naik Rp ${Math.round(selisih).toLocaleString("id-ID")}</strong>
            atau sekitar
            <strong>${persen}%</strong>.
            </p>

            <p>
            <strong>${namaTerbesar}</strong>
            menjadi kontributor terbesar dengan porsi
            <strong>${kontribusi}%</strong>
            dari total pengeluaran.
            </p>

            <p>
            Risiko Kenaikan Pengeluaran:
            <strong>${emoji} ${level}</strong>
            </p>

            <hr>

            <strong>Rekomendasi GARDA AI</strong>

            <ul class="mb-0">
                <li>${rekomendasi}</li>
                <li>Prioritaskan pembelian <strong>${namaTerbesar}</strong>.</li>
                <li>Pantau kembali prediksi harga beberapa hari ke depan.</li>
            </ul>
        `;
    }

    else if (selisih < 0){
        insight.className = "alert alert-success";
        insight.innerHTML = `
            <h5>GARDA AI Insight</h5>

            <p>
            Total pengeluaran diprediksi
            <strong>turun Rp ${Math.round(Math.abs(selisih)).toLocaleString("id-ID")}</strong>
            atau sekitar
            <strong>${persen}%</strong>.
            </p>

            <p>
            Pengeluaran terbesar tetap berasal dari
            <strong>${namaTerbesar}</strong>
            sebesar
            <strong>${kontribusi}%</strong>.
            </p>

            <p>
            Kondisi pasar :
            <strong>🟢 Menguntungkan</strong>
            </p>

            <hr>

            <strong>Rekomendasi GARDA AI</strong>

            <ul class="mb-0">
                <li>Pembelian dapat dilakukan sesuai kebutuhan.</li>
                <li>Manfaatkan penurunan harga untuk menghemat pengeluaran.</li>
                <li>Tidak diperlukan pembelian lebih awal.</li>
            </ul>
        `;
    }

    else{
        insight.className = "alert alert-info";
        insight.innerHTML = `
            <h5>GARDA AI Insight</h5>

            Harga diprediksi relatif stabil.

            <hr>

            <strong>Rekomendasi GARDA AI</strong>

            <ul class="mb-0">
                <li>Lakukan pembelian sesuai kebutuhan.</li>
                <li>Tidak terdapat risiko kenaikan harga yang signifikan.</li>
            </ul>
        `;
    }}

// TOMBOL PLUS
document.querySelectorAll(".plus").forEach(button => {
    button.addEventListener("click", () => {
        const input = button.parentElement.querySelector(".jumlah");
        input.value = Number(input.value) + 1;
        hitungTotal();
    });
});

// TOMBOL MINUS
document.querySelectorAll(".minus").forEach(button => {
    button.addEventListener("click", () => {
        const input = button.parentElement.querySelector(".jumlah");

        if (Number(input.value) > 0) {
            input.value = Number(input.value) - 1;
            hitungTotal();
        }
    });
});

// HITUNG AWAL
hitungTotal();
