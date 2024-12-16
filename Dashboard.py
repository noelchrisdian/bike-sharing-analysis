import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.header('Dashboard Penyewaan Sepeda')

st.subheader('Rata - Rata Total Penyewaan Sepeda dalam 1 Minggu')

daydf = pd.read_csv('./Dataset/Day.csv')
weekdayMean = daydf.pivot_table(
    index='weekday',
    values='cnt',
    aggfunc='mean').reset_index().sort_values(by='cnt', ascending=False)
plt.figure(figsize=(10, 5))
sns.barplot(y='cnt',
            x='weekday',
            data=weekdayMean,
            color='blue')
plt.title('Penyewaan Sepeda')
plt.ylabel(None)
plt.xlabel(None)
st.pyplot(plt)

st.subheader('Hari dengan Total Penyewaan Sepeda Tertinggi')

weekdayMax = daydf.pivot_table(
    index='weekday',
    values='cnt',
    aggfunc='max').reset_index().sort_values(by=('cnt'), ascending=False)
plt.figure(figsize=(10, 5))
sns.barplot(y='cnt',
            x='weekday',
            data=weekdayMax.sort_values(by='cnt', ascending=True),
            color='blue')
plt.title('Penyewaan Sepeda')
plt.ylabel(None)
plt.xlabel(None)
st.pyplot(plt)

st.subheader(
    'Perbedaan Rata - Rata Total Penyewaan Sepeda pada Hari Kerja dan Libur')

workingday = daydf.pivot_table(
    index='workingday',
    values='cnt',
    aggfunc=['mean', 'max', 'min']).reset_index()

workingday.columns = ['workingday', 'mean', 'max', 'min']
workingday = workingday.melt(id_vars='workingday',
                             var_name='aggfunc',
                             value_name='cnt')
plt.figure(figsize=(10, 5))
sns.barplot(
    data=workingday,
    y='cnt',
    x='workingday',
    hue='aggfunc',
    errorbar=None
)
plt.title('Penyewaan Sepeda')
plt.ylabel(None)
plt.xlabel(None)
st.pyplot(plt)

st.subheader('Jam dengan Total Penyewaan Sepeda Tertinggi')

hourdf = pd.read_csv('./Dataset/Hour.csv')
hourMax = hourdf.pivot_table(
    index='hr',
    values='cnt',
    aggfunc='max').reset_index().sort_values(by='cnt', ascending=False)

plt.figure(figsize=(10, 5))
sns.barplot(y='cnt',
            x='hr',
            data=hourMax,
            color='blue')
plt.title('Penyewaan Sepeda')
plt.ylabel(None)
plt.xlabel(None)
st.pyplot(plt)

st.subheader('Pengaruh Cuaca terhadap Rata - Rata Total Penyewaan Sepeda')

weather = daydf.pivot_table(
    index='weathersit', values='cnt', aggfunc='mean').reset_index()

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

st.subheader('Perbedaan antara Penyewa yang Terdaftar dengan yang Tidak')

users = daydf.pivot_table(
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