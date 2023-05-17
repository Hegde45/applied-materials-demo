import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

st.set_page_config(layout="wide", page_title='Problem 4')

@st.cache_data
def load_csv():
    csv = pd.read_csv("train.csv")
    if 'Id' in csv:
        del csv['Id']
    return csv

if 'train_data' not in st.session_state:
    st.session_state['train_data'] = pd.DataFrame(load_csv())

# Calculate summary statistics
@st.cache_data
def summary_stats():
    stats = st.session_state['train_data'].describe()
    st.write(stats)

# Display the correlation
@st.cache_data
def heatmap(threshold_flag):

    df = st.session_state['train_data'].copy()

    for column in df.columns:
        if df[column].dtype == 'object': 
            df[column]=df[column].astype('category').cat.codes

    correlation_matrix = df.corr()
    if threshold_flag == True:
        threshold = 0.5
        correlation_matrix = correlation_matrix[((correlation_matrix >= threshold) | (correlation_matrix <= -threshold)) & (correlation_matrix != 1.000)]

    plt.figure(figsize=(60, 40), dpi = 1000)
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', xticklabels=correlation_matrix.columns, yticklabels=correlation_matrix.columns)
    plt.xticks(rotation=45)
    plt.tick_params(axis = 'x', labelsize = 16)
    plt.yticks(rotation=45)
    plt.tick_params(axis = 'y', labelsize = 16)
    plt.tight_layout()
    st.pyplot(plt)

# @st.cache_data
# def heatmap_high_correlations():
#     df = st.session_state['train_data'].copy()
#     for column in df.columns:
#         if df[column].dtype == 'object': 
#             df[column]=df[column].astype('category').cat.codes
            
#     correlation_matrix = df.corr()
   
#     plt.figure(figsize=(50, 20))
#     sns.heatmap(filtered_corr_df, annot=True, cmap='coolwarm', xticklabels=correlation_matrix.columns, yticklabels=correlation_matrix.columns, cbar=1, square=1, annot_kws={'size': 15})
#     plt.xticks(rotation=90)
#     plt.yticks(rotation=0)

#     plt.tight_layout()
#     st.pyplot(plt)

# Display the scatter plots
@st.cache_data
def scatter_plot(selected_features):
    for feature in selected_features:
        plt.figure(figsize=(8, 6))
        sns.scatterplot(x=feature, y='SalePrice', data=st.session_state['train_data'])
        st.pyplot(plt)

def app():
    
    st.title('''**Problem 4 - Housing Prices Analysis**''', anchor=False)
    
    st.subheader('Dataframe', anchor=False)
    st.dataframe(st.session_state['train_data'], use_container_width=True)

    st.subheader('Summary Statistics', anchor=False)
    summary_stats()

    # heat map
    st.subheader('All Correlations', anchor=False)
    heatmap(False)

    st.subheader('High Correlations', anchor=False)
    heatmap(True)
        
    # scatter plot
    st.subheader('Scatter plot', anchor=False)
    selected_features = st.multiselect('Select features to plot against sale price', st.session_state['train_data'].columns)
    scatter_plot(selected_features)

if __name__ == '__main__':
    app()