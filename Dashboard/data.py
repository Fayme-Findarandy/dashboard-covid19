import streamlit as st
import pandas as pd
import plotly.express as px

def map_chart(df, year=None):
    df['Date'] = pd.to_datetime(df['Date'])
    
    if year:
        df = df[df['Date'].dt.year == year]
    
    df_agg = df.groupby(['Location', 'Latitude', 'Longitude'], as_index=False)['New Cases'].sum()
    df_map = df_agg.dropna(subset=['Latitude', 'Longitude', 'New Cases'])
    
    if df_map.empty:
        st.info("Tidak ada data untuk ditampilkan di peta.")
        return
    
    fig = px.scatter_mapbox(
        df_map,
        lat="Latitude",
        lon="Longitude",
        size="New Cases",
        color="New Cases",
        hover_name="Location",
        zoom=3,
        center={"lat": -2.5, "lon": 118},
        size_max=20,
        opacity=0.7,
        color_continuous_scale="OrRd",
        title=f"Sebaran Kasus Baru Covid-19 di Indonesia ({year if year else 'Semua Tahun'})"
    )
    
    fig.update_layout(
        mapbox_style="carto-positron",
        height=600,
        margin={"r":0,"t":50,"l":0,"b":0}
    )
    
    st.plotly_chart(fig, use_container_width=True)

def bar_chart1(df):
    df_last = df.sort_values('Date').groupby('Location', as_index=False).last()
    top5 = df_last.nlargest(5, 'Total Deaths')
    fig = px.bar(
        top5,
        x='Location',
        y='Total Deaths',
        color='Total Deaths',
        color_continuous_scale='Reds',
        title='5 Provinsi dengan Kematian Tertinggi',
        labels={'Total Deaths': 'Total Kematian', 'Location': 'Provinsi'}
    )
    fig.update_layout(xaxis_title='Provinsi', yaxis_title='Total Kematian', title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)

def bar_chart2(df):
    df_last = df.sort_values('Date').groupby('Location', as_index=False).last()
    top5 = df_last.nlargest(5, 'Total Recovered')
    fig = px.bar(
        top5,
        x='Location',
        y='Total Recovered',
        color='Total Recovered',
        color_continuous_scale='Greens',
        title='5 Provinsi dengan Kesembuhan Tertinggi',
        labels={'Total Recovered': 'Total Kesembuhan', 'Location': 'Provinsi'}
    )
    fig.update_layout(xaxis_title='Provinsi', yaxis_title='Total Kesembuhan', title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)

def pie_chart1(df):
    total_mati = total_death(df)
    total_sumbuh = total_recovery(df)

    data = {
        'Status': ['Meninggal', 'Sembuh'],
        'Jumlah': [total_mati, total_sumbuh]
    }

    fig = px.pie(
        data,
        names='Status',
        values='Jumlah',
        title='Perbandingan Total Kematian VS Total Kesembuhan',
        hole=0.5,
        color_discrete_sequence=['#4de89f', '#ff6459']
    )

    st.plotly_chart(fig, use_container_width=True)
def load_data():
    df = pd.read_csv("covid_19_indonesia_time_series_all.csv")
    df = df[df["Location"] != "Indonesia"]
    return df

def filter_data(df, year=None, location=None):
    if year:
        df = df[df['Date'].astype(str).str.contains(str(year))]
    if location:
        df = df[df['Location'].isin(location)]
    return df

def select_location(df):
    locations = sorted(df['Location'].unique())
    return st.sidebar.multiselect(
        "Pilih Provinsi",
        options=locations
    )

def select_year():
    selected = st.sidebar.selectbox(
        "Pilih Tahun",
        options=["Semua Tahun", 2020, 2021, 2022]
    )
    return None if selected == "Semua Tahun" else selected

def show_data():
    df = load_data()
    st.subheader("Tabel Data")
    st.dataframe(df)

    st.subheader("Informasi Dataset")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"Jumlah Baris: {df.shape[0]}")
        st.write(f"Jumlah Kolom: {df.shape[1]}")
    with col2:
        st.write(f"Kolom: {', '.join(df.columns.tolist())}")

    st.subheader("Statistik Deskriptif")
    st.dataframe(df.describe())

def total_case(df):
    total_kasus = df.sort_values('Date').groupby('Location', as_index=False).last()
    return total_kasus['Total Cases'].sum()

def total_death(df):
    total_mati = df.sort_values('Date').groupby('Location', as_index=False).last()
    return total_mati['Total Deaths'].sum()

def total_recovery(df):
    total_sembuh = df.sort_values('Date').groupby('Location', as_index=False).last()
    return total_sembuh['Total Recovered'].sum()

def kolom(df):
    kasus = total_case(df)
    kematian = total_death(df)
    sembuh = total_recovery(df)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Kasus", f"{kasus:,}")
    with col2:
        st.metric("Total Kematian", f"{kematian:,}")
    with col3:
        st.metric("Total Sembuh", f"{sembuh:,}")
