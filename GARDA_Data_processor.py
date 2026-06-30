import os
import pandas as pd

folder = "../dataset/raw_data"
files = os.listdir(folder)

print("File yang ditemukan:")

def transform_dataset(df):
    df = df.iloc[[1]]
    df = df.drop(columns=["No"])
    df = pd.melt(df, id_vars = ["Komoditas (Rp)"], var_name = "Tanggal", value_name = "Harga" )
    df ["Harga"] = df["Harga"].replace("-", pd.NA)
    df["Harga"] = df["Harga"].astype(str)
    df["Harga"] = df["Harga"].str.replace(",", "")
    df["Harga"] = pd.to_numeric(df["Harga"], errors = "coerce")

    df["Tanggal"] = df["Tanggal"].str.replace(" ", "", regex=False)
    df["Tanggal"] = pd.to_datetime(df["Tanggal"], format = "%d/%m/%Y")

    df["Wilayah"] = "palembang"

    print(df.info())
    print(df.head(10))
    return df

semua_data = []

for file in files:
    path_file = os.path.join(folder, file)
    df = pd.read_excel(path_file)
    hasil = transform_dataset (df)
    semua_data.append(hasil)

    print(hasil)

dataset = pd.concat(semua_data, ignore_index=True)

print(dataset.info())
print(dataset.head())
print(dataset.tail())

dataset.to_csv("../dataset/processed/GARDA_DATASET_V1.csv", index = False)

print("")
print("dataset sudah berhasil di edit dan berhasil disimpan")