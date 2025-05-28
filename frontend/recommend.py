import streamlit as st
import pandas as pd
from pathlib import Path
from backend.model import Recommender

@st.cache_data
def load_dataframe(path) -> pd.DataFrame:
    return pd.read_csv(path)

def find_absolute_path(filename: str):
    """
    Find the dataset from the main directory. Since a streamlit
    app can be run from any directory, hard-coded paths cause FileNotFoundException.
    This is the fix for that with the limitation that it does not go back from the main directory.

    :param filename: The file to find
    :return: Absolute path to the file
    """
    parent = Path.cwd()
    while parent.parts[-1] != 'waiter_bot':
        parent = parent.parent
    return parent / 'data' / filename

df = load_dataframe(find_dataset_path())
categories = list(df['RecipeCategory'].unique())

selected_cat = st.selectbox('Choose a category:', ['All'] + categories)

#rec = Recommender(df, df.sample(20))

if st.button('Apply'):
    if selected_cat != 'All':
        # recipes = rec.recommend_recipes(selected_cat)
        pass
    else:
        #recipes = rec.recommend_recipes()
        pass