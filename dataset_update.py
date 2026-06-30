import requests
import pandas as pd
from datetime import datetime, timedelta

# KONFIGURASI
DATASET_LAMA = "dataset/processed/GARDA_DATASET_V1.csv"
DATASET_BARU = "dataset/processed/GARDA_DATASET_V2.csv"

PROVINCE_ID = 8
REGENCY_ID = 18
PRICE_TYPE = 1
COMCAT_ID = (
    "com_5,"
    "com_7,"
    "com_8,"
    "com_10,"
    "com_11,"
    "com_12,"
    "com_13,"
    "com_18"
)

# MENGAMBIL DATA DARI API BI
def ambil_data_api():
    today = datetime.today()
    start_date = (today - timedelta(days=7)).strftime("%Y-%m-%d")
    end_date = today.strftime("%Y-%m-%d")

    print("Tanggal awal :", start_date)
    print("Tanggal akhir:", end_date)
    url = (
    "https://www.bi.go.id/hargapangan/WebSite/TabelHarga/"
    "GetGridDataDaerah?"
    f"price_type_id={PRICE_TYPE}"
    f"&comcat_id={COMCAT_ID}"
    f"&province_id={PROVINCE_ID}"
    f"&regency_id={REGENCY_ID}"
    f"&market_id="
    f"&tipe_laporan=1"
    f"&start_date={start_date}"
    f"&end_date={end_date}"
)
    
    response = requests.get(url)
    response.raise_for_status()
    return response.json()



# JSON -> DATAFRAME
def json_ke_dataframe(data):
    rows = []

    for item in data["data"]:
        if item["level"] != 2:
            continue

        nama = item["name"]

        for key, value in item.items():
            if key in ["no", "name", "level"]:
                continue

            harga = None if value == "-" else int(value.replace(",", ""))
            rows.append({"Komoditas (Rp)": nama, "Tanggal": pd.to_datetime(key, format="%d/%m/%Y"), "Harga": harga, "Wilayah": "palembang"})

    return pd.DataFrame(rows)

# MEMBACA DATASET LAMA
def baca_dataset():
    df = pd.read_csv(DATASET_LAMA)
    df["Tanggal"] = pd.to_datetime(df["Tanggal"])
    df["Wilayah"] = df["Wilayah"].str.lower()
    return df


# MENGGABUNGKAN DATASE
def gabungkan_dataset(df_lama, df_api):
    df_api["Wilayah"] = df_api["Wilayah"].str.lower()
    dataset = pd.concat([df_lama, df_api], ignore_index=True)
    dataset.drop_duplicates(subset=["Komoditas (Rp)","Tanggal","Wilayah"], keep="last", inplace=True)
    dataset = dataset.sort_values(["Komoditas (Rp)", "Tanggal"]).reset_index(drop=True)
    return dataset

# MENYIMPAN DATASET
def simpan_dataset(df):
    df.to_csv(DATASET_BARU, index=False)

# MAIN PROGRAM
def update_dataset():
    data_json = ambil_data_api()
    dataset_api = json_ke_dataframe(data_json)
    dataset_lama = baca_dataset()
    dataset_baru = gabungkan_dataset(dataset_lama, dataset_api)
    simpan_dataset(dataset_baru)

# MENJALANKAN PROGRAM
if __name__ == "__main__":
    update_dataset()