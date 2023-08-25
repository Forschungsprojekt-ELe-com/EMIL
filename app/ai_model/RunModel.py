#!/usr/bin/env python
# coding: utf-8

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Load the model
tfidf_loaded = joblib.load('ai_model/tfidf_model.pkl')


# In[12]:


df = pd.read_pickle('ai_model/my_dataframe.pkl')


# In[13]:


# compute the cosine similarity matrix
similarity = cosine_similarity(tfidf_loaded)


# In[14]:


# create a function that takes in movie title as input and returns a list of the most similar movies

def get_top_titles_and_categories(df, movie_indices, mediaPref):
    # extract the 'subtitle' and 'category' columns from the DataFrame
    top_titles_df = pd.DataFrame(df.iloc[movie_indices]['subtitle'])
    top_categories_df = pd.DataFrame(df.iloc[movie_indices]['category'])
    top_ref_id_df = pd.DataFrame(df.iloc[movie_indices][f'ref_id{mediaPref}'])
    top_obj_id_df = pd.DataFrame(df.iloc[movie_indices][f'obj_id{mediaPref}'])


    # concatenate the data frames horizontally
    result_df = pd.concat([top_titles_df, top_categories_df, top_ref_id_df, top_obj_id_df], axis=1)

    return result_df


def get_recommendations(item_name, mediaPref,  level, n, done_list_ref_id, cosine_sim=similarity):

    # If 'item_name' is None, select a random 'item_index' where 'level' equals 'category'
    if item_name is None:
        item_index = df[df.category == level].sample(1).index.tolist()
    else:
        item_index = df[df[f'ref_id{mediaPref}'] == item_name].index.tolist()
    print(item_index)


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

    #filtering by level
    if level < 3:
        result_df = result_df.loc[df['category'] == level, :]

    result_df = result_df[~result_df[f'ref_id{mediaPref}'].isin(done_list_ref_idComplete)]

    # If len of result_df is less than 5, grab results from level 3
    # If len of result_df is less than 5, increment level by 1 and grab results until level 3
    while len(result_df) < 5 and level < 3:
        level += 1
        additional_result_df, additional_sim_scores_all = get_recommendations(item_name, mediaPref,  level, n, done_list_ref_idComplete, cosine_sim)
        result_df = pd.concat([result_df, additional_result_df])
        sim_scores_all += additional_sim_scores_all

    # sort the DataFrame by 'sim_scores' in descending order
    result_df = result_df.sort_values(by='sim_scores', ascending=False)

    print(result_df)
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
    # Flatten the DataFrame into a list
    result_list = result_info.values.flatten().tolist()
    print(result_list)
    return result_list


# visualize the results
def show_results(movie_name, top_titles_df):
    movie_index = df[df.itemId==movie_name].subtitle
    top_titles_df = top_titles_df.sort_values(by='sim_scores', ascending=False)
    fix, ax = plt.subplots(figsize=(11, 5))
    sns.barplot(data=top_titles_df, y='subtitle', x= 'sim_scores', color='blue')
    plt.xlim((0,1))
    plt.title(f'Top 15 recommendations for {movie_index}')
    pct_values = ['{:.2}'.format(elm) for elm in list(top_titles_df['sim_scores'])]
    ax.bar_label(container=ax.containers[0], labels=pct_values, size=12)

# generate a list of recommendations for a specific movie title
mediaPref = 1 #1--> Audio / 2-->Text / 3-->Video
item_name = 647 #ref_id of latest interaction
number_of_recommendations = 20
level = 2
done_list_ref_id = [633, 655, 635, 626, 650, 671, 665, 668, 647]

# result_df, _ = get_recommendations(item_name, level, number_of_recommendations)
#get_recommendations(movie_name, level, number_of_recommendations)



