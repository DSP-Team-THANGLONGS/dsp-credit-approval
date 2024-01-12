from sqlalchemy.orm import Session

from . import models

import numpy as np
from psycopg2.extensions import register_adapter, AsIs


register_adapter(np.int64, AsIs)


def get_records(db: Session, limit: int = 10000):
    records = db.query(models.Records).limit(limit).all()
    return records


def save_record(db: Session, records: dict):
    # Assuming all lists have the same length
    num_records = len(records["own_car"])
    # Create a list to hold the Records objects
    db_records = []
    for i in range(num_records):
        db_record = models.Records(
            own_car=records["own_car"][i],
            own_realty=records["own_realty"][i],
            income=records["income"][i],
            education=records["education"][i],
            family_status=records["family_status"][i],
            housing_type=records["housing_type"][i],
            birthday=records["birthday"][i],
            employed_day=records["employed_day"][i],
            still_working=records["still_working"][i],
            occupation=records["occupation"][i],
            fam_members=records["fam_members"][i],
            result=records["result"][i],
            platform=records["platform"][i],
            date_prediction=records["date_prediction"][i],
        )
        db_records.append(db_record)
    db.add_all(db_records)
    db.commit()
    for db_record in db_records:
        db.refresh(db_record)
    return db_records
