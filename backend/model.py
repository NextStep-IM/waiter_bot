import joblib
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, FunctionTransformer


# PIPELINE = joblib.load('recommend_recipes_pipeline.pkl')
# DATASET: pd.DataFrame = pd.read_csv('../data/cleaned_recipes.csv')
# def recommend(user_data: dict) -> pd.DataFrame:
#     """
#     Recommend recipes according to user's preferences.
#
#     :param user_data: Dict containing user's past chosen recipes and their contents
#     :return: DataFrame containing the similar recipes
#     """
#     df_user_data = pd.DataFrame(user_data)
#     indices = PIPELINE.transform(df_user_data)[0] # Find similar recipes
#     return DATASET.iloc[indices]

class Recommender:

    def __init__(self, df: pd.DataFrame, user_data: pd.DataFrame):
        self.features = ['Calories', 'FatContent', 'SaturatedFatContent', 'CholesterolContent', 'SodiumContent', 'CarbohydrateContent', 'FiberContent', 'SugarContent', 'ProteinContent']
        self.df = df
        self.user_data = user_data[self.features]

    def _scaling(self, extracted_data: pd.DataFrame):
        scaler = StandardScaler()
        prep_data = scaler.fit_transform(extracted_data[self.features])
        return prep_data,scaler


    def _nn_predictor(self, prep_data):
        neigh = NearestNeighbors(metric='cosine', algorithm='brute')
        neigh.fit(prep_data)
        return neigh

    def _build_pipeline(self, neigh, scaler, params):
        transformer = FunctionTransformer(neigh.kneighbors, kw_args=params)
        pipeline = Pipeline(
            [
                ('std_scaler',scaler),
                ('NN',transformer)
            ]
        )
        return pipeline

    def _extract_data(self, df, category):
        extracted_data = df.copy()
        # if not ingredient_filter:
        #     for ingredient in ingredient_filter:
        #         extracted_data = extracted_data[extracted_data['RecipeIngredientParts'].str.contains(ingredient, regex=False)]

        if category:
            extracted_data = extracted_data[extracted_data['RecipeCategory'] == category]
            print(f'- - - - - - - - - - -\n{extracted_data['RecipeCategory'].sample(5)}\n- - - - - - - - - - ')
        return extracted_data

    def _apply_pipeline(self, pipeline, user_data, extracted_data):
        return extracted_data.iloc[pipeline.transform(user_data)[0]]

    def recommend(self, category: str=None, params: dict=None):
        if params is None:
            params = {'return_distance': False}

        extracted_data = self._extract_data(self.df, category)
        prep_data,scaler = self._scaling(extracted_data)
        neigh = self._nn_predictor(prep_data)
        pipeline = self._build_pipeline(neigh,scaler,params)

        return self._apply_pipeline(pipeline, self.user_data, extracted_data)


def main():
    features = ['Calories', 'FatContent', 'SaturatedFatContent', 'CholesterolContent', 'SodiumContent',
                     'CarbohydrateContent', 'FiberContent', 'SugarContent', 'ProteinContent']
    df = pd.read_csv('../data/cleaned_recipes.csv')
    test_data = df[features].sample(20)
    print(f'Test Data:\n{test_data}\n- - - - - - - - - - -')
    rec = Recommender(df, test_data)
    result = rec.recommend('Dessert')
    print(result[['Name', 'RecipeCategory']])
    print('- - - - - - - - - - -')
    for t, r in zip(test_data.index, result.index):
        if t == r:
            print(f'Test Data and Recommendations are same at index: {t}')

if __name__ == '__main__':
    main()