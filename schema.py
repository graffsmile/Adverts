from pydantic import BaseModel


class User(BaseModel):
    user_name: str
    # password: str

class Adv(BaseModel):
    tittle: str
    description: str
    owner: int