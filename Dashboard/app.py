import streamlit as st
from data import *

st.set_page_config(page_title="Dashboard COVID-19 Indonesia", layout="wide")

def judul():
    st.title("Dashboard COVID-19 Indonesia")
    st.write("Selamat datang di Dashboard interaktif data COVID-19 Indonesia.")

st.sidebar.title("Navigasi")
menu = st.sidebar.radio("Pilih Halaman", ["Home", "Data"])

if menu == "Home":
    judul()
    df = load_data()
    year = select_year()
    location = select_location(df)
    df_filtered = filter_data(df, year, location)
    kolom(df_filtered)
    pie_chart1(df_filtered)
    bar_chart1(df_filtered)
    bar_chart2(df_filtered)
    map_chart(df_filtered, year)
    

elif menu == "Data":
    judul()
    df = load_data()
    year = select_year()
    location = select_location(df)
    df_filtered = filter_data(df, year, location)
    show_data(df_filtered)  

st.markdown("---")
st.markdown("© 2026 Fayme Findarandy / 184240034. All Rights Reserved.")
