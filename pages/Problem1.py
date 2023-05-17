import pandas as pd
import streamlit as st
import ydata_profiling as ydp
from streamlit_pandas_profiling import st_profile_report

st.set_page_config(layout="wide", page_title='Problem 1')

@st.cache_data
def load_csv():
    csv = pd.read_csv('EDA_Gold_Silver_prices.csv')
    return csv

def app():
    st.title('**Problem 1 - Gold & Silver Exploratory Data Analysis**', anchor=False)
    gold_silver_data = load_csv()
    profile_report = ydp.ProfileReport(gold_silver_data, explorative=True)
    st.header('**Dataframe**')
    st.write(gold_silver_data)
    st_profile_report(profile_report)

if __name__ == '__main__':
    app()