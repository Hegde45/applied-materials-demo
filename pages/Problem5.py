import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(layout="wide", page_title='Problem 5')

@st.cache_data
def load_csv():
    csv = pd.read_csv("covid_tracking.csv")
    return csv

# Initialize or retrieve the session state
if 'covid_data' not in st.session_state:
    st.session_state['covid_data'] = st.session_state['covid_data_backup'] = pd.DataFrame(load_csv())

def app():
    st.title('''**Problem 5 - Covid Tracking Time Series Analysis**''', anchor=False)
    st.header('Dataframe', anchor=False)
    df = st.session_state['covid_data']
    df = df.rename(columns={'total_test_results': 'Total Test Results'})
    df = df.rename(columns={'positive': 'Confirmed Cases'})
    df = df.rename(columns={'hospitalized_cumulative': 'Hospitalizations'})
    df = df.rename(columns={'recovered': 'Recovery'})
    df = df.rename(columns={'death': 'Death'})
    df = df.rename(columns={'date': 'Date'})

    st.dataframe(df, use_container_width=True)
    criteria = ["Total Test Results", "Confirmed Cases", "Hospitalizations", "Recovery", "Death"]
    for index, item in enumerate(criteria):
        data = df[['Date', 'state', item]]
        fig = px.line(data, x='Date', y=item, color='state',
                    title=f'{item} by State')
        st.plotly_chart(fig, use_container_width=True)

if __name__ == '__main__':
    app()