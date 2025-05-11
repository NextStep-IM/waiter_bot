import joblib
import pandas as pd

PIPELINE = joblib.load('recommend_recipes_pipeline.pkl')
DATASET: pd.DataFrame = pd.read_csv('../data/cleaned_recipes.csv')
