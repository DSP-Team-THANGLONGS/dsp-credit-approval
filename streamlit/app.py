import streamlit as st
from predict import predict
from past_predictions import past_predictions

st.set_page_config(layout="wide")

def main():
    page = st.sidebar.selectbox(
        "Select a page", ("Predict", "Past Predictions")
    )

    if page == "Predict":
        predict()
    elif page == "Past Predictions":
        past_predictions()

if __name__ == "__main__":
    main()