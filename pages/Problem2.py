import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title='Problem 2')

@st.cache_data
def load_csv():
    csv = pd.read_csv("currencies.csv")
    return csv

if 'currencies_data' not in st.session_state:
    st.session_state['currencies_data'] = st.session_state['currencies_data_backup'] = pd.DataFrame(load_csv())

if 'append_counter' not in st.session_state:
    st.session_state['append_counter'] = 0

if 'format' not in st.session_state:
    st.session_state['format'] = 'wide'

# Append another month of data
def append_data():

    currencies_data_copy = st.session_state['currencies_data_backup'].copy()
    if st.session_state['format'] == 'long':
        currencies_data_copy = pd.melt(currencies_data_copy, id_vars=['Date'], var_name='Currency', value_name='Exchange Rate')
        
    num_duplicates = len(currencies_data_copy)

    currencies_data_copy = currencies_data_copy.iloc[::-1]

    st.session_state['append_counter'] = st.session_state['append_counter'] + 1
    for i in range(num_duplicates):
        last_date = datetime.strptime(st.session_state['currencies_data'].iloc[i, 0], '%B %d, %Y')
        days = 31*st.session_state['append_counter']
        new_date = last_date + timedelta(days=days)
        new_date_string = new_date.strftime("%B %d, %Y")
        currencies_data_copy.iloc[i, 0] = new_date_string

    st.session_state['currencies_data'] = pd.concat([st.session_state['currencies_data'], currencies_data_copy], ignore_index=True)
    st.success('Data appended successfully!')

# Convert data from wide to long format
def long_format_conversion():
    st.session_state['currencies_data'] = pd.melt(st.session_state['currencies_data'], id_vars=['Date'], var_name='Currency', value_name='Exchange Rate')
    st.session_state['format'] = 'long'
    st.success('Data converted to long format successfully!')

def app():
    
    st.title('''**Problem 2 - Currency Exchange Rates Analysis**''', anchor=False)

    st.header('**Dataframe**')

    plotdata = st.session_state['currencies_data'].copy()
    if st.session_state['format'] == 'long':
        plotdata['Exchange Rate'] = plotdata['Exchange Rate'].astype(str)

    st.session_state['exp_dataframe'] = st.experimental_data_editor(plotdata, key='exp_change_data', num_rows='dynamic', use_container_width=True)

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        data_frame_temp = st.session_state['exp_dataframe']
        # data_frame_temp2 = data_frame_temp.drop(data_frame_temp.columns[0], axis=1, inplace=True)
        csv_data = data_frame_temp.to_csv(index=False).encode('utf-8')
        if st.download_button('Save & Download', csv_data, file_name='currencies_v1.csv'):
            st.success('Data saved to currencies_v1.csv successfully!')

    with col2:
        st.button('Append Another Month of Data', on_click=append_data)

    with col3:
        if st.session_state['format'] == 'wide':
            st.button('Convert Data to Long Format', on_click=long_format_conversion)
    
    st.divider()

    if st.session_state['format'] == 'long':
        dataframe_ts = st.session_state['currencies_data'].copy()
        dataframe_ts['Date'] = pd.to_datetime(dataframe_ts['Date']).dt.strftime('%b %d')

        dataframe_ts['Exchange Rate'] = dataframe_ts['Exchange Rate'].astype(str)

        # Create a dropdown menu to select the currency to visualize
        currencies = dataframe_ts['Currency'].unique()
        default_currencies = ["Euro","Japanese Yen","U.K. Pound Sterling","U.S. Dollar","Chinese Yuan","Australian Dollar","Indian Rupee"]
        selected_currencies = st.multiselect("Select currency", options=currencies, default=default_currencies)

        # Filter data based on selected currencies
        filtered_data2 = {currency: dataframe_ts[dataframe_ts["Currency"] == currency] for currency in selected_currencies}

        fig = go.Figure()
        for currency, dff in filtered_data2.items():
            fig = fig.add_trace(go.Scatter(x=dff["Date"], y=dff["Exchange Rate"], name=currency))

        st.plotly_chart(fig, use_container_width=True)

if __name__ == '__main__':
    app()