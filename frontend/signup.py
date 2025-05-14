import streamlit as st

st.markdown("<h1 style='text-align: center;'>Sign Up</h1>", unsafe_allow_html=True)
st.write('- - -')
st.text_input('Enter username:', placeholder='hitchhiker42')
st.text_input('Enter password:', type='password')