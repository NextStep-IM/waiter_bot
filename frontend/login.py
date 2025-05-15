import streamlit as st

#st.title('Login')
# Login
st.markdown("<h1 style='text-align: center;'>Login</h1>", unsafe_allow_html=True)
st.write('- - -')
username_field = st.text_input('Enter username: ', placeholder='hitchhiker42', max_chars=20)
password_field = st.text_input('Enter password: ', type='password', max_chars=20)

# Sign Up
st.text('\n')
st.markdown(':small[Don\'t have an account?]')
signup_btn = st.button('Sign Up')

if signup_btn:
    st.switch_page('signup.py')