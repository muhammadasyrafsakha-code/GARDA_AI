import joblib
import pandas as pd

model = joblib.load("models/GARDA_MODEL.pkl")
encoder = joblib.load("models/LABEL_ENCODER.pkl")
features = joblib.load("models/FEATURES.pkl")
metrics = joblib.load("models/METRICS.pkl")

print("Backend AI berhasil dimuat.")

def prediksi_harga(
        komoditas,
        lag1,
        lag3,
        lag7,
        ma7,
        ma30,
        price_diff,
        price_change,
        tahun,
        bulan, 
        hari):
    
    kode = encoder.transform([komoditas])[0]
    data = pd.DataFrame([{
        "Komoditas (Rp)": kode,
        "Lag_1": lag1,
        "Lag_3": lag3,
        "Lag_7": lag7,
        "MA_7": ma7,
        "MA_30": ma30,
        "Price_Diff": price_diff,
        "Price_Change": price_change,
        "Tahun": tahun,
        "Bulan": bulan,
        "Hari": hari
        }])
    
    prediksi = model.predict(data)[0]
    return {
    "harga_prediksi": round(float(prediksi), 2),
    "status": "Naik" if prediksi > lag1 else "Turun",
    "selisih": round(float(prediksi - lag1), 2),
    "persentase": round(float(((prediksi - lag1) / lag1) * 100), 2)}
