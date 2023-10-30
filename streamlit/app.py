# BEGIN: 3j4k5l6m7n8o
import streamlit as st

def main():
    st.title("Credit Card Approval Form")
    st.write("Please fill out the following form to check your eligibility for a credit card.")

    # Question 1
    st.write("Do you own a car?")
    car_options = ["Yes", "No"]
    car = st.radio("Select an option", car_options, key="radio1")

    # Question 2
    st.write("Do you own any piece of real estate?")
    real_estate_options = ["Yes", "No"]
    real_estate = st.radio("Select an option", real_estate_options, key="radio2")

    # Question 3
    st.write(" Do you have children?")
    children_options = ["Yes", "No"]
    children = st.radio("Select an option", children_options, key="radio3")
    
    if children == "Yes":
        st.write("How many children do you have?")
        children_count_options = list(range(11))
        children_count = st.selectbox("Select an option", children_count_options, key="select1")

    # Question 5
    st.write("What is your yearly income?")
    income = st.number_input("Enter your yearly income", min_value=0.0, format="%f", key="number1")

    # Question 6
    st.write("What is your source of income?")
    occupation_options = ["Working", "Commercial associate", "Pensioner", "State servant", "Student"]
    occupation = st.selectbox("Select an option", occupation_options, key="select2")

    # Question 7
    st.write("What is your education level?")
    education_options = ["Higher education", "Secondary / secondary special", "Incomplete higher", "Lower secondary", "Academic degree"]
    education = st.selectbox("Select an option", education_options, key="select3")

    # Question 8
    st.write("What is your marital status?")
    marital_status_options = ["Civil marriage", "Married", "Single / not married", "Separated", "Widow"]
    marital_status = st.selectbox("Select an option", marital_status_options, key="select4")

    # Question 9
    st.write("What is your housing situation?")
    housing_options = ["Rented apartment", "House / apartment", "Municipal apartment", "With parents", "Co-op apartment", "Office apartment"]
    housing = st.selectbox("Select an option", housing_options, key="select5")

    # Question 10
    st.write("How many members are there in your family?")
    family_members_options = list(range(1, 21))
    family_members = st.selectbox("Select an option", family_members_options, key="select6")

if __name__ == "__main__":
    main()
