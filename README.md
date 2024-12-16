SETUP ENVIRONTMENT
python create --name main-ds python=3.9
python activate main-ds
pip install pandas matplotlib seaborn streamlit

RUN STREAMLIT 

Jika module streamlit di dalam PATH :
streamlit run Dashboard.py

Jika module streamlit di luar PATH :
python -m streamlit run Dashboard.py
