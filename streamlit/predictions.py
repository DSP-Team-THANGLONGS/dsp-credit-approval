import streamlit as st
import requests
import pandas as pd


def app():
    st.title("Table Viewer")

    st.write("Past predictions:")

    res = requests.get("http://127.0.0.1:8000/get-predictions")
    data = res.json()
    df = pd.DataFrame(data)
    # Rename columns
    column_mapping = {
        "own_car": "FLAG_OWN_CAR",
        "own_realty": "FLAG_OWN_REALTY",
        "income": "AMT_INCOME_TOTAL",
        "family_status": "NAME_FAMILY_STATUS",
        "result": "NAME_INCOME_TYPE",
        "education": "NAME_EDUCATION_TYPE",
        "housing_type": "NAME_HOUSING_TYPE",
        "birthday": "DAYS_BIRTH",
        "employed_day": "DAYS_EMPLOYED",
        "occupation": "OCCUPATION_TYPE",
        "fam_members": "CNT_FAM_MEMBERS",
        "result": "RESULT",
    }
    df.rename(columns=column_mapping, inplace=True)
    st.table(df if "df" in locals() else pd.DataFrame())


if __name__ == "__main__":
    app()
