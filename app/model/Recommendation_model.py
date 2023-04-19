from typing import List, Optional
import time


class AI_recommendation:
    transmitted_at = time.time()

    def __init__(self, MLE_ref_id, user_id, id_course, current_usecase):
        self.MLE_ref_id = MLE_ref_id
        self.user_id = user_id
        self.id_course = id_course
        self.current_usecase = current_usecase
