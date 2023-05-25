import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
import plotly.graph_objects as go
import calendar

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

if 'selected_months' not in st.session_state:
    st.session_state['selected_months'] = []

if 'months_in_data' not in st.session_state:
    st.session_state['months_in_data'] = [7]


# Append another month of data
def append_data():

    if len(st.session_state['selected_months']) == 0:
        st.error('Please select a month!')
        return

    for monthNum in st.session_state['selected_months']:
        # month_name = calendar.month_name[monthNum]
        print("************************** &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& selected months", st.session_state['selected_months'])
        currencies_data_copy = st.session_state['currencies_data_backup'].copy()
        if st.session_state['format'] == 'long':
            currencies_data_copy = pd.melt(currencies_data_copy, id_vars=['Date'], var_name='Currency', value_name='Exchange Rate')
            
        for index, row in currencies_data_copy.iterrows():
            date_object = datetime.strptime(row['Date'], "%B %d, %Y")
            date_num = date_object.day

            new_date_object = datetime(2016, monthNum, date_num)
            new_date_str = new_date_object.strftime("%B %d, %Y")
            currencies_data_copy.at[index, 'Date'] = new_date_str

        st.session_state['months_in_data'].append(monthNum)
        st.session_state['currencies_data'] = pd.concat([st.session_state['currencies_data'], currencies_data_copy], ignore_index=True)
        st.session_state[monthNum] = False
    transform_sort()
    st.success('Data appended successfully!')
    st.session_state['selected_months'] = []

def transform_sort():
    st.session_state['currencies_data']['Date'] = pd.to_datetime(st.session_state['currencies_data']['Date'])
    st.session_state['currencies_data'] = st.session_state['currencies_data'].sort_values('Date')
    st.session_state['currencies_data']['Date'] = st.session_state['currencies_data']['Date'].dt.strftime('%B %d, %Y')

def save():
    st.session_state['currencies_data'] = st.session_state['exp_dataframe']

def long_format_conversion():
    try:
        st.session_state['currencies_data'] = pd.melt(st.session_state['currencies_data'], id_vars=['Date'], var_name='Currency', value_name='Exchange Rate')
        st.session_state['format'] = 'long'
        st.success('Data converted to long format successfully!')
    except Exception as e: # work on python 3.x
        print('error', e)

def app():
    
    st.title('''**Problem 2 - Currency Exchange Rates Analysis**''', anchor=False)

    st.header('**Dataframe**', anchor=False)

    plotdata = st.session_state['currencies_data'].copy().reset_index(drop=True)
    print("long", plotdata)
    if st.session_state['format'] == 'long':
        plotdata['Exchange Rate'] = plotdata['Exchange Rate'].astype(str)

    st.session_state['exp_dataframe'] = st.experimental_data_editor(plotdata, key='exp_change_data', num_rows='dynamic', use_container_width=True)

    st.subheader(f'''Data ranges from `{plotdata.iloc[0, 0]}` to `{plotdata.iloc[-1, 0]}`''', anchor=False)

    st.divider()

    columns = st.columns(12)
    columns_list = list(columns)
    for i, column in enumerate(columns_list):
        with column:
            print('******************************************** month', i)
            month_name = calendar.month_name[i+1]
            checkbox_state = st.checkbox(month_name, key=str(i+1), disabled=((i+1) in st.session_state["months_in_data"]))
            if checkbox_state and (i+1) not in st.session_state['selected_months']:
                st.session_state['selected_months'].append(i+1)

    col1, col2, col3, col4 = st.columns([1, 1, 3, 3])

    with col1:
        st.button('Save', on_click=save)
    
    with col2:
        data_frame_temp = st.session_state['exp_dataframe']
        csv_data = data_frame_temp.to_csv(index=False).encode('utf-8')
        if st.download_button('Download', csv_data, file_name='currencies_v1.csv'):
            st.success('Data saved to currencies_v1.csv successfully!')

    with col3:
        st.button('Append Another Month of Data', on_click=append_data)

    with col4:
        if st.session_state['format'] == 'wide':
            st.button('Convert Data to Long Format', on_click=long_format_conversion)
    
    st.divider()

    if st.session_state['format'] == 'long':
        dataframe_ts = st.session_state['currencies_data'].copy()
        dataframe_ts['Date'] = pd.to_datetime(dataframe_ts['Date']).dt.strftime('%b %d')

        dataframe_ts['Exchange Rate'] = dataframe_ts['Exchange Rate'].astype(str)

        currencies = dataframe_ts['Currency'].unique()
        default_currencies = ["Euro","Japanese Yen","U.K. Pound Sterling","U.S. Dollar","Chinese Yuan","Australian Dollar","Indian Rupee"]
        selected_currencies = st.multiselect("Select currency", options=currencies, default=default_currencies)

        filtered_data2 = {currency: dataframe_ts[dataframe_ts["Currency"] == currency] for currency in selected_currencies}

        fig = go.Figure()
        for currency, dff in filtered_data2.items():
            fig = fig.add_trace(go.Scatter(x=dff["Date"], y=dff["Exchange Rate"], name=currency))

        st.plotly_chart(fig, use_container_width=True)

if __name__ == '__main__':
    app()