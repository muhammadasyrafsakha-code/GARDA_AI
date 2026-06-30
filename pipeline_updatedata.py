import time
import joblib
from datetime import datetime
from dataset_update import update_dataset
from feature import create_feature
from train_model import train_model

#fungsi untuk mengupdate data terbaru melalui PIHPS
def run_pipeline():
    start = time.time()

    try:

        # STEP 1
        update_dataset()
        print("Dataset berhasil diperbarui")

        # STEP 2
        create_feature()
        print("Feature berhasil dibuat")

        # STEP 3
        train_model(show_plot=False)
        print("Model berhasil dilatih")

        # LOAD METRICS
        metrics = joblib.load("models/METRICS.pkl")
        mape = round(metrics["MAPE"] * 100, 2)

        # AI HEALTH
        if mape < 2:
            health = "Excellent"
            color = "success"
            insight = (
                "Model AI memiliki tingkat kesalahan yang sangat rendah. "
                "Prediksi dinilai sangat andal."
            )

        elif mape < 5:
            health = "Good"
            color = "primary"
            insight = (
                "Model AI memiliki performa yang baik "
                "dan layak digunakan."
            )

        elif mape < 10:
            health = "Fair"
            color = "warning"
            insight = (
                "Performa model mulai menurun. "
                "Disarankan menambah data pelatihan."
            )

        else:
            health = "Poor"
            color = "danger"
            insight = (
                "Model memiliki tingkat kesalahan yang cukup tinggi. "
                "Disarankan melakukan retraining."
            )

        # TOTAL WAKTU
        total = round(time.time() - start, 2)
        print(f"Durasi : {total} detik")

        return {
            "status": "success",
            "message": "GARDA AI berhasil diperbarui.",
            "time": total,
            "updated_at": datetime.now().strftime("%d %B %Y %H:%M"),
            "model": "XGBoost",
            "version": "GARDA AI v1.0",
            "mape": mape,
            "health": health,
            "color": color,
            "insight": insight
        }

    except Exception as e:
        total = round(time.time() - start, 2)

        return {
            "status": "failed",
            "message": str(e),
            "time": total,
            "updated_at": datetime.now().strftime("%d %B %Y %H:%M"),
            "model": "-",
            "version": "GARDA AI v1.0",
            "mape": "-",
            "health": "Error",
            "color": "danger",
            "insight": "Pipeline gagal dijalankan."
        }

# MAIN
if __name__ == "__main__":
    hasil = run_pipeline()

    for key, value in hasil.items():
        print(f"{key:12}: {value}")