#from surprise import KNNWithMeans
#from surprise import Reader, Dataset

from ai_model import RunModel

def recommendation(done_MLE):
    number_of_recommendation = 20
    mediaPref = 1 #1--> Audio / 2-->Text / 3-->Video
    level = 2

    recommendations, _ = RunModel.get_recommendations(mediaPref, level, number_of_recommendation, done_MLE)
    return recommendations
