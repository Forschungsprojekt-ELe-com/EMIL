# from surprise import KNNWithMeans
# from surprise import Reader, Dataset
import random

from ai_model import RunModel


def recommendation(done_MLE, preference):
    number_of_recommendation = 20
    if preference and len(preference) == 2:

        # map media preference value
        media_preference_list = preference[0::3]
        mapping = {0: 1, 1: 2, 2: 3}
        mapped_media_preference = [mapping[element] for element in media_preference_list if element in mapping]

        # map level
        level_preference_list = preference[1::3]

        media_pref = mapped_media_preference[-1]  # 1--> Audio / 2-->Text / 3-->Video ### 1 Text / 2 Audio / 3 Video
        level = level_preference_list[-1] + 1
    # if preference is empty, use default value
    else:
        media_pref = 1
        level = 1

    # Get recommendations using AI model
    # recommendations, _ = RunModel.get_recommendations(media_pref, level, number_of_recommendation, done_MLE)
    recommendations = get_recommendation_for_each_pref(level, number_of_recommendation, done_MLE)
    return recommendations


def get_recommendation_for_each_pref(level, number_of_recommendation, done_MLE):
    lesen, _ = RunModel.get_recommendations(2, level, number_of_recommendation, done_MLE)
    rec_lesen = filter_rec(lesen)
    hoeren, _ = RunModel.get_recommendations(1, level, number_of_recommendation, done_MLE)
    rec_hoeren = filter_rec(hoeren)
    sehen, _ = RunModel.get_recommendations(3, level, number_of_recommendation, done_MLE)
    rec_sehen = filter_rec(sehen)
    combined_recommendations = [item for sublist in zip(rec_lesen, rec_hoeren, rec_sehen) for item in sublist]
    return combined_recommendations


def filter_rec(df):
    obj_id_column = [col for col in df.columns if col.startswith('obj_id')]
    rec = df[obj_id_column[0]].dropna().tolist()
    random.shuffle(rec)
    return rec