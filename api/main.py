import sys

sys.path.append("../")
from typing import Union
from fastapi import FastAPI
import pickle
import pandas as pd
from scripts.preprocessing import features_preprocessing

app = FastAPI()
dataset = pd.read_csv("../data/merged_data.csv").drop(
    ["ID", "APPROVED"], axis=1
)


def save_predict(data: pd.DataFrame) -> bool:
    print(data)
    pass


@app.get("/get-columns")
def get_column_names():
    return dataset.columns.tolist()


@app.get("/get-features/{columns}")
def get_features(columns: str):
    return dataset[columns].unique().tolist()


@app.post("/predict")
def make_predictions(features: dict):
    # load model
    model_path = "../output_model/model.pkl"
    loaded_model = pickle.load(open(model_path, "rb"))
    converted_ft = pd.DataFrame([features])
    processed_ft, _ = features_preprocessing(converted_ft)
    result = loaded_model.predict(processed_ft)
    proba = loaded_model.predict_proba(processed_ft)
    processed_ft["PROBA"] = proba
    processed_ft["RESULT"] = result
    save_predict(processed_ft)
    return str(result[0]), str(max(proba[0]))


@app.get("past-predictions")
def get_past_predictions():
    pass
