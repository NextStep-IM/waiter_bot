
import streamlit as st
import pandas as pd
from pathlib import Path


# if 'save_btn_clicked' not in st.session_state:
#     st.session_state['save_btn_clicked'] = False

if 'recipes' not in st.session_state:
    st.session_state['recipes'] = []

if 'selected_recipes' not in st.session_state:
    st.session_state['selected_recipes'] = []

if 'apply_btn_clicked' not in st.session_state:
    st.session_state['apply_btn_clicked'] = False

if 'save_triggered' not in st.session_state:
    st.session_state.save_triggered = False

if 'recommended_recipes' not in st.session_state:
    st.session_state['recommended_recipes'] = pd.DataFrame()

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



def display_recipes(df: pd.DataFrame):
    if not df.empty:
        st.session_state['recipes'] = df['Name'].tolist()
        # Index of the received dataframe may have random index numbers.
        # This will set the index from 0 to [number of rows].
        df.reset_index(drop=True, inplace=True)
        no_image_path = 'assets/no_image.jpg'
        for i in range(0, len(df), 2):
            cols = st.columns(2)
            for j, row in df.iloc[i:i + 2].iterrows(): # i = index, row = Series
                print(j)
                with cols[j % 2]:
                    # try:
                    #     st.image(row['Images'], use_container_width=True)
                    # except Exception as err:
                    #     st.image(no_image_path, use_container_width=True)

                    st.markdown("---")
                    st.subheader(f"🍽️ {row['Name']} - Details")
                    st.markdown(f"**Category**: {row['RecipeCategory']}")
                    st.markdown(f"**Instructions**: {row['RecipeInstructions']}")

                    st.markdown(f"**Ingredients:**")
                    parts = row['RecipeIngredientParts'].strip('[]').split(',')
                    quantities = row['RecipeIngredientQuantities'].strip('[]').split(',')
                    for part, qty in zip(parts, quantities):
                        st.markdown(f"- {part}: {qty}")

                    st.markdown("**Nutrition Facts**")
                    st.markdown(f"- **Calories**: {row['Calories']} kcal")
                    st.markdown(f"- **Fat**: {row['FatContent']}")
                    st.markdown(f"- **Saturated Fat**: {row['SaturatedFatContent']}")
                    st.markdown(f"- **Cholesterol**: {row['CholesterolContent']}")
                    st.markdown(f"- **Sodium**: {row['SodiumContent']}")
                    st.markdown(f"- **Carbs**: {row['CarbohydrateContent']}")
                    st.markdown(f"- **Fiber**: {row['FiberContent']}")
                    st.markdown(f"- **Sugar**: {row['SugarContent']}")
                    st.markdown(f"- **Protein**: {row['ProteinContent']}")


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


def recommend_with_user_history():
    categories = list(recipes_df['RecipeCategory'].unique())
    selected_cat = st.selectbox('Choose a category:', ['All'] + categories)
    result = pd.DataFrame()
    if st.button('Apply', key='apply_btn'):
        if selected_cat != 'All':
            rec_response = st.session_state.http_session.post(f'http://localhost:1111/recommend/{selected_cat}')
        else:
            rec_response = st.session_state.http_session.post(f'http://localhost:1111/recommend/All')

        if rec_response.status_code == 200:
            result = pd.DataFrame(rec_response.json()['message'])
        else:
            st.error(rec_response.text)
        if 'save_triggered' in st.session_state:
            st.session_state['save_triggered'] = False

    display_recipes(result.copy())

recipes_df = load_dataframe(find_absolute_path('cleaned_recipes.csv'))

response = st.session_state.http_session.get('http://localhost:1111/user')

if response.status_code == 200:
    json_data = response.json()
    if json_data['message']['first_time']:
        st.markdown(f"<h1 style='text-align: center;'>Since this is your first time, I will recommend you some popular recipes!</h1>", unsafe_allow_html=True)
        display_recipes(recommend_popular_recipes(recipes_df))
    else:
        recommend_with_user_history()
        if not st.session_state.save_triggered:
            recipe_names = st.session_state['recipes']
            selected_recipes = st.multiselect("Select recipes to save:", recipe_names)
            if st.button("Save Selected Recipe"):
                st.session_state.selected_recipes = selected_recipes
                st.session_state.save_triggered = True
                # Example action: look up full row and call your save logic
                selected_rows = pd.DataFrame()
                for recipe in st.session_state['selected_recipes']:
                    print(recipe)
                    selected_rows = recipes_df[recipes_df['Name'] == recipe]
                selected_rows = selected_rows[RECIPE_DATA]
                if not selected_rows.empty:
                    json_data = selected_rows.to_dict(orient='records')
                    print(json_data)
                    st.session_state.http_session.post(
                        'http://localhost:1111/save_recipe', json=json_data
                    )
                    st.success(f"✅ Saved: {selected_rows.to_dict()}")

else:
    print('Error in response from /user')