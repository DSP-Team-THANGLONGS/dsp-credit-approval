import pandas as pd
from sklearn.preprocessing import StandardScaler, OrdinalEncoder, OneHotEncoder


def features_preprocessing(data: pd.DataFrame) -> (pd.DataFrame, pd.DataFrame):
    # create scaler and encoder
    scaler = StandardScaler()
    ordinal_encoder = OrdinalEncoder()

    # ordinal encoder
    ordinal_data = ordinal_encoder.fit(data[["CNT_FAM_MEMBERS"]])
    data[["CNT_FAM_MEMBERS"]] = ordinal_data.transform(
        data[["CNT_FAM_MEMBERS"]]
    )

    # onehot encoder
    data = pd.get_dummies(
        data,
        columns=[
            "NAME_INCOME_TYPE",
            "NAME_EDUCATION_TYPE",
            "NAME_HOUSING_TYPE",
            "OCCUPATION_TYPE",
        ],
        dtype=int,
    )

    # scaler
    scaler_data = scaler.fit(data[["AMT_INCOME_TOTAL", "DAYS_EMPLOYED"]])
    data[["AMT_INCOME_TOTAL", "DAYS_EMPLOYED"]] = scaler_data.transform(
        data[["AMT_INCOME_TOTAL", "DAYS_EMPLOYED"]]
    )

    data[["FLAG_OWN_CAR", "FLAG_OWN_REALTY"]] = data[
        ["FLAG_OWN_CAR", "FLAG_OWN_REALTY"]
    ].replace({"Y": 1, "N": 0})

    # core features and target
    features = data.drop("APPROVED", axis=1)
    target = data[["APPROVED"]]
    return features, target
