import pandas as pd

DATASET = "dataset/processed/GARDA_DATASET_V2.csv"
OUTPUT = "dataset/processed/GARDA_DATASET_FEATURE.csv"

def create_feature():

    # Membaca Dataset
    print("Membaca dataset...")
    df = pd.read_csv(DATASET)
    df["Tanggal"] = pd.to_datetime(df["Tanggal"])
    df = df.dropna(subset=["Harga"]).reset_index(drop=True)
    df = df.sort_values(["Komoditas (Rp)", "Tanggal"]).reset_index(drop=True)

    # Lag Feature
    print("Membuat Lag Feature...")
    df["Lag_1"] = (df.groupby("Komoditas (Rp)")["Harga"].shift(1))
    df["Lag_3"] = (df.groupby("Komoditas (Rp)")["Harga"].shift(3))
    df["Lag_7"] = (df.groupby("Komoditas (Rp)")["Harga"].shift(7))

    # Moving Average
    print("Membuat Moving Average...")
    df["MA_7"] = (df.groupby("Komoditas (Rp)")["Harga"].transform(lambda x: x.rolling(window=7).mean()))
    df["MA_30"] = (df.groupby("Komoditas (Rp)")["Harga"].transform(lambda x: x.rolling(window=30).mean()))

    # Price Feature
    print("Membuat Feature Harga...")
    df["Price_Diff"] = (df.groupby("Komoditas (Rp)")["Harga"].diff())
    df["Price_Change"] = (df.groupby("Komoditas (Rp)")["Harga"].pct_change())

    # Time Feature
    print("Membuat Feature Waktu...")
    df["Tahun"] = df["Tanggal"].dt.year
    df["Bulan"] = df["Tanggal"].dt.month
    df["Hari"] = df["Tanggal"].dt.dayofweek

    # Menghapus NaN
    df = df.dropna().reset_index(drop=True)

    # Menyimpan Dataset
    print("Menyimpan dataset feature...")
    df.to_csv(OUTPUT, index=False)
    return df


if __name__ == "__main__":
    create_feature()