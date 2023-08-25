class Data:
    MLE_ref_id: list
    recommendation_reason: str


class Meta:
    transmitted_at: str
    status: str
    error: str


class EMIL:
    def __init__(self):
        self.meta = Meta()
        self.data = Data()
