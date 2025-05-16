import streamlit as st
import requests

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
        data = requests.post('http://localhost:1111/login',
                             params=params).json()
        if data['status'] == 200:
            st.switch_page('home.py')
        elif data['status'] == 401:
            st.error('Invalid credentials', icon=':material/error:')
        else:
            st.error('Server error', icon=':material/error:')

if signup_btn:
    st.switch_page('signup.py')