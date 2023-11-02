import streamlit as st
import requests
import pandas as pd


def past_predictions():
    st.title("Past predictions:")

    res = requests.get("http://127.0.0.1:8000/get-predictions")
    data = res.json()
    df = pd.DataFrame(data)
    # Rename columns
    column_mapping = {
        "date_prediction": "date prediction",
        "own_car": "Car Owner",
        "own_realty": "Realty Owner",
        "income": "Income Total",
        "family_status": "Family Status",
        "education": "Eductation",
        "housing_type": "Housing Type",
        "birthday": "Birthday",
        "employed_day": "(Un)Employed day",
        "still_working": "Is still working",
        "occupation": "Occupation",
        "fam_members": "Family member",
        "result": "Result",
    }
    df.rename(columns=column_mapping, inplace=True)
    df = df[column_mapping.values()]
    df["Result"] = df["Result"].replace({1: "Good", 0: "Bad"})
    df["Income Total"] = df["Income Total"].round(2)
    if not df.empty:
        st.table(df)
    else:
        st.write("No data available.")


if __name__ == "__main__":
    past_predictions()
