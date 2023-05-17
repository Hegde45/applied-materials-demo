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
    for column in st.session_state['train_data'].columns:
        if st.session_state['train_data'][column].dtype == 'object': 
            st.session_state['train_data'][column]=st.session_state['train_data'][column].astype('category').cat.codes

# Calculate summary statistics
@st.cache_data
def summary_stats():
    stats = st.session_state['train_data'].describe()
    st.write(stats)

# Display the correlation
@st.cache_data
def heatmap_all_correlations():

    df = st.session_state['train_data'].copy()

    correlation_matrix = df.corr()
    plt.figure(figsize=(100, 60), dpi=400)
    sns.heatmap(correlation_matrix, annot=True, cmap='Blues', xticklabels=correlation_matrix.columns, yticklabels=correlation_matrix.columns, cbar=1, square=1, annot_kws={'size': 15})
    plt.tick_params(axis = 'x', labelsize = 26)
    plt.tick_params(axis = 'y', labelsize = 26)
    plt.xticks(rotation=90)
    plt.yticks(rotation=0)
    plt.tight_layout()
    st.pyplot(plt)

@st.cache_data
def heatmap_high_correlations():
    df = st.session_state['train_data'].copy()
    for column in df.columns:
        if df[column].dtype == 'object': 
            df[column]=df[column].astype('category').cat.codes
            
    correlation_matrix = df.corr()
    threshold = 0.5
    filtered_corr_df = correlation_matrix[((correlation_matrix >= threshold) | (correlation_matrix <= -threshold)) & (correlation_matrix != 1.000)]

    plt.figure(figsize=(60, 40), dpi=300)
    sns.heatmap(filtered_corr_df, annot=True, cmap='Blues', xticklabels=correlation_matrix.columns, yticklabels=correlation_matrix.columns, cbar=1, square=1, annot_kws={'size': 15})
    plt.tick_params(axis = 'x', labelsize = 18)
    plt.tick_params(axis = 'y', labelsize = 18)
    plt.xticks(rotation=90)
    plt.yticks(rotation=0)

    plt.tight_layout()
    st.pyplot(plt)

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

    # # heat map
    st.subheader('All Correlations', anchor=False)
    heatmap_all_correlations()

    st.subheader('High Correlations', anchor=False)
    heatmap_high_correlations()
        
    # scatter plot
    st.subheader('Scatter plot', anchor=False)
    selected_features = st.multiselect('Select features to plot against sale price', st.session_state['train_data'].columns)
    scatter_plot(selected_features)

    st.subheader('summary numeric', anchor=False)
    numeric_cols = st.session_state['train_data'].select_dtypes(include=['int64', 'float64'])
    summary_stats2 = numeric_cols.describe()
    st.dataframe(summary_stats2)

    st.subheader('summary categorical', anchor=False)
    categorical_cols = st.session_state['train_data'].select_dtypes(include=['int8'])
    summary_stats3 = categorical_cols.describe()
    st.dataframe(summary_stats3)

    # group 1 - scatter matrix plot
    subset_variables_array = [
        ['MSSubClass','MSZoning','LotFrontage','LotArea','Street','Alley','LotShape','LandContour','Utilities','LotConfig','LandSlope','Neighborhood']
        ['Condition1','Condition2','BldgType','HouseStyle','OverallQual','OverallCond','YearBuilt','YearRemodAdd']
        ['RoofStyle','RoofMatl','Exterior1st','Exterior2nd','MasVnrType','MasVnrArea','ExterQual','ExterCond']
        ['Foundation','BsmtQual','BsmtCond','BsmtExposure','BsmtFinType1','BsmtFinSF1','BsmtFinType2','BsmtFinSF2','BsmtUnfSF','TotalBsmtSF']
        ['Heating','HeatingQC','CentralAir','Electrical','1stFlrSF','2ndFlrSF','LowQualFinSF','GrLivArea']
        ['BsmtFullBath','BsmtHalfBath', 'FullBath','HalfBath','BedroomAbvGr']
        ['KitchenAbvGr','KitchenQual','TotRmsAbvGrd','Functional','Fireplaces','FireplaceQu']
        ['GarageType','GarageYrBlt','GarageFinish','GarageCars','GarageArea','GarageQual','GarageCond','PavedDrive','WoodDeckSF']
        ['OpenPorchSF','EnclosedPorch','3SsnPorch','ScreenPorch','PoolArea','PoolQC','Fence','MiscFeature','MiscVal','MoSold','YrSold','SaleType','SaleCondition']
    ]
    for index, item in enumerate(subset_variables_array):
        # Creating the scatter matrix plot
        name = 'Scatter matrix plot - Category ' + str(index + 1)
        st.subheader(name, anchor=False)
        subset_df = st.session_state['train_data'][item]
        sns.set(style="ticks")
        sns.pairplot(subset_df)
        st.pyplot(plt)

if __name__ == '__main__':
    app()