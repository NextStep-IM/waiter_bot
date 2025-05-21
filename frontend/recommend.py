import streamlit as st
import pandas as pd
from pathlib import Path
from backend.model import Recommender

@st.cache_data
def load_dataframe(path) -> pd.DataFrame:
    return pd.read_csv(path)

