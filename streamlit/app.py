# BEGIN: 3j4k5l6m7n8o
import streamlit as st
import json
import datetime
import requests
import pandas as pd


def predict():
    st.title("Credit Card Approval Form")
    st.write(
        "Please fill out the following form to check your eligibility for a credit card."
    )

    # Question 1
    st.write("Do you own a car?")
    car_options = ["Yes", "No"]
    car = st.radio("Select an option", car_options, key="radio1")

    # Question 2
    st.write("Do you own any piece of real estate?")
    real_estate_options = ["Yes", "No"]
    real_estate = st.radio(
        "Select an option", real_estate_options, key="radio2"
    )

    # Question Birthday
    st.write("What is your birthday?")
    birthday = st.date_input("Calendar", datetime.date(1999, 11, 12))

    # Question 3
    st.write(" Do you have children?")
    children_options = ["Yes", "No"]
    children = st.radio("Select an option", children_options, key="radio3")
    children_count = 0
    if children == "Yes":
        st.write("How many children do you have?")
        children_count_options = list(range(11))
        children_count = st.selectbox(
            "Select an option", children_count_options, key="select1"
        )

    # Question 5
    st.write("What is your yearly income?")
    income = st.number_input(
        "Enter your yearly income", min_value=0.0, format="%f", key="number1"
    )

    # Question 6
    st.write("What is your source of income?")
    income_type_options = [
        "Working",
        "Commercial associate",
        "Pensioner",
        "State servant",
        "Student",
    ]
    income_type = st.selectbox(
        "Select an option", income_type_options, key="select2"
    )

    st.write("Are you still working?")
    working_options = ["Yes", "No"]
    isWorking = st.radio("Select an option", working_options, key="radio4")
    if isWorking == "Yes":
        st.write("The day you start working?")
        workday = st.date_input("Calendar", datetime.date(2020, 10, 20))
    else:
        st.write("The day you stop working?")
        workday = st.date_input("Calendar", datetime.date(2020, 10, 20))

    st.write("What is your working domain?")
    occupation_options = [
        "Other",
        "Security staff",
        "Sales staff",
        "Accountants",
        "Laborers",
        "Core staff",
        "Managers",
        "Drivers",
        "Cleaning staff",
        "Private service staff",
        "High skill tech staff",
        "Low-skill Laborers",
        "Cooking staff",
        "Medicine staff",
        "Secretaries",
        "HR staff",
        "Waiters/barmen staff",
        "Realty agents",
        "IT staff",
    ]
    occupation = st.selectbox(
        "Select an option", occupation_options, key="select3"
    )

    # Question 7
    st.write("What is your education level?")
    education_options = [
        "Higher education",
        "Secondary / secondary special",
        "Incomplete higher",
        "Lower secondary",
        "Academic degree",
    ]
    education = st.selectbox(
        "Select an option", education_options, key="select4"
    )

    # Question 8
    st.write("What is your marital status?")
    marital_status_options = [
        "Civil marriage",
        "Married",
        "Single / not married",
        "Separated",
        "Widow",
    ]
    marital_status = st.selectbox(
        "Select an option", marital_status_options, key="select5"
    )

    # Question 9
    st.write("What is your housing situation?")
    housing_options = [
        "Rented apartment",
        "House / apartment",
        "Municipal apartment",
        "With parents",
        "Co-op apartment",
        "Office apartment",
    ]
    housing = st.selectbox("Select an option", housing_options, key="select6")

    # Question 10
    st.write("How many members are there in your family?")
    family_members_options = list(range(1, 21))
    family_members = st.selectbox(
        "Select an option", family_members_options, key="select7"
    )

    if st.button("Submit prediction", type="primary"):
        birthday_calc = birthday - datetime.date.today()
        employed_calc = (
            workday - datetime.date.today()
            if isWorking == "Yes"
            else datetime.date.today() - workday
        )
        data = {
            "FLAG_OWN_CAR": car[0],
            "FLAG_OWN_REALTY": real_estate[0],
            "AMT_INCOME_TOTAL": income,
            "NAME_INCOME_TYPE": income_type,
            "NAME_EDUCATION_TYPE": education,
            "NAME_FAMILY_STATUS": marital_status,
            "NAME_HOUSING_TYPE": housing,
            "DAYS_BIRTH": birthday_calc.days,
            "DAYS_EMPLOYED": employed_calc.days,
            "OCCUPATION_TYPE": occupation,
            "CNT_FAM_MEMBERS": family_members,
        }

        res = requests.post(
            "http://127.0.0.1:8000/predict", data=json.dumps(data)
        )
        input_list = (res.text).strip("[]").split(",")
        result_list = [
            int(item.strip('"'))
            if item.strip('"').isdigit()
            else float(item.strip('"'))
            if "." in item
            else item.strip('"')
            for item in input_list
        ]
        is_good_applicant = "good" if result_list[0] == 1 else "bad"
        result = f"This profile is a {is_good_applicant} applicants"
        st.write(result)


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
        "employed_day": "Employed day",
        "occupation": "Occupation",
        "fam_members": "Family member",
        "result": "Result",
    }
    df.rename(columns=column_mapping, inplace=True)
    df = df[column_mapping.values()]
    df["Result"] = df["Result"].replace({1: "Good", 0: "Bad"})

    if not df.empty:
        st.table(df)
    else:
        st.write("No data available.")


if __name__ == "__main__":
    predict()
    past_predictions()
