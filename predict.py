import pickle
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, Field


class Client(BaseModel):
    lead_source: str
    number_of_courses_viewed: int
    annual_income: float

class PredictResponse(BaseModel):
    sub_probability: float
    subscription: bool


app = FastAPI(title="client-sub")

with open('pipeline_v2.bin', 'rb') as f_in:
    pipeline = pickle.load(f_in)

def predict_single(client):
    result = pipeline.predict_proba(client)[0, 1]
    return float(result)

@app.post("/predict")
def predict(client: Client) -> PredictResponse:
    prob = predict_single(client.model_dump())

    return PredictResponse(
        sub_probability = prob,
        subscription =  bool(prob >= 0.5)
    )



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9696)
