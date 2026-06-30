import pandas as pd
from ai_engine import (
    prediksi_otomatis, 
    daftar_komoditas, 
    histori_7_hari, 
    get_dashboard_data, 
    garda_insight, peringatan_dini,
    data_simulasi, 
    rekomendasi_ai, 
    cek_kewajaran, 
    satuan
    )
from pipeline_updatedata import run_pipeline
from flask import Flask, render_template, request


app = Flask(__name__)

@app.route("/")
def dashboard():
    data = get_dashboard_data()
    insight = garda_insight(data)
    return render_template("dashboard.html", data=data, insight=insight)

@app.route("/prediksi", methods=["GET", "POST"])
def prediksi():

    # Membaca dataset untuk dropdown
    komoditas_list = daftar_komoditas()
    hasil = None
    grafik = None

    if request.method == "POST":
        komoditas = request.form["komoditas"]
        hasil = prediksi_otomatis(komoditas)
        grafik = histori_7_hari(komoditas)
    return render_template("prediksi.html", komoditas_list=komoditas_list, hasil=hasil, grafik=grafik)

@app.route("/peringatan_dini")
def peringatan():
    data, ringkasan, peringatan = peringatan_dini()
    return render_template("peringatan_dini.html", data=data, ringkasan=ringkasan, peringatan=peringatan)

@app.route("/simulasi")
def simulasi():
    komoditas = data_simulasi()
    return render_template("simulasi.html", komoditas=komoditas, satuan=satuan)

@app.route("/rekomendasi")
def rekomendasi():
    data, summary = rekomendasi_ai()
    return render_template("rekomendasi.html",data=data,summary=summary)

@app.route("/cek-harga", methods=["GET","POST"])
def cek():
    komoditas = daftar_komoditas()
    hasil = None

    if request.method == "POST":
        hasil = cek_kewajaran(request.form["komoditas"],float(request.form["harga"]))
    return render_template("cek_harga.html", komoditas=komoditas,hasil=hasil)

@app.route("/update-data")
def update_data():
    return render_template("update.html", pipeline=None)

@app.route("/run-pipeline")
def run_pipeline_now():
    hasil = run_pipeline()
    return render_template("update.html", pipeline=hasil)

if __name__ == "__main__":
    app.run(debug=True)