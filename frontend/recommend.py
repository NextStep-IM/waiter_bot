import streamlit as st
import pandas as pd
from pathlib import Path
from backend.model import Recommender

@st.cache_data
def load_dataframe(path) -> pd.DataFrame:
    return pd.read_csv(path)

def find_dataset_path():
    parent = Path.cwd()
    while parent.parts[-1] != 'waiter_bot':
        parent = parent.parent
    return parent / 'data' / 'cleaned_recipes.csv'

