from pydantic import BaseModel

class Observation(BaseModel):
    email_text: str
    has_link: bool
    has_money: bool
    step_count: int


class Action(BaseModel):
    action_type: str


class Reward(BaseModel):
    value: float
    reason: str