import pandas as pd
import streamlit as st

st.set_page_config(layout="wide", page_title='Problem 3')

@st.cache_data
def load_csv():
    csv = pd.read_csv("sales.csv")
    return csv

@st.cache_data
def load_csv2():
    csv = pd.read_csv("storedemo.csv")
    return csv

# Initialize or retrieve the session state
if 'sales_data' not in st.session_state:
    st.session_state['sales_data'] = pd.DataFrame(load_csv())

if 'store_data' not in st.session_state:
    st.session_state['store_data'] = pd.DataFrame(load_csv2())

def app():
    
    st.title('''**Problem 3 - Dominick's Orange Juice Dataset Analysis**''', anchor=False)
    
    if 'Unnamed: 0' in st.session_state['sales_data']:
        del st.session_state['sales_data']['Unnamed: 0']
    if 'Unnamed: 0' in st.session_state['store_data']:
        del st.session_state['store_data']['Unnamed: 0']

    if 'Units Sold' not in st.session_state['sales_data']:
        st.session_state['sales_data']['Units Sold'] = st.session_state['sales_data']['logmove'].apply(lambda x: round(pow(10, x)))

    st.header("Sales Dataframe", anchor=False)
    st.dataframe(st.session_state['sales_data'], use_container_width=True)
    st.write("To get the number of units sold, an exponential transform has been applied to logmove column and resulting data has been written to **Units Sold** column")

    st.header("Stores Dataframe", anchor=False)
    st.dataframe(st.session_state['store_data'], use_container_width=True)

    st.header("Joined Dataframe", anchor=False)
    merge_data = st.session_state['sales_data'].merge(st.session_state['store_data'], left_on='store', right_on='STORE', how='inner')
    if 'STORE' in merge_data:
        del merge_data['STORE']
    st.dataframe(merge_data, use_container_width=True)

if __name__ == '__main__':
    app()
