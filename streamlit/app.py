import streamlit as st
from predict import predict
from past_predictions import past_predictions

st.set_page_config(layout="wide")
PAGE_PREDICT = "Predict Credit Card Approval"
PAGE_PAST_PREDICTIONS = "Past Predictions"

PAGE_PREDICT = "Predict Credit Card Approval"
PAGE_PAST_PREDICTIONS = "Past Predictions"

def main():
    page = st.sidebar.selectbox(
        "Select a page", ("Predict", "Past Predictions")
    )

    if page == "Predict":
        predict()
    elif page == "Past Predictions":
        past_predictions()

pages = {
    PAGE_PREDICT: predict,
    PAGE_PAST_PREDICTIONS: past_predictions,
}

if __name__ == "__main__":
    pages = {
        PAGE_PREDICT: predict,
        PAGE_PAST_PREDICTIONS: past_predictions,
    }

    selected_page = st.sidebar.selectbox("Go to", list(pages.keys()))

    pages[selected_page]()
