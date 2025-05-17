import requests
import streamlit as st

# Sign Up
st.markdown("<h1 style='text-align: center;'>Sign Up</h1>", unsafe_allow_html=True)
st.write('- - -')
username_field = st.text_input('Enter username:', placeholder='hitchhiker42')
password_field = st.text_input('Enter password:', type='password')
signup_btn = st.button('Sign Up')

# Login
st.text('\n')
st.markdown(':small[Already have an account?]')
login_btn = st.button('Login')
if login_btn:
    st.switch_page('login.py')

if signup_btn:
    if not (username_field and password_field):
        st.error('Please fill all the fields.', icon=':material/error:')
    else:
        params = {'name': username_field, 'password': password_field}
        response = requests.post('http://localhost:1111/signup',
                                 json=params).json()
        print(f'Response: {response}')
        if response['success']:
            st.switch_page('login.py')
        else:
            st.error(response['message'], icon=':material/error:')