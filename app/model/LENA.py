from pydantic import BaseModel


class LENA(BaseModel):
    user_id: str
    ref_id_course: int
    current_usecase: int
    transmitted_at: str