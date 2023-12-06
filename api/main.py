import sys

sys.path.append("../")
from fastapi import FastAPI, Depends
import pickle
import pandas as pd
import numpy as np
from scripts.preprocessing import features_preprocessing
from database.database import SessionLocal, engine
from database import crud, models
from sqlalchemy.orm import Session
import datetime

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
dataset = pd.read_csv("../data/merged_data.csv").drop(
    ["ID", "APPROVED"], axis=1
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def save_predict(
    data: pd.DataFrame, db: Session = Depends(get_db)
) -> bool:
    date_prediction = datetime.date.today()
    date_prediction = date_prediction.strftime("%Y-%m-%d")
    today = datetime.datetime.now().date()
    birthday = today - datetime.timedelta(
        days=int(np.abs(data["DAYS_BIRTH"].values[0]))
    )
    employed_day = today - datetime.timedelta(
        days=int(np.abs(data["DAYS_EMPLOYED"].values[0]))
    )

    still_working = True if data["DAYS_EMPLOYED"].values[0] < 0 else False
    record = {
        "own_car": data["FLAG_OWN_CAR"].values[0],
        "own_realty": data["FLAG_OWN_REALTY"].values[0],
        "income": data["AMT_INCOME_TOTAL"].values[0],
        "education": data["NAME_EDUCATION_TYPE"].values[0],
        "family_status": data["NAME_FAMILY_STATUS"].values[0],
        "housing_type": data["NAME_HOUSING_TYPE"].values[0],
        "birthday": birthday,
        "employed_day": employed_day,
        "still_working": still_working,
        "occupation": data["OCCUPATION_TYPE"].values[0],
        "fam_members": data["CNT_FAM_MEMBERS"].values[0],
        "result": data["RESULT"].values[0],
        "platform": data["PLATFORM"].values[0],
        "date_prediction": date_prediction,
    }
    db_record = crud.save_record(db=db, record=record)
    return db_record


@app.get("/get-columns")
def get_column_names():
    return dataset.columns.tolist()


@app.get("/get-features/{columns}")
def get_features(columns: str):
    return dataset[columns].unique().tolist()


@app.post("/predict")
async def make_predictions(
    features: list[dict], db: Session = Depends(get_db)
):
    # load model
    model_path = "../output_model/model.pkl"
    loaded_model = pickle.load(open(model_path, "rb"))
    converted_ft = pd.DataFrame(features)
    processed_ft, _ = features_preprocessing(converted_ft.copy())
    result = [
        rs
        for rs in (
            1 if proba >= 0.65 else 0
            for proba in loaded_model.predict_proba(processed_ft)[:, 1]
        )
    ]
    converted_ft["RESULT"] = result
    # await save_predict(converted_ft, db=db)
    return str(result)


@app.get("/get-predictions")
async def get_predictions(db: Session = Depends(get_db)):
    predictions = crud.get_records(db)
    return predictions
