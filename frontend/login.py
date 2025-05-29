import streamlit as st
import requests
from typing import Tuple
from flask import Response

if "http_session" not in st.session_state:
    st.session_state.http_session = requests.Session()

# Login
st.markdown("<h1 style='text-align: center;'>Login</h1>", unsafe_allow_html=True)
st.write('- - -')
username_field = st.text_input('Enter username: ', placeholder='hitchhiker42', max_chars=20)
password_field = st.text_input('Enter password: ', type='password', max_chars=20)
login_btn = st.button('Login')

# Sign Up
st.text('\n')
st.markdown(':small[Don\'t have an account?]')
signup_btn = st.button('Sign Up')

if login_btn:
    if not (username_field and password_field):
        st.error('Please fill all the fields', icon=':material/error:')
    else:
        params = {'name': username_field, 'password': password_field}
        response = st.session_state.http_session.post('http://localhost:1111/login',
                             json=params).json()
        if response['success']:
            st.switch_page('home.py')
        else:
            st.error(response['message'], icon=':material/error:')

if signup_btn:
    st.switch_page('signup.py')