import great_expectations as ge
import shutil
import os
import pandas as pd
from pyteamcity import TeamCity
from sqlalchemy import create_engine, Column, String, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pyteamcity import TeamCity

Base = declarative_base()


class DataProblemsStatistics(Base):
    __tablename__ = "data_problems_statistics"

    id = Column(Integer, primary_key=True, autoincrement=True)
    file_name = Column(String)
    column = Column(String)
    expectation_type = Column(String)
    unexpected_values = Column(Text)


def read_and_validate_file(df):
    context = ge.DataContext("gx")
    expectation_suite_name = "external.table.warning"
    suite = context.get_expectation_suite(expectation_suite_name)

    if suite is None:
        suite = context.create_expectation_suite(expectation_suite_name)

    ge_df = ge.dataset.PandasDataset(df, expectation_suite=suite)

    ge_df.expect_column_values_to_be_in_set(
        column="CODE_GENDER", value_set=["F", "M"]
    )
    ge_df.expect_column_values_to_be_in_set(
        column="FLAG_OWN_CAR", value_set=["Y", "N"]
    )
    ge_df.expect_column_values_to_be_in_set(
        column="FLAG_OWN_REALTY", value_set=["Y", "N"]
    )
    ge_df.expect_column_values_to_be_in_set(
        column="NAME_INCOME_TYPE",
        value_set=[
            "Working",
            "Commercial associate",
            "State servant",
            "Student",
            "Pensioner",
        ],
    )
    ge_df.expect_column_values_to_be_in_set(
        column="NAME_EDUCATION_TYPE",
        value_set=[
            "Higher education",
            "Secondary / secondary special",
            "Incomplete higher",
            "Lower secondary",
            "Academic degree",
        ],
    )
    ge_df.expect_column_values_to_be_in_set(
        column="NAME_FAMILY_STATUS",
        value_set=[
            "Civil marriage",
            "Married",
            "Single / not married",
            "Separated",
            "Widow",
        ],
    )
    ge_df.expect_column_values_to_be_in_set(
        column="NAME_HOUSING_TYPE",
        value_set=[
            "Rented apartment",
            "House / apartment",
            "Municipal apartment",
            "With parents",
            "Co-op apartment",
            "Office apartment",
        ],
    )
    ge_df.expect_column_values_to_be_between(
        column="CNT_CHILDREN", min_value=0
    )
    ge_df.expect_column_values_to_be_between(
        column="AMT_INCOME_TOTAL", min_value=0
    )
    ge_df.expect_column_values_to_be_between(column="DAYS_BIRTH", max_value=0)
    ge_df.expect_column_values_to_be_between(
        column="DAYS_EMPLOYED", max_value=0
    )
    ge_df.expect_column_values_to_be_in_set(
        column="FLAG_MOBIL", value_set=[0, 1]
    )
    ge_df.expect_column_values_to_be_in_set(
        column="FLAG_WORK_PHONE", value_set=[0, 1]
    )
    ge_df.expect_column_values_to_be_in_set(
        column="FLAG_PHONE", value_set=[0, 1]
    )
    ge_df.expect_column_values_to_be_in_set(
        column="FLAG_EMAIL", value_set=[0, 1]
    )
    ge_df.expect_column_values_to_be_between(
        column="CNT_FAM_MEMBERS", min_value=0
    )
    ge_df.expect_column_values_to_be_between(
        column="CNT_FAM_MEMBERS",
        min_value=0,
        parse_strings_as_datetimes=True,
    )
    ge_df.expect_column_values_to_be_in_set(
        column="APPROVED", value_set=[0, 1]
    )

    validation_result = ge_df.validate()

    return validation_result


def process_file(file_path, folder_b, folder_c):
    db_url = "postgresql://postgres:121199@localhost/dsp"
    df = pd.read_csv(file_path)
    validation_result = read_and_validate_file(df)

    if validation_result["success"]:
        store_file_in_folder(file_path, folder_c)
    else:
        if all(
            result["success"] is False
            for result in validation_result["results"]
        ):
            store_file_in_folder(file_path, folder_b)

            save_data_problems_statistics(validation_result, db_url)

        else:
            split_file_and_save_problems(
                file_path, folder_b, folder_c, validation_result, db_url
            )

    if not validation_result["success"]:
        alert_user_with_teams_notification()


def store_file_in_folder(file_path, destination_folder):
    shutil.move(
        file_path,
        os.path.join(destination_folder, os.path.basename(file_path)),
    )


def save_data_problems_statistics(validation_result, db_url):
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    file_name = os.path.basename(validation_result["meta"]["data_asset_name"])
    for result in validation_result["results"]:
        if not result["success"]:
            column = result["expectation_config"]["kwargs"]["column"]
            expectation_type = result["expectation_config"]["expectation_type"]
            unexpected_values = str(result["result"]["unexpected_list"])

            stat = DataProblemsStatistics(
                file_name=file_name,
                column=column,
                expectation_type=expectation_type,
                unexpected_values=unexpected_values,
            )
            session.add(stat)

    session.commit()
    session.close()


def split_file_and_save_problems(
    file_path, folder_b, folder_c, validation_result, db_url
):
    df = pd.read_csv(file_path)

    problematic_rows = []
    for result in validation_result["results"]:
        if not result["success"]:
            problematic_rows.extend(result["result"]["unexpected_index_list"])

    if problematic_rows:
        df_problems = df.loc[problematic_rows]
        df_no_problems = df.drop(problematic_rows)

        save_data_problems_statistics(validation_result, db_url)

        problems_file_path = os.path.join(
            folder_b, f"file_with_data_problems_{os.path.basename(file_path)}"
        )
        df_problems.to_csv(problems_file_path, index=False)

        no_problems_file_path = os.path.join(
            folder_c,
            f"file_without_data_problems_{os.path.basename(file_path)}",
        )
        df_no_problems.to_csv(no_problems_file_path, index=False)

    else:
        store_file_in_folder(file_path, folder_c)


def alert_user_with_teams_notification():
    teamcity = TeamCity()
    teamcity.post_message(
        "Data quality issues detected. Check the logs for details."
    )
