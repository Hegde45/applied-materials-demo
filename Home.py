import streamlit as st

st.set_page_config(layout="wide", page_title='Solutions')

def app():

    st.title('**Solutions Demo App**', anchor=False)

    st.header('**Tech Stack**', anchor=False)
    st.subheader('''**`Python`** **`Streamlit`**''', anchor=False)

    st.header('**Libraries**', anchor=False)
    st.subheader('**`pandas`**\t**`ydata-profiling`**\t**`streamlit-pandas-profiling`**\t**`plotly`**\t**`matplotlib`**\t**`seaborn`**\t', anchor=False)

    st.header('**By**', anchor=False)
    st.subheader('**[Bharat Hegde](https://www.linkedin.com/in/bharat-hegde-402212200/)**', anchor=False)

if __name__ == '__main__':
    app()