import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


sns.set(style='darkgrid')

# --- 1. SETUP DATA & MAPPING ---
season_mapping = {1: 'Musim Semi', 2: 'Musim Panas', 3: 'Musim Gugur', 4: 'Musim Dingin'}
weather_mapping = {1: 'Cerah/Sedikit Berawan', 2: 'Berawan/Berkabut', 3: 'Hujan Ringan/Salju', 4: 'Cuaca Ekstrim'}
workingday_mapping = {0: 'Akhir Pekan/Libur', 1: 'Hari Kerja'}


@st.cache_data
def load_data():
    
    try:
        df = pd.read_csv("dashboard/day.csv") 
    except FileNotFoundError:
        df = pd.read_csv("day.csv")

    if 'dteday' in df.columns:
        df['dteday'] = pd.to_datetime(df['dteday'])
    
    # Mapping Data
    df['season_label'] = df['season'].map(season_mapping)
    df['weather_label'] = df['weathersit'].map(weather_mapping)
    df['workingday_label'] = df['workingday'].map(workingday_mapping)
    
    
    df['temp_category'] = pd.cut(
        df['temp'], 
        bins=[0, 0.35, 0.7, 1.0], 
        labels=['Sejuk', 'Sedang', 'Panas']
    )
    return df

all_df = load_data()

#sidebar
with st.sidebar:
    st.header("Selamat Datang")
    st.text("Penyewaan Sepeda Berkualitas by Ariel Gibranu")
    st.image("dashboard/sepeda.jpg")
    
    
    
    season_options = ['Semua Musim'] + list(season_mapping.values())
    selected_season = st.selectbox('Pilih Musim:', season_options)
    
    st.caption('Copyright (c) Ariel Gibranu 2024')


if selected_season == 'Semua Musim':
    filtered_df = all_df
else:
    filtered_df = all_df[all_df['season_label'] == selected_season]


st.title('Analisis Data Bike Sharing :sparkles:')
st.write(f"Menampilkan data untuk: **{selected_season}**")


col1, col2 = st.columns(2)
with col1:
    total_sewa = filtered_df['cnt'].sum()
    st.metric("Total Penyewaan", value=f"{total_sewa:,}")
with col2:
    avg_sewa = filtered_df['cnt'].mean()
    st.metric("Rata-rata Harian", value=f"{avg_sewa:.2f}")

st.markdown("---")

# 1.
st.subheader("1. Jumlah Penyewaan: Hari Kerja vs Libur")

wd_counts = filtered_df.groupby('workingday_label')['cnt'].sum()
wd_order = ['Akhir Pekan/Libur', 'Hari Kerja']
wd_counts = wd_counts.reindex(wd_order, fill_value=0)

fig_wd, ax_wd = plt.subplots(figsize=(8, 5))
sns.barplot(x=wd_counts.index, y=wd_counts.values, palette=["#FFA726", "#29B6F6"], ax=ax_wd)
ax_wd.set_ylabel('Total Penyewaan')
ax_wd.set_xlabel(None)

for i, v in enumerate(wd_counts.values):
    ax_wd.text(i, v + (v*0.01), str(int(v)), ha='center', va='bottom')

st.pyplot(fig_wd)


# 2.
st.subheader("2. Jumlah Penyewaan Berdasarkan Cuaca")

weather_counts = filtered_df.groupby('weather_label')['cnt'].sum()
weather_order = ['Cerah/Sedikit Berawan', 'Berawan/Berkabut', 'Hujan Ringan/Salju', 'Cuaca Ekstrim']
weather_counts = weather_counts.reindex(weather_order, fill_value=0)

fig_weather, ax_weather = plt.subplots(figsize=(10, 6))
sns.barplot(x=weather_counts.index, y=weather_counts.values, palette="Blues_d", ax=ax_weather)
ax_weather.set_ylabel('Total Penyewaan')
ax_weather.set_xlabel(None)

for i, v in enumerate(weather_counts.values):
    ax_weather.text(i, v + (v*0.01), str(int(v)), ha='center', va='bottom')

st.pyplot(fig_weather)


# 3.
st.markdown("---")
st.header("Analisis Lanjutan")
st.subheader("3. Rata-rata Penyewaan Berdasarkan Suhu")


temp_avg = filtered_df.groupby('temp_category', observed=False)['cnt'].mean()


temp_order = ['Sejuk', 'Sedang', 'Panas']
temp_avg = temp_avg.reindex(temp_order, fill_value=0)

fig_temp, ax_temp = plt.subplots(figsize=(9, 6))


sns.barplot(
    x=temp_avg.index, 
    y=temp_avg.values, 
    palette=["#4DD0E1", "#FFD54F", "#FF7043"], 
    ax=ax_temp
)

ax_temp.set_title(f"Rata-rata Penyewaan pada {selected_season}")
ax_temp.set_ylabel('Rata-rata Penyewaan')
ax_temp.set_xlabel('Suhu')


for i, v in enumerate(temp_avg.values):
    
    ax_temp.text(i, v + (v*0.01), f"{v:.2f}", ha='center', va='bottom', fontsize=11, fontweight='bold')

st.pyplot(fig_temp)