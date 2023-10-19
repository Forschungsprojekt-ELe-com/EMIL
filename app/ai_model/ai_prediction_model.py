# from surprise import KNNWithMeans
# from surprise import Reader, Dataset

from ai_model import RunModel


def recommendation(done_MLE, preference):
    number_of_recommendation = 20

    if preference:
        media_pref = preference[0] + 1  # 1--> Audio / 2-->Text / 3-->Video
        level = preference[1] + 1

    # if preference is empty, use default value
    else:
        media_pref = 1
        level = 1

    # Get recommendations using AI model
    recommendations, _ = RunModel.get_recommendations(media_pref, level, number_of_recommendation, done_MLE)
    return recommendations
