EMPTY_OBJECT_ID = [1407, 1408, 1392, 1426, 1431, 1441, 1403, 1442, 1404, 1443, 1405, 1398, 1437, 1399, 1438, 1400, 1439,
                   1401, 1440, 1402]
def filter_empty_objects(recommendations):
    filtered_recommendations = [x for x in recommendations if x not in EMPTY_OBJECT_ID]
    return filtered_recommendations
