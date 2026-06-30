import pandas as pd

DATASET = "../dataset/processed/GARDA_DATASET_V2.csv"

df = pd.read_csv(DATASET)
df["Tanggal"] = pd.to_datetime(df["Tanggal"])

print("INFORMASI DATASET")
print("=" * 60)
print(df.info())
print()

print("JUMLAH DATA")
print("=" * 60)
print(f"Total Baris      : {len(df)}")
print(f"Total Kolom      : {len(df.columns)}")
print(f"Jumlah Komoditas : {df['Komoditas (Rp)'].nunique()}")
print()

print("RENTANG TANGGAL")
print("=" * 60)
print("Tanggal Awal :", df["Tanggal"].min().date())
print("Tanggal Akhir:", df["Tanggal"].max().date())
print()

print("MISSING VALUE")
print("=" * 60)
print(df.isnull().sum())
print()

print("DUPLIKAT")
print("=" * 60)
print(df.duplicated().sum())
print()

print("DAFTAR KOMODITAS")
print("=" * 60)
for komoditas in sorted(df["Komoditas (Rp)"].unique()):
    print("-", komoditas)
print()

print("JUMLAH DATA PER KOMODITAS")
print("=" * 60)
print(df.groupby("Komoditas (Rp)").size())
print()