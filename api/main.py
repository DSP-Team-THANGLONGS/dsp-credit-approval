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
    # Calculate today's date
    today = datetime.datetime.now().date()

    # Convert "DAYS_BIRTH" and "DAYS_EMPLOYED" columns to absolute values
    data["DAYS_BIRTH"] = np.abs(data["DAYS_BIRTH"])
    data["DAYS_EMPLOYED"] = np.abs(data["DAYS_EMPLOYED"])

    # Calculate birthday and employed day
    data["DAYS_BIRTH"] = data["DAYS_BIRTH"].apply(
        lambda x: today - pd.to_timedelta(x, unit="D")
    )
    data["EMPLOYED_DAY"] = data["DAYS_EMPLOYED"].apply(
        lambda x: today - pd.to_timedelta(x, unit="D")
    )

    # Determine if still working
    data["STILL_WORKING"] = data["DAYS_EMPLOYED"] < 0

    # Create the record DataFrame
    records = {
        "own_car": data["FLAG_OWN_CAR"].tolist(),
        "own_realty": data["FLAG_OWN_REALTY"].tolist(),
        "income": data["AMT_INCOME_TOTAL"].tolist(),
        "education": data["NAME_EDUCATION_TYPE"].tolist(),
        "family_status": data["NAME_FAMILY_STATUS"].tolist(),
        "housing_type": data["NAME_HOUSING_TYPE"].tolist(),
        "birthday": data["DAYS_BIRTH"].tolist(),
        "employed_day": data["EMPLOYED_DAY"].tolist(),
        "still_working": data["STILL_WORKING"].tolist(),
        "occupation": data["OCCUPATION_TYPE"].tolist(),
        "fam_members": data["CNT_FAM_MEMBERS"].tolist(),
        "result": data["RESULT"].tolist(),
        "platform": data["PLATFORM"].tolist(),
        "date_prediction": [today.strftime("%Y-%m-%d %H:%M:%S")] * len(data),
    }
    db_record = crud.save_record(db=db, records=records)
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
    await save_predict(converted_ft, db=db)
    return str(result)


@app.get("/get-predictions")
async def get_predictions(db: Session = Depends(get_db)):
    predictions = crud.get_records(db)
    return predictions
