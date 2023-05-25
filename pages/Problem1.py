import pandas as pd
import streamlit as st
from streamlit_pandas_profiling import st_profile_report
import ydata_profiling as yp
import calendar
import numpy as np

st.set_page_config(layout="wide", page_title='Problem 1')

@st.cache_data(experimental_allow_widgets=True)
def load_csv():
    csv = pd.read_csv('EDA_Gold_Silver_prices.csv')
    return csv

if 'selected_month_filter' not in st.session_state:
    st.session_state['selected_month_filter'] = []

if 'selected_year_filter' not in st.session_state:
    st.session_state['selected_year_filter'] = []

if 'gold_silver_data' not in st.session_state:
    st.session_state['gold_silver_data'] = load_csv()

if 'gold_silver_filtered_data' not in st.session_state:
    st.session_state['gold_silver_filtered_data'] = load_csv()

if 'filter_flag' not in st.session_state:
    st.session_state['filter_flag'] = False

def correlations():
    correlation = st.session_state['gold_silver_filtered_data'][['SilverPrice', 'GoldPrice']].corr()

    st.write('Correlation Matrix:')
    st.write(correlation)

@st.cache_data
def unique_months():
    months = range(1, 13)
    month_names = []
    for month in months:
        month_name = calendar.month_name[month][:3]
        month_names.append(month_name)
    return month_names

@st.cache_data
def unique_years():
    return st.session_state['gold_silver_data']['Month'].str.split('-').str[1].unique()

def time_filters_ui():
    st.session_state['selected_month_filter'] = st.sidebar.multiselect('Select Months', options=unique_months())
    st.session_state['selected_year_filter'] = st.sidebar.multiselect('Select Years', options=unique_years())

@st.cache_data
def filter_month_data(data, months):
    month_filter_str = '|'.join(months)
    print('filter month_filter_str *****************************************************', month_filter_str)
    return data[data['Month'].str.contains(month_filter_str)]

@st.cache_data
def filter_years_data(data, years):
    year_filter_str = '|'.join(years)
    return data[data['Month'].str.contains(year_filter_str)]

@st.cache_data
def filter_data(data, months, years):
    months_count = len(months)
    years_count = len(years)
    filtered_data = []

    if months_count > 0 and years_count > 0:
        filtered_data = filter_month_data(filter_years_data(data, years), months)
    elif months_count > 0:
        filtered_data = filter_month_data(data, months)
    elif years_count > 0:
        filtered_data = filter_years_data(data, years)
    else:
        filtered_data = data

    return filtered_data

@st.cache_data()
def eda_report(data):
    return yp.ProfileReport(st.session_state['gold_silver_filtered_data'], explorative=True, dark_mode=True,
    correlations={
        "auto": {"calculate": True},
        "pearson": {"calculate": True},
        "spearman": {"calculate": True},
        "kendall": {"calculate": True},
        "phi_k": {"calculate": True},
        "cramers": {"calculate": True},
    })

def data_frame_ui():
    st.header('**Dataframe**', anchor=False)
    st.dataframe(st.session_state['gold_silver_filtered_data'])
    st.divider()

def profile_report_ui(report):    
    st_profile_report(report)

def app():
    st.title('**Problem 1 - Gold & Silver Exploratory Data Analysis**', anchor=False)
    # filter_button = time_filters_ui()
    time_filters_ui()
    st.session_state['gold_silver_filtered_data'] = filter_data(st.session_state['gold_silver_data'], st.session_state['selected_month_filter'], st.session_state['selected_year_filter'])
    if len(st.session_state['gold_silver_filtered_data']) == 0:
        st.success('No data found for the filter criteria!')
    else:
        correlations()
        data_frame_ui()
        report = eda_report(st.session_state['gold_silver_filtered_data'])
        print("**************************************** report", report.config)
        print("**************************************** report")
        profile_report_ui(report)

if __name__ == '__main__':
    app()