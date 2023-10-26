# from surprise import KNNWithMeans
# from surprise import Reader, Dataset

from ai_model import RunModel


def recommendation(done_MLE, preference):
    number_of_recommendation = 20

    if preference and len(preference) >= 3:

        # map media preference value
        media_preference_list = preference[0::3]
        mapping = {0: 2, 1: 1, 2: 3}
        mapped_media_preference = [mapping[element] for element in media_preference_list if element in mapping]

        # map level
        level_preference_list = preference[1::3]

        media_pref = mapped_media_preference[-1] # 1--> Audio / 2-->Text / 3-->Video
        level = level_preference_list[-1] + 1
    # if preference is empty, use default value
    else:
        media_pref = 1
        level = 1

    # Get recommendations using AI model
    recommendations, _ = RunModel.get_recommendations(media_pref, level, number_of_recommendation, done_MLE)
    return recommendations
