import streamlit as st

st.markdown("<h1 style='text-align: center;'>Hello!</h1>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center;'>I am WaiterBot!</h1>", unsafe_allow_html=True)
st.text('\n\n')
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    rec_btn = st.button('Recommend Me Recipes!')