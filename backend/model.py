import joblib
import pandas as pd

PIPELINE = joblib.load('recommend_recipes_pipeline.pkl')
DATASET: pd.DataFrame = pd.read_csv('../data/cleaned_recipes.csv')
def recommend(user_data: dict) -> pd.DataFrame:
    """
    Recommend recipes according to user's preferences.

    :param user_data: Dict containing user's past chosen recipes and their contents
    :return: DataFrame containing the similar recipes
    """
    df_user_data = pd.DataFrame(user_data)
    indices = PIPELINE.transform(df_user_data)[0] # Find similar recipes
    return DATASET.iloc[indices]

