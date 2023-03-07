import streamlit as st

st.set_page_config(layout='wide')

st.title('Data Analysis Tools')
st.markdown('---')

col1, col2, col3 = st.columns(3)







button_style = """
        <style>
        .stButton > button {
            color: blue;
            background: gray;
            width: 100px;
            height: 50px;
        }
        </style>
        """

with col1:
    st.button('DVP Analysis')

with col2:
    st.button('Current Sweep')

    st.button('Thermocouples Check')

with col3:
    st.button('Health Check')

st.markdown('---')
st.title('Data Analysis Tools')