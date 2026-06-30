import os
import joblib
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    mean_absolute_percentage_error)

from xgboost import XGBRegressor

DATASET = "dataset/processed/GARDA_DATASET_FEATURE.csv"
MODEL_PATH = "models"

# TRAIN MODEL
def train_model(show_plot=True):
    # Membaca Dataset
    print("Membaca dataset feature...")
    df = pd.read_csv(DATASET)
    df["Tanggal"] = pd.to_datetime(df["Tanggal"])

    # Feature dan Target
    x = df[[
        "Komoditas (Rp)",
        "Lag_1",
        "Lag_3",
        "Lag_7",
        "MA_7",
        "MA_30",
        "Price_Diff",
        "Price_Change",
        "Tahun",
        "Bulan",
        "Hari"
    ]].copy()
    y = df["Harga"]

    # Label Encoder
    encoder = LabelEncoder()
    x["Komoditas (Rp)"] = encoder.fit_transform(x["Komoditas (Rp)"])

    # Train Test Split
    tanggal_unik = sorted(df["Tanggal"].unique())
    cutoff = tanggal_unik[int(len(tanggal_unik) * 0.9)]
    train_mask = df["Tanggal"] <= cutoff
    test_mask = df["Tanggal"] > cutoff
    x_train = x[train_mask]
    x_test = x[test_mask]
    y_train = y[train_mask]
    y_test = y[test_mask]

    # Membuat Model
    print("Melatih model AI...")
    model = XGBRegressor(

        objective="reg:squarederror",
        n_estimators=100,
        learning_rate=0.1,
        max_depth=6,
        random_state=42)
    model.fit(x_train, y_train)

    # Prediksi
    y_pred = model.predict(x_test)

    # Evaluasi
    mae = mean_absolute_error(y_test, y_pred)
    rmse = mean_squared_error(y_test,y_pred) ** 0.5
    mape = mean_absolute_percentage_error(y_test, y_pred)

    # Feature Importance
    importance = pd.DataFrame({"Feature": x_train.columns, "Importance": model.feature_importances_})
    importance = importance.sort_values(by="Importance", ascending=False)
    
    # Simpan Model
    print("Menyimpan model...")
    os.makedirs(MODEL_PATH, exist_ok=True)
    joblib.dump(model, os.path.join(MODEL_PATH, "GARDA_MODEL.pkl"))
    joblib.dump(encoder, os.path.join(MODEL_PATH, "LABEL_ENCODER.pkl"))
    joblib.dump(x.columns.tolist(), os.path.join(MODEL_PATH, "FEATURES.pkl"))
    joblib.dump({"MAE": mae, "RMSE": rmse, "MAPE": mape}, os.path.join(MODEL_PATH, "METRICS.pkl"))

    # Monitoring
    print()
    print("HASIL TRAINING")
    print()
    print("Train Data :", len(x_train))
    print("Test Data  :", len(x_test))
    print()
    print("Cutoff :", cutoff)
    print()
    print(f"MAE  : {mae:.2f}")
    print(f"RMSE : {rmse:.2f}")
    print(f"MAPE : {mape*100:.2f}%")
    print()
    print("Feature Importance")
    print(importance)
    print()
    print("Model berhasil disimpan.")

    # Grafik
    if show_plot:
        plt.figure(figsize=(14,6))
        plt.plot(y_test.values, label="Harga Asli", linewidth=2)
        plt.plot(y_pred, label="Prediksi AI", linewidth=2)
        plt.title("Perbandingan Harga Asli dan Prediksi AI")
        plt.xlabel("Data")
        plt.ylabel("Harga")
        plt.grid(True)
        plt.legend()
        plt.show()
        plt.figure(figsize=(10,6))
        plt.barh(importance["Feature"], importance["Importance"])
        plt.title("Feature Importance")
        plt.gca().invert_yaxis()
        plt.grid(True)
        plt.show()

    return model


# MAIN
if __name__ == "__main__":
    train_model()