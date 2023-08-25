#from surprise import KNNWithMeans
#from surprise import Reader, Dataset

from ai_model import RunModel


def recommendation(ref_id, done_MLE):
    number_of_recommendation = 20
    mediaPref = 1 #1--> Audio / 2-->Text / 3-->Video
    item_name = 647 #ref_id of latest interaction
    level = 2
    done_MLE = [633, 655, 635, 626, 650, 671, 665, 668, 647]
    recommendations, _ = RunModel.get_recommendations(item_name, mediaPref, level, number_of_recommendation, done_MLE)
    return recommendations