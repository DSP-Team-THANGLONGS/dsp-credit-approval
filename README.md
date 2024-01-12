# Data Science in Production: Machine Learning Project

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](<!-- add link -->)

#### Group: Thanglongs

##### Members

1. Minh Duc Vu
2. Akansha Verma
3. Shashank Vaidya
4. Johnfredrick Ebikemefa Owotorufa

<!--Add image-->

## Use Case: _Credit Applicant Risk Prediction_

#### Title: Credit Applicant Risk Prediction

#### Dataset: [Credit Card Approval Predic](https://www.kaggle.com/datasets/rikdifos/credit-card-approval-prediction)

---

### Actor

- Credit Card Applicants
- Financial Institution/Bank
- Data Scientists/Analysts

### Preconditions

- The bank has collected sufficient application and credit records.
- Machine learning algorithms and infrastructure are available.

### Data Pre-processing

- Data from `application_record.csv` and `credit_record.csv` is merged based on
  the Client ID.
- Features such as 'good' or 'bad' client labels are engineered, possibly using
  techniques like vintage analysis.

### Model Development

- As data scientists, we would employ traditional logistic models as a baseline.
- Also, advanced machine learning algorithms (e.g., Boosting, Random Forest, SVM) are trained to refine predictions.

### Prediction & Decision Making

- The developed model would predict the creditworthiness of new applicants.
- The bank uses the model’s predictions, alongside other factors, to decide credit card approvals.

### Feedback Loop

- As new data accumulates, the model is retrained or adjusted to remain accurate.
- Transparent explanations for credit decisions are prepared for both applicants and
  regulatory purposes.

### Postconditions

- Applicants are either granted or denied credit based on the model’s predictions.
- Continuous learning ensures the model evolves with changing economic
  conditions and application trends.

### Exeption

If economic conditions shift drastically, manual review or adjustment may be
necessary to ensure model reliability.

### Note

Handling imbalanced data will be crucial for accurate prediction. Techniques
such as oversampling, under-sampling, or synthetic data generation might be
needed.

---

### Credit Applicant Risk Prediction Architecture diagram

## Main components

### Web app

There are 2 pages of the app:

- `Predict`: predicting the output by 2 ways
  - Enter your own details
  - Upload a CSV
- `History`: showing all rows in database that can be filtered by time and other types.

![Predict](images/predict.png)
![History](images/history.png)

### API

We implemented 2 endpoints by FastAPI:

- `predict`: POST request - inference prediction & save data to database
- `get-predict`: GET request - retrieve data from database

### Database

We used PostgreSQL with table including 15 columns:

    `id`: number of predictions
    `own_car`: own a car or not
    `own_realty`: own a realty or not
    `income`: income of the applicant
    `education`: education level of the applicant
    `family_status`: family status of the applicant
    `housing_type`: housing type of the applicant
    `birthday`: birthday of the applicant
    `employed_days`: employed days of the applicant
    `still_working`: still working or not
    `occupation`: occupation of the applicant
    `fam_members`:  family members of the applicant
    `result`: result of the prediction
    `date_prediction`: date of the prediction

### Modelling

## Contributing

We welcome contributions to this project! Here's how you can contribute:

1. Fork the Repository
2. Clone the Repository
3. Create a New Branch
4. Make Your Changes
5. Commit Your Changes
6. Push Your Changes
7. Submit a Pull Request
