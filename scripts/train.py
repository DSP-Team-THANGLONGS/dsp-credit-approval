import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from scripts.preprocessing import features_preprocessing


def build_model(data: pd.DataFrame) -> dict[str, str]:
    train_set, val_set = train_test_split(
        data, test_size=0.25, random_state=42
    )
    train_set_features, train_set_target = features_preprocessing(train_set)
    val_set_features, val_set_target = features_preprocessing(val_set)

    classifiers = {
        "Decision Tree": DecisionTreeClassifier(max_depth=10),
        "Random Forest": RandomForestClassifier(
            n_estimators=150, max_depth=10
        ),
        "Logistic Regression": LogisticRegression(C=0.1),
        "SVM": SVC(kernel="poly", C=0.5),
        "Naive Bayes": GaussianNB(),
    }

    best_model = None
    best_accuracy = 0

    for name, classifier in classifiers.items():
        classifier.fit(train_set_features, train_set_target)
        y_pred = classifier.predict(val_set_features)
        accuracy = accuracy_score(val_set_target, y_pred)
        print(f"{name} Accuracy: {accuracy}")

        if accuracy > best_accuracy:
            best_model = classifier
            best_accuracy = accuracy

    print(f"Best Model: {best_model}\nBest Accuracy: {best_accuracy}")
    model = best_model
    with open("../output_model/model.pkl", "wb") as f:
        pickle.dump(model, f)
    result = accuracy_score(model.predict(val_set_features), val_set_target)

    return {"accuracy_score": str(result)}
