from fastapi import FastAPI
from models import Observation, Action
from server.email_env_environment import MedicalEnvironment

app = FastAPI()

env = MedicalEnvironment()


@app.post("/reset")
def reset():
    obs = env.reset()
    return {"observation": obs.dict()}


@app.post("/step")
def step(action: Action):
    obs, reward, done, _ = env.step(action)

    return {
        "observation": obs.dict(),
        "reward": reward.dict(),
        "done": done
    }


@app.get("/state")
def state():
    return env.state()