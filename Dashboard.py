import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

daydf = pd.read_csv('./Dataset/Day.csv')
hourdf = pd.read_csv('./Dataset/Hour.csv')

st.set_page_config(layout='wide')
st.title('Dashboard Bike Sharing Dataset Analyst')
col1, col2 = st.columns(2)

with col1:
    daydf['dteday'] = pd.to_datetime(daydf['dteday'], errors='coerce')
    hourdf['dteday'] = pd.to_datetime(hourdf['dteday'], errors='coerce')

    selected_date = st.date_input('Date', min_value=daydf['dteday'].min().date(), max_value=daydf['dteday'].max().date(), value=(pd.to_datetime('2011-12-08'), pd.to_datetime('2011-12-15')))

    filter_day = daydf[(daydf['dteday'] >= pd.to_datetime(selected_date[0])) & (daydf['dteday'] <= pd.to_datetime(selected_date[1]))]
    filter_hour = hourdf[(hourdf['dteday'] >= pd.to_datetime(selected_date[0])) & (hourdf['dteday'] <= pd.to_datetime(selected_date[1]))]

with col2:
    st.text('Rata - Rata Total Penyewaan Sepeda dalam 1 Minggu')
    filter_day['weekday'] = filter_day['weekday'].replace(
        {0: 'Minggu', 1: 'Senin', 2: 'Selasa', 3: 'Rabu', 4: 'Kamis', 5: 'Jumat', 6: 'Sabtu'})
    day_order = ['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu']
    filter_day['weekday'] = pd.Categorical(
        filter_day['weekday'], categories=day_order, ordered=True)
    weekdayMean = filter_day.pivot_table(
        index='weekday',
        values='cnt',
        aggfunc='mean').reset_index().sort_values(by='weekday')
    plt.figure(figsize=(10, 5))
    sns.barplot(y='cnt',
                x='weekday',
                data=weekdayMean,
                color='blue')
    plt.title('Penyewaan Sepeda')
    plt.ylabel('Total')
    plt.xlabel('Hari')
    st.pyplot(plt)

    st.text('Hari dengan Total Penyewaan Sepeda Tertinggi')
    weekdayMax = filter_day.pivot_table(
        index='weekday',
        values='cnt',
        aggfunc='max').reset_index().sort_values(by=('cnt'), ascending=False)
    plt.figure(figsize=(10, 5))
    sns.barplot(y='cnt',
                x='weekday',
                data=weekdayMax.sort_values(by='cnt', ascending=True),
                color='blue')
    plt.title('Penyewaan Sepeda')
    plt.ylabel('Total')
    plt.xlabel('Hari')
    st.pyplot(plt)

    st.text(
        'Perbedaan Rata - Rata Total Penyewaan Sepeda pada Hari Kerja dan Libur')
    workingday = filter_day.pivot_table(
        index='workingday',
        values='cnt',
        aggfunc='mean').reset_index()
    workingday['workingday'] = workingday['workingday'].replace(
        {0: 'Hari Libur', 1: 'Hari Kerja'})
    plt.figure(figsize=(8, 5))
    sns.barplot(
        data=workingday,
        x='workingday',
        y='cnt',
        hue='workingday',
        palette={'Hari Libur': 'blue', 'Hari Kerja': 'orange'}
    )
    plt.title('Penyewaan Sepeda')
    plt.xlabel(None)
    plt.ylabel('Total')
    st.pyplot(plt)

    st.text('Jam dengan Total Penyewaan Sepeda Tertinggi')
    hourMax = filter_hour.pivot_table(
        index='hr',
        values='cnt',
        aggfunc='max').reset_index().sort_values(by='cnt', ascending=False)
    plt.figure(figsize=(10, 5))
    sns.barplot(y='cnt',
                x='hr',
                data=hourMax,
                color='blue')
    plt.title('Penyewaan Sepeda')
    plt.ylabel('Total')
    plt.xlabel('Jam')
    st.pyplot(plt)

    st.text('Pengaruh Cuaca terhadap Rata - Rata Total Penyewaan Sepeda')
    weather = filter_day.pivot_table(
        index='weathersit', values='cnt', aggfunc='mean').reset_index()
    weather['weathersit'] = weather['weathersit'].replace(
        {1: 'Cerah', 2: 'Berawan', 3: 'Hujan Ringan'})
    plt.figure(figsize=(10, 5))
    sns.barplot(
        y='weathersit',
        x='cnt',
        data=weather,
        orient='h',
        color='blue')
    plt.xlabel('Total Penyewa')
    plt.ylabel('Cuaca')
    plt.title('Penyewaan Sepeda')
    st.pyplot(plt)

    st.text('Perbedaan antara Penyewa yang Terdaftar dengan yang Tidak')
    users = filter_day.pivot_table(
        index='cnt',
        values=['casual', 'registered']).reset_index()
    totalCasual = users['casual'].sum()
    totalRegistered = users['registered'].sum()
    sizes = [totalCasual, totalRegistered]
    labels = ['Casual', 'Registered']
    colors = ('blue', 'lightblue')
    explode = (0.1, 0)
    fig, ax = plt.subplots()
    ax.pie(
        sizes,
        labels=labels,
        autopct='%1.1f%%',
        colors=colors,
        explode=explode
    )
    ax.axis('equal')
    st.pyplot(fig)