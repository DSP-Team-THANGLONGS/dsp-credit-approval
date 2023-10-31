import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from scripts.preprocessing import features_preprocessing


def build_model(data: pd.DataFrame) -> dict[str, str]:
    train_set, val_set = train_test_split(
        data, test_size=0.25, random_state=42
    )
    train_set_features, train_set_target = features_preprocessing(train_set)
    val_set_features, val_set_target = features_preprocessing(val_set)
    # model = SVC(gamma="auto", kernel="sigmoid")
    model = RandomForestClassifier(
        criterion="entropy", max_depth=5, n_estimators=150
    )
    model.fit(train_set_features, train_set_target)
    with open("../output_model/model.pkl", "wb") as f:
        pickle.dump(model, f)
    result = accuracy_score(model.predict(val_set_features), val_set_target)

    return {"accuracy_score": str(result)}
