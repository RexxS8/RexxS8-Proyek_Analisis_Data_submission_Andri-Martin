import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
def load_data():
    df = pd.read_csv("dashboard/main_data.csv")
    return df

df = load_data()

# Mapping season
season_dict = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
# Mapping weathersit
weather_dict = {
    1: "Clear / Few clouds / Partly cloudy",
    2: "Mist / Cloudy / Broken clouds",
    3: "Light Snow / Light Rain / Thunderstorm",
    4: "Heavy Rain / Snow / Fog"
}

# Sidebar Filter
st.sidebar.header("🔍 **Filter Data**")

# Pilihan musim dengan label yang lebih jelas
season = st.sidebar.selectbox(
    "📅 **Pilih Musim**",
    options=df["season"].unique(),
    format_func=lambda x: season_dict.get(x, "Unknown")
)

# Pilihan cuaca dengan label yang lebih jelas
weather = st.sidebar.selectbox(
    "🌦 **Pilih Kondisi Cuaca**",
    options=df["weathersit"].unique(),
    format_func=lambda x: weather_dict.get(x, "Unknown")
)

# Tampilkan hasil filter dalam teks
st.sidebar.markdown(f"✅ **Musim dipilih:** {season_dict.get(season, 'Unknown')}")
st.sidebar.markdown(f"✅ **Kondisi Cuaca dipilih:** {weather_dict.get(weather, 'Unknown')}")

# Filter data berdasarkan input pengguna
df_filtered = df[(df["season"] == season) & (df["weathersit"] == weather)]

# Layout Dashboard
st.title("🚲 Dashboard Bike Sharing Analysis")
st.write("Analisis data penyewaan sepeda berdasarkan kondisi cuaca, musim, dan waktu.")

# **Pertanyaan 1: Bagaimana pengaruh kondisi cuaca terhadap jumlah penyewaan sepeda pada hari kerja dan akhir pekan?**
st.subheader("📌 Pengaruh Kondisi Cuaca terhadap Penyewaan Sepeda")

# Menghitung rata-rata penyewaan berdasarkan cuaca dan hari kerja
weather_effect = df.groupby(['weathersit', 'workingday'])['cnt_days'].mean().reset_index()

# Mapping label untuk kategori cuaca dan hari kerja
weather_effect['weathersit'] = weather_effect['weathersit'].map(weather_dict)
weather_effect['workingday'] = weather_effect['workingday'].map({0: "Akhir Pekan", 1: "Hari Kerja"})

# Visualisasi dalam bar chart
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x='weathersit', y='cnt_days', hue='workingday', data=weather_effect, palette='coolwarm', ax=ax)
plt.xlabel("Kondisi Cuaca")
plt.ylabel("Rata-rata Penyewaan Sepeda")
plt.title("Pengaruh Kondisi Cuaca terhadap Penyewaan Sepeda")
plt.xticks(rotation=15)
plt.legend(title="Kategori Hari")
st.pyplot(fig)

# **Pertanyaan 2: Bagaimana dampak hari libur terhadap jumlah penyewaan sepeda?**
st.subheader("📌 Dampak Hari Libur terhadap Penyewaan Sepeda")

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x='holiday', y='cnt_days', data=df, palette='viridis', estimator=sum, ax=ax)
plt.title('Dampak Hari Libur terhadap Penyewaan Sepeda')
plt.xlabel('Hari Libur (0: Bukan Libur, 1: Libur)')
plt.ylabel('Total Penyewaan Sepeda')
st.pyplot(fig)

# **Pertanyaan 3: Bagaimana tren penggunaan sepeda berdasarkan musim dalam satu tahun terakhir?**
st.subheader("📌 Tren Penggunaan Sepeda Berdasarkan Musim")

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x='mnth', y='cnt_hours', hue='season', data=df, marker='o', palette='Set1', ax=ax)
plt.title('Tren Penggunaan Sepeda Berdasarkan Musim')
plt.xlabel('Bulan')
plt.ylabel('Total Penyewaan per Jam')
plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.legend(title='Musim', labels=['Spring', 'Summer', 'Fall', 'Winter'])
st.pyplot(fig)

# Statistik Data
st.subheader("📊 Statistik Deskriptif")
st.write(df_filtered.describe())

# Heatmap Korelasi
st.subheader("🔥 Heatmap Korelasi")
numeric_cols = df_filtered.select_dtypes(include=['number'])
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(numeric_cols.corr(), annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
st.pyplot(fig)
