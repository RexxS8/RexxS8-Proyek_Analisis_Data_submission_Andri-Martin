import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
def load_data():
    df = pd.read_csv("C:/Users/andri/Documents/Andri Martin/Trisakti/Semester 6/DBS_Coding-Camp2025/submission/dashboard/main_data.csv")
    return df

df = load_data()

# Sidebar untuk filter
st.sidebar.header("Filter Data")
season = st.sidebar.selectbox("Pilih Musim:", df["season"].unique())
weather = st.sidebar.selectbox("Pilih Cuaca:", df["weathersit"].unique())

# Filter data berdasarkan input pengguna
df_filtered = df[(df["season"] == season) & (df["weathersit"] == weather)]

# Layout Dashboard
st.title("Dashboard Bike Sharing Analysis")
st.write("Dataset ini menunjukkan jumlah penyewaan sepeda berdasarkan kondisi cuaca, musim, dan waktu.")

# Menampilkan data
st.subheader("Data yang Dipilih")
st.write(df_filtered.head())

# Visualisasi Penyewaan Sepeda per Bulan
st.subheader("Tren Penyewaan Sepeda per Bulan")
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=df_filtered, x="mnth", y="cnt_days", marker='o', ax=ax)
plt.xlabel("Bulan")
plt.ylabel("Jumlah Penyewaan")
plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
st.pyplot(fig)

# Memilih hanya kolom numerik untuk heatmap
numeric_cols = df_filtered.select_dtypes(include=['number'])

# Heatmap Korelasi
st.subheader("Heatmap Korelasi")
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(numeric_cols.corr(), annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
st.pyplot(fig)

# Statistik Data
st.subheader("Statistik Deskriptif")
st.write(df_filtered.describe())