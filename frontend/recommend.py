import streamlit as st
import pandas as pd
from pathlib import Path

RECIPE_DATA = ['Name', 'RecipeId', 'RecipeInstructions', 'RecipeIngredientParts', 'RecipeIngredientQuantities', 'RecipeCategory',
         'Images', 'Calories', 'FatContent', 'SaturatedFatContent', 'CholesterolContent', 'SodiumContent',
         'CarbohydrateContent', 'FiberContent', 'SugarContent', 'ProteinContent']

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

@st.cache_data
def recommend_popular_recipes(recipes_df: pd.DataFrame) -> pd.DataFrame:
    """
    Recommend highest-rated recipes from each category. This function
    is for when the user's logging in for the first time and there is no
    data for the model (NearestNeighbors) to use.

    :param recipes_df: The cleaned recipes dataset
    :return: Recipes
    """
    reviews_df = load_dataframe(find_absolute_path('reviews.csv'))
    merged_df = recipes_df.merge(reviews_df, on='RecipeId', how='outer', copy=True)
    indices = merged_df.groupby('RecipeCategory')['Rating'].idxmax()
    return merged_df.iloc[indices][RECIPE_DATA]

# TODO: Finish this
def recommend_with_user_history():
    categories = list(recipes_df['RecipeCategory'].unique())
    selected_cat = st.selectbox('Choose a category:', ['All'] + categories)

    if st.button('Apply'):
        # if selected_cat != 'All':
        #     # recipes = rec.recommend_recipes(selected_cat)
        #     pass
        # else:
        #     #recipes = rec.recommend_recipes()
        #     pass
        pass

    else:
