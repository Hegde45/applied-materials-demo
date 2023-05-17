import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import numpy as np

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
        # Convert logmove column to numeric and apply exponential transform
        st.session_state['sales_data']['logmove'] = pd.to_numeric(st.session_state['sales_data']['logmove'])
        st.session_state['sales_data']['Units Sold'] = np.exp(st.session_state['sales_data']['logmove'])

        # Check for outliers
        st.write('units sold describe')
        st.write(st.session_state['sales_data']['Units Sold'].describe())

    st.header("Sales Dataframe", anchor=False)
    st.dataframe(st.session_state['sales_data'], use_container_width=True)
    st.write("To get the number of units sold, an exponential transform has been applied to logmove column and resulting data has been written to **Units Sold** column")

    st.header("Sales Summary Statistics", anchor=False)
    st.dataframe(st.session_state['sales_data'].describe())

    st.header("Stores Dataframe", anchor=False)
    st.dataframe(st.session_state['store_data'], use_container_width=True)

    st.header("Stores Summary Statistics", anchor=False)
    st.dataframe(st.session_state['store_data'].describe())

    st.header("Joined Dataframe", anchor=False)
    merge_data = st.session_state['sales_data'].merge(st.session_state['store_data'], left_on='store', right_on='STORE', how='inner')
    if 'STORE' in merge_data:
        del merge_data['STORE']
    st.dataframe(merge_data, use_container_width=True)

    st.header("Joined Summary Statistics", anchor=False)
    st.dataframe(merge_data.describe())

    # Distribution of sales
    plt.figure(figsize=(10, 6))
    sns.histplot(merge_data['Units Sold'], bins=20, kde=True)
    plt.title('Distribution of Units Sold')
    plt.xlabel('Units Sold')
    plt.ylabel('Frequency')
    st.pyplot(plt)

    # Correlation heatmap
    merge_data_copy = merge_data.copy()
    if 'constant' in merge_data_copy:
        del merge_data_copy['constant']
    plt.figure(figsize=(60, 40), dpi=300)
    sns.heatmap(merge_data_copy.corr(), annot=True, cmap='Blues', annot_kws={'size': 15})
    plt.title('Correlation Heatmap', fontsize = 50)
    plt.tick_params(axis = 'x', labelsize = 26)
    plt.tick_params(axis = 'y', labelsize = 26)
    plt.xticks(rotation=90)
    plt.yticks(rotation=0)
    plt.tight_layout()
    st.pyplot(plt)

    # Box plots
    plt.figure(figsize=(60, 40), dpi=300)
    sns.boxplot(data=merge_data, x='brand', y='Units Sold')
    plt.xlabel('Brand')
    plt.ylabel('Units Sold')
    plt.title('Box Plot of Units Sold by Brand')
    st.pyplot(plt)

    # Scatter plot
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=merge_data, x='INCOME', y='Units Sold')
    plt.xlabel('Income')
    plt.ylabel('Units Sold')
    plt.title('Scatter Plot of Units Sold vs Income')
    st.pyplot(plt)

    # Bar plot
    avg_units_sold_by_brand = merge_data.groupby('brand')['Units Sold'].mean()
    plt.figure(figsize=(10, 6))
    sns.barplot(x=avg_units_sold_by_brand.index, y=avg_units_sold_by_brand.values)
    plt.xlabel('Brand')
    plt.ylabel('Average Units Sold')
    plt.title('Average Units Sold by Brand')
    st.pyplot(plt)

if __name__ == '__main__':
    app()
