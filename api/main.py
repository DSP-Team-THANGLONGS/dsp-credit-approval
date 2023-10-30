from typing import Union
from fastapi import FastAPI
import pickle
from sklearn.preprocessing import StandardScaler, OrdinalEncoder, OneHotEncoder
import pandas as pd

app = FastAPI()
scaler = StandardScaler()
ordinal_encoder = OrdinalEncoder()
onehot_encoder = OneHotEncoder()
dataset = pd.read_csv('../data/application_record.csv').drop('ID', axis=1)
print(dataset)


def save_predict(data: pd.DataFrame) -> bool:


@app.get('/get-columns')
def get_column_names():
    return dataset.columns.tolist()


@app.get('/get-features/{columns}')
def get_features(columns: str):
    return dataset[columns].unique().tolist()


@app.post('/predict')
def make_predictions(features: list):
    # load model
    model_path = '../output_model/model.sav'
    loaded_model = pickle.load(open(model_path, 'rb'))
    result = loaded_model.predict(features)
    save_predict()
    return 


@app.get('past-predictions')
def get_past_predictions():
    pass
