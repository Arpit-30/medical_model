from pydantic import BaseModel

class Observation(BaseModel):
    symptoms: str
    step_count: int


class Action(BaseModel):
    action_type: str  # "urgent" or "not_urgent"


class Reward(BaseModel):
    value: float
    reason: str