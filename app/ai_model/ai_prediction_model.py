#from surprise import KNNWithMeans
#from surprise import Reader, Dataset

from ai_model import RunModel


def recommendation(ref_id, done_MLE):
    number_of_recommendation = 20
    level = 1
    recommendations, _ = RunModel.get_recommendations(ref_id, level, number_of_recommendation, done_MLE)
    return recommendations