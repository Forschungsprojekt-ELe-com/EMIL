#from surprise import KNNWithMeans
#from surprise import Reader, Dataset

from ai_model import RunModel

def recommendation(done_MLE, preference):
    number_of_recommendation = 20
    media_pref = (preference[0] or 0)+1 #1--> Audio / 2-->Text / 3-->Video
    level = (preference[1] or 0)+1

    print(media_pref, level)

    # Get recommendations using AI model
    recommendations, _ = RunModel.get_recommendations(media_pref, level, number_of_recommendation, done_MLE)
    return recommendations
