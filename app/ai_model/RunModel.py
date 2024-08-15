from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib
import pandas as pd
import seaborn as sns
import os

# Get current absolute path
current_script_path = os.path.abspath(__file__)
current_script_directory = os.path.dirname(current_script_path)

# Load the model
tfidf_path = os.path.join(current_script_directory, "tfidf_model.pkl")
tfidf_loaded = joblib.load(tfidf_path)

dataframe_path = os.path.join(current_script_directory, "my_dataframe.pkl")
df = pd.read_pickle(dataframe_path)

# compute the cosine similarity matrix
similarity = cosine_similarity(tfidf_loaded)


# get Data from DataFrame
def get_top_titles_and_categories(df, movie_indices, mediaPref):
    # extract the 'subtitle' and 'category' columns from the DataFrame
    top_titles_df = pd.DataFrame(df.iloc[movie_indices]['subtitle'])
    top_categories_df = pd.DataFrame(df.iloc[movie_indices]['category'])
    top_ref_id_df = pd.DataFrame(df.iloc[movie_indices][f'ref_id{mediaPref}'])
    top_obj_id_df = pd.DataFrame(df.iloc[movie_indices][f'obj_id{mediaPref}'])

    # concatenate the data frames horizontally
    result_df = pd.concat([top_titles_df, top_categories_df, top_ref_id_df, top_obj_id_df], axis=1)

    return result_df


def get_recommendations(mediaPref, level, n, done_list_ref_id_not_filtered,
                        cosine_sim=similarity):
    item_name, done_list_ref_id = validate_obj_ids(done_list_ref_id_not_filtered)
    # If 'item_name' is None, select a random 'item_index' where 'level' equals 'category'
    if not done_list_ref_id:
        item_index = df[df.category == level].sample(1).index.tolist()
    else:
        item_index = df[(df[f'obj_id1'] == item_name) |
                        (df[f'obj_id2'] == item_name) |
                        (df[f'obj_id3'] == item_name)].index.tolist()

    # get the pairwsie similarity scores of all movies with that movie and sort the movies based on the similarity scores
    # sim_scores_all = sorted(list(enumerate(cosine_sim[item_index])), key=lambda x: x[1], reverse=True)[1:]
    # will be always only one single value in the list xxxxD
    sim_scores_all = []
    for item_index in item_index:
        sim_scores_all += sorted(list(enumerate(cosine_sim[item_index])),
                                 key=lambda x: x[1], reverse=True)[1:]

    movie_indices = [i[0] for i in sim_scores_all]
    scores = [i[1] for i in sim_scores_all]

    # return the top n most similar movies from the movies df
    result_df = get_top_titles_and_categories(df, movie_indices, mediaPref)
    result_df['sim_scores'] = scores
    result_df['ranking'] = range(1, len(result_df) + 1)

    done_list_ref_idComplete = get_id_info(df, done_list_ref_id)

    # filtering by level
    if level < 3:
        result_df = result_df.loc[df['category'] == level, :]
    result_df = result_df[~result_df[f'obj_id{mediaPref}'].isin(done_list_ref_idComplete)]

    # If len of result_df is less than 5, grab results from level 3
    # If len of result_df is less than 5, increment level by 1 and grab results until level 3
    while len(result_df) < 5 and level < 3:
        level += 1
        additional_result_df, additional_sim_scores_all = get_recommendations(item_name, mediaPref, level, n,
                                                                              done_list_ref_idComplete, cosine_sim)
        result_df = pd.concat([result_df, additional_result_df])
        sim_scores_all += additional_sim_scores_all

    # sort the DataFrame by 'sim_scores' in descending order
    result_df = result_df.sort_values(by='sim_scores', ascending=False)
    return result_df, sim_scores_all


def get_id_info(df, done_list_ref_id):
    # Columns we are interested in
    columns = ['ref_id1', 'ref_id2', 'ref_id3', 'obj_id1', 'obj_id2', 'obj_id3']
    # Create an empty DataFrame to store results
    result_info = pd.DataFrame(columns=columns)
    # Iterate through done_list_ref_id
    for id_value in done_list_ref_id:
        # For each ID, get rows where the ID is found in the columns of interest
        id_df = df[df[columns].apply(lambda row: id_value in row.values, axis=1)][columns]
        result_info = pd.concat([result_info, id_df], ignore_index=True)
    result_list = result_info.dropna()
    return result_list


# check for valid obj_ids
def validate_obj_ids(done_list_ref_id):
    valid_ids = df[['obj_id1', 'obj_id2', 'obj_id3']].values.flatten()  # Extract valid IDs from DataFrame
    done_list_ref_id = [id_ for id_ in done_list_ref_id if
                        id_ in valid_ids]  # Filter out IDs not found in the DataFrame
    # If item_name isn't set (None), default to the last ID in done_list_ref_id
    if done_list_ref_id:
        item_name = done_list_ref_id[-1]
    else:
        item_name = None

    return item_name, done_list_ref_id
