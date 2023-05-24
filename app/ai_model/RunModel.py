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

def get_top_titles_and_categories(df, movie_indices):
    # extract the 'subtitle' and 'category' columns from the DataFrame
    top_titles_df = pd.DataFrame(df.iloc[movie_indices]['subtitle'])
    top_categories_df = pd.DataFrame(df.iloc[movie_indices]['category'])
    top_ref_id1_df = pd.DataFrame(df.iloc[movie_indices]['ref_id1'])
    top_ref_id2_df = pd.DataFrame(df.iloc[movie_indices]['ref_id2'])
    top_ref_id3_df = pd.DataFrame(df.iloc[movie_indices]['ref_id3'])
    top_obj_id1_df = pd.DataFrame(df.iloc[movie_indices]['obj_id1'])
    top_obj_id2_df = pd.DataFrame(df.iloc[movie_indices]['obj_id2'])
    top_obj_id3_df = pd.DataFrame(df.iloc[movie_indices]['obj_id3'])

    # concatenate the two data frames horizontally
    #result_df = pd.concat([top_titles_df, top_categories_df], axis=1) #old function
    result_df = pd.concat([top_titles_df, top_categories_df, top_ref_id1_df, top_ref_id2_df, top_ref_id3_df, top_obj_id1_df, top_obj_id2_df, top_obj_id3_df], axis=1)


    return result_df


def get_recommendations(title, level, n, done_list_ref_id, cosine_sim=similarity):

 # get the index of the item that matches the title
    item_index = df[(df.ref_id1 == item_name) |
                      (df.ref_id2 == item_name) |
                      (df.ref_id3 == item_name)].index.tolist()


    # get the pairwsie similarity scores of all movies with that movie and sort the movies based on the similarity scores
    #sim_scores_all = sorted(list(enumerate(cosine_sim[item_index])), key=lambda x: x[1], reverse=True)[1:]
    sim_scores_all = []
    for item_index in item_index:
        sim_scores_all += sorted(list(enumerate(cosine_sim[item_index])),
                                 key=lambda x: x[1], reverse=True)[1:]

    movie_indices = [i[0] for i in sim_scores_all]
    scores = [i[1] for i in sim_scores_all]

    # return the top n most similar movies from the movies df
    result_df = get_top_titles_and_categories(df, movie_indices)
    result_df['sim_scores'] = scores
    result_df['ranking'] = range(1, len(result_df) + 1)

    #filtering by level
    if level < 3:
        result_df = result_df.loc[df['category'] == level, :]

    # Remove rows from the result DataFrame where ref_id is found in any of the ref_id columns
    result_df = result_df[~result_df['ref_id1'].isin(done_list_ref_id) &
                      ~result_df['ref_id2'].isin(done_list_ref_id) &
                      ~result_df['ref_id3'].isin(done_list_ref_id)]
    # print(result_df)
    return result_df, sim_scores_all


# generate a list of recommendations for a specific movie title
item_name = 629 #ref_id
number_of_recommendations = 20
level = 2
# done_list_ref_id = [644,633,655]

# result_df, _ = get_recommendations(item_name, level, number_of_recommendations)
#get_recommendations(movie_name, level, number_of_recommendations)



