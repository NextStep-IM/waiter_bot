import streamlit as st

pages = {
    'account': [
        st.Page('login.py', title='Login'),
        st.Page('signup.py', title='Sign Up'),
    ],
    'home': [st.Page('home.py', title='Home')],
    'recommend': [st.Page('recommend.py', title='Recommend')]
}

pg = st.navigation(pages, position='hidden')
pg.run()