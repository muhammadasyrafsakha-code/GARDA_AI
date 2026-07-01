import pandas as pd
from prediction import prediksi_harga

# KONFIGURASI
DATASET = "dataset/processed/GARDA_DATASET_FEATURE.csv"

df_global = pd.read_csv(DATASET)
df_global["Tanggal"] = pd.to_datetime(df_global["Tanggal"])
# MEMBACA DATASET
def baca_dataset():
    return df_global

# MENGAMBIL DATA TERAKHIR KOMODITAS
def ambil_data_terakhir(df, komoditas):
    data = df[df["Komoditas (Rp)"] == komoditas]
    if data.empty:
        raise ValueError(f"Komoditas '{komoditas}' tidak ditemukan.")

    return data.sort_values("Tanggal").iloc[-1]

# AI ENGINE
def prediksi_otomatis(komoditas):
    df = baca_dataset()
    data = ambil_data_terakhir(df, komoditas)
    hasil_ai = prediksi_harga(
        komoditas=komoditas,

        lag1=float(data["Lag_1"]),
        lag3=float(data["Lag_3"]),
        lag7=float(data["Lag_7"]),

        ma7=float(data["MA_7"]),
        ma30=float(data["MA_30"]),

        price_diff=float(data["Price_Diff"]),
        price_change=float(data["Price_Change"]),

        tahun=int(data["Tahun"]),
        bulan=int(data["Bulan"]),
        hari=int(data["Hari"])
    )

    harga_sekarang = float(data["Harga"])
    harga_prediksi = hasil_ai["harga_prediksi"]
    selisih = harga_prediksi - harga_sekarang
    persentase = (selisih / harga_sekarang) * 100

    return {
        "komoditas": komoditas,
        "tanggal":
        data["Tanggal"].strftime("%d-%m-%Y"),
        "harga_sekarang":
        round(harga_sekarang,2),
        "harga_prediksi":
        round(harga_prediksi,2),
        "selisih":
        round(selisih,2),
        "persentase":
        round(persentase,2),
        "status":
        "Naik" if selisih > 0 else "Turun"
    }

#insight (rule logic)
def garda_insight(data):
    naik = (data["Price_Diff"] > 0).sum()
    turun = (data["Price_Diff"] < 0).sum()
    stabil = (data["Price_Diff"] == 0).sum()
    total = len(data)

    # Kenaikan terbesar
    terbesar_naik = data.loc[data["Price_Change"].idxmax()]

    # Penurunan terbesar
    terbesar_turun = data.loc[data["Price_Change"].idxmin()]

    if naik > turun:
        narasi = (
            "GARDA AI mendeteksi mayoritas komoditas mengalami tren kenaikan harga. "
            f"Masyarakat disarankan mempertimbangkan pembelian lebih awal, terutama "
            f"{terbesar_naik['Komoditas (Rp)']} yang mengalami kenaikan tertinggi."
        )

    elif turun > naik:
        narasi = (
            "GARDA AI mendeteksi mayoritas komoditas mengalami penurunan harga. "
            "Kondisi ini menunjukkan pasar relatif lebih kondusif untuk konsumen."
        )

    else:
        narasi = (
            "GARDA AI mendeteksi kondisi pasar relatif stabil dengan jumlah "
            "komoditas naik dan turun yang hampir seimbang."
        )

    return {
        "total": total,
        "naik": int(naik),
        "turun": int(turun),
        "stabil": int(stabil),
        "komoditas_naik": terbesar_naik["Komoditas (Rp)"],
        "persen_naik": round(terbesar_naik["Price_Change"] * 100, 2),
        "komoditas_turun": terbesar_turun["Komoditas (Rp)"],
        "persen_turun": round(terbesar_turun["Price_Change"] * 100, 2),
        "narasi": narasi

    }

# DAFTAR KOMODITAS
def daftar_komoditas():
    df = baca_dataset()
    return sorted(df["Komoditas (Rp)"].unique())

#data 7 hari sebelum
def histori_7_hari(komoditas):
    df = baca_dataset()
    data = (df[df["Komoditas (Rp)"] == komoditas].sort_values("Tanggal").tail(7))
    
    # Prediksi besok
    hasil = prediksi_otomatis(komoditas)
    harga_prediksi = hasil["harga_prediksi"]

    tanggal = data["Tanggal"].dt.strftime("%d/%m").tolist()
    tanggal.append("Prediksi")

    historis = data["Harga"].tolist()
    historis.append(None)

    prediksi = [None] * 6
    prediksi.append(data["Harga"].iloc[-1])
    prediksi.append(harga_prediksi)

    return {
        "tanggal": tanggal,
        "historis": historis,
        "prediksi": prediksi
    }

#mengabil data untuk dashboard
def get_dashboard_data():
    df = baca_dataset()
    data = (df.sort_values("Tanggal").groupby("Komoditas (Rp)").tail(1).copy())
    grafik_list = []

    for komoditas in data["Komoditas (Rp)"]:
        grafik_list.append(histori_dashboard(komoditas))

    data["Grafik"] = grafik_list

    return data

#menagbil data 7 hari sebelum
def histori_dashboard(komoditas):
    df = baca_dataset()
    data = (df[df["Komoditas (Rp)"] == komoditas].sort_values("Tanggal").tail(7))

    return {
        "tanggal": data["Tanggal"].dt.strftime("%d/%m").tolist(),
        "harga": data["Harga"].tolist()
    }

#fungsi untuk meneu early warning
def peringatan_dini():
    hasil = []

    for komoditas in daftar_komoditas():
        prediksi = prediksi_otomatis(komoditas)
        persen = prediksi["persentase"]

        if persen >= 5:
            level = "Tinggi"
            warna = "danger"
            ikon = "🔴"
            pesan = (
                "Harga diprediksi naik cukup tinggi. "
                "Disarankan melakukan pembelian lebih awal."
            )

        elif persen >= 2:
            level = "Sedang"
            warna = "warning"
            ikon = "🟡"
            pesan = (
                "Terjadi potensi kenaikan harga. "
                "Perlu dilakukan pemantauan."
            )

        elif persen >= 0:
            level = "Rendah"
            warna = "success"
            ikon = "🟢"
            pesan = (
                "Harga relatif stabil dan tidak memerlukan tindakan khusus."
            )

        else:
            level = "Turun"
            warna = "primary"
            ikon = "🔵"
            pesan = (
                "Harga diprediksi menurun sehingga pembelian dapat ditunda."
            )

        hasil.append({
            "komoditas": komoditas,
            "harga": prediksi["harga_sekarang"],
            "prediksi": prediksi["harga_prediksi"],
            "persentase": prediksi["persentase"],
            "level": level,
            "warna": warna,
            "ikon": ikon,
            "pesan": pesan

        })
    urutan = {
            "Tinggi":0,
            "Sedang":1,
            "Rendah":2,
            "Turun":3,}

    hasil.sort(key=lambda x: urutan[x["level"]])
    ringkasan = {
    "tinggi": sum(x["level"] == "Tinggi" for x in hasil),
    "sedang": sum(x["level"] == "Sedang" for x in hasil),
    "rendah": sum(x["level"] == "Rendah" for x in hasil),
    "turun": sum(x["level"] == "Turun" for x in hasil)
    }

    peringatan = None
    for item in hasil:
        if item["level"] == "Tinggi":
            peringatan = item
            break

    return hasil, ringkasan, peringatan

#dictionary untuk kalkulator pengeluaran
satuan = {
    "Beras Kualitas Super I":"kg",
    "Cabai Merah Besar":"kg",
    "Bawang Merah Ukuran Sedang":"kg",
    "Bawang Putih Ukuran Sedang":"kg",
    "Daging Ayam Ras Segar":"kg",
    "Daging Sapi Kualitas 1":"kg",
    "Minyak Goreng Kemasan Bermerk 1":"L",
    "Telur Ayam Ras Segar":"kg"
}

#mengambil data untuk simulasi
def data_simulasi():
    data = []

    for komoditas in daftar_komoditas():
        hasil = prediksi_otomatis(komoditas)
        data.append({
            "nama": komoditas,
            "harga": hasil["harga_sekarang"],
            "prediksi": hasil["harga_prediksi"]
        })

    return data

#fungsi untuk menu simulasi
def rekomendasi_ai():
    hasil = []

    for komoditas in daftar_komoditas():
        prediksi = prediksi_otomatis(komoditas)
        hasil.append({
            "komoditas": komoditas,
            "harga": prediksi["harga_sekarang"],
            "prediksi": prediksi["harga_prediksi"],
            "persentase": prediksi["persentase"]
        })

    hasil.sort(key=lambda x: x["persentase"], reverse=True)
    prioritas = len([x for x in hasil if x["persentase"] > 2])
    stabil = len([x for x in hasil if 0 <= x["persentase"] <= 2])
    turun = len([x for x in hasil if x["persentase"] < 0])
    summary = {
        "jumlah": len(hasil),
        "prioritas": prioritas,
        "stabil": stabil,
        "turun": turun,
        "top1": hasil[0]["komoditas"],
        "top2": hasil[1]["komoditas"] if len(hasil) > 1 else "-"
    }

    return hasil, summary

#fungsi untuk cek kewajaran
def cek_kewajaran(komoditas, harga_input):
    prediksi = prediksi_otomatis(komoditas)
    harga_ai = prediksi["harga_prediksi"]
    selisih = harga_input - harga_ai
    persen = (selisih / harga_ai) * 100

    #price fairness score
    score = 100 - abs(persen) * 2
    score = max(0, min(100, round(score)))

    if abs(persen) <= 10:
        status = "Wajar"
        warna = "success"
        ikon = "🟢"
        insight = (
            "Harga yang Anda temukan masih berada dalam batas kewajaran "
            "berdasarkan analisis GARDA AI."
        )

    elif persen > 10:
        status = "Lebih Mahal"
        warna = "danger"
        ikon = "🔴"
        insight = (
            "Harga lebih tinggi dibandingkan harga referensi GARDA AI. "
            "Disarankan membandingkan harga dengan penjual lain."
        )

    else:
        status = "Lebih Murah"
        warna = "primary"
        ikon = "🔵"
        insight = (
            "Harga lebih rendah dibandingkan harga referensi GARDA AI. "
            "Pastikan kualitas produk sebelum membeli."
        )

    return {
        "harga_ai": round(harga_ai),
        "harga_input": harga_input,
        "selisih": round(selisih),
        "persentase": round(persen,2),
        "status": status,
        "warna": warna,
        "ikon": ikon,
        "insight": insight,
        "score": round(score)
    }

# TEST PROGRAM
if __name__ == "__main__":
    hasil = prediksi_otomatis("Beras Kualitas Super I")

    print(f"Komoditas      : {hasil['komoditas']}")
    print(f"Tanggal        : {hasil['tanggal']}")
    print(f"Harga Sekarang : Rp {hasil['harga_sekarang']:,.2f}")
    print(f"Prediksi Besok : Rp {hasil['harga_prediksi']:,.2f}")
    print(f"Selisih        : Rp {hasil['selisih']:,.2f}")
    print(f"Persentase     : {hasil['persentase']} %")
    print(f"Status         : {hasil['status']}")