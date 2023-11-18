import streamlit as st
import requests
import pandas as pd
import config
import datetime


def past_predictions():
    st.title("Past predictions:")

    res = requests.get(config.URL_GET_PREDICTIONS)
    data = res.json()
    df = pd.DataFrame(data)

    df["date_prediction"] = pd.to_datetime(
        df["date_prediction"], format="%Y-%m-%d"
    ).dt.date
    df["result"] = df["result"].replace({1: "Good", 0: "Bad"})
    df["income"] = df["income"].round(2)

    st.write("Filter Options")
    start_date = datetime.date.today() - datetime.timedelta(days=7)
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "Start Date",
            value=start_date,
            max_value=datetime.date.today(),
            key="start_date",
        )
    with col2:
        end_date = st.date_input(
            "End Date", max_value=datetime.date.today(), key="end_date"
        )

    col3, col4 = st.columns(2)
    with col3:
        result = st.selectbox("Result", ["All", "Good", "Bad"], key="result")
    with col4:
        platform = st.selectbox(
            "Platform", ["All", "App", "Job"], key="platform"
        )

    # Filter the DataFrame based on user selections
    filter_conditions = (
        (
            (df["date_prediction"] >= start_date)
            & (df["date_prediction"] <= end_date)
            if start_date and end_date
            else True
        )
        & ((df["result"] == result) if result != "All" else True)
        & ((df["platform"] == platform) if platform != "All" else True)
    )

    df = df[filter_conditions]

    # Rename columns
    column_mapping = {
        "date_prediction": "Date of prediction",
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

    st.dataframe(df, hide_index=True)


if __name__ == "__main__":
    past_predictions()
