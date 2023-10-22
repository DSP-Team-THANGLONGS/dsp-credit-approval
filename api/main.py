from typing import Union
from fastapi import FastAPI
import sklearn
from sklearn.ensemble import RandomForestClassifier
import pickle
from sklearn.preprocessing import StandardScaler, OrdinalEncoder, OneHotEncoder

app = FastAPI()
scaler = StandardScaler()
ordinal_encoder = OrdinalEncoder()
onehot_encoder = OneHotEncoder()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/predict")
def make_predictions(features: list):
    #load model
    model_path = "../output_model/model.sav"
    loaded_model = pickle.load(open(model_path, "rb"))

    return loaded_model.predict(features)