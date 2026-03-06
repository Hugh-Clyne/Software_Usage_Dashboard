from fastapi import FastAPI, HTTPException, Query
import pandas as pd
import os
from typing import Optional
from datetime import date

app = FastAPI()

#current directory and project root
cd = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(cd, ".."))

#path to the data
users_path = os.path.join(project_root, "data", "users.csv")
usage_path = os.path.join(project_root, "data", "usage_daily.csv")

# #reading data
user_df = pd.read_csv(users_path)
usage_df = pd.read_csv(usage_path)

#helper functions
def filter_usage_data(df:pd.DataFrame,
    end_date: Optional[date]=None,
    company: Optional[str] = None,
    app: Optional[str] = None,
    ):
    if end_date:
        df = df.copy()
        df["date"] = pd.to_datetime(df["date"]).dt.date
        df = df[df["date"] <= end_date]

    if company:
        df = df[df['company'] == company]

    if app:
        df = df[df['app'] == app]

    return df

def filter_user_data(df:pd.DataFrame,
    company: Optional[str] = None,
    user_id: Optional[int] = None,
    department: Optional[str] = None,
    ):
    if company:
        df = df[df['company'] == company]
    if user_id is not None:
        df = df[df['user_id'] == user_id]
    if department:
        df = df[df['department'].str.lower() == department.lower()]
    return df

#creating endpoints
@app.get("/usage")
def get_usage(
    limit: int = Query(100, ge=1, le=5000),
    end_date: Optional[date] = Query(None, description="Includes records up to this date (YYYY-MM-DD)"),
    company: Optional[str] = None,
    app: Optional[str] = None
    ):
    """
    Return usage records (optionally filtered).
    """
    filtered_usage = filter_usage_data(usage_df, end_date=end_date, company=company, app=app)

    if filtered_usage.empty:
        raise HTTPException(status_code=404, detail="No usage records found matching the criteria.")

    total = len(filtered_usage)
    records = filtered_usage.head(limit).to_dict(orient="records")
    return {"count": len(records), "total": total, "data": records}

@app.get("/users")
def get_users(
    limit: int = Query(100, ge=1, le=1000),
    company: Optional[str] = None,
    user_id: Optional[int] = None,
    department: Optional[str] = None
    ):
    """
    Return user records (optionally limited).
    """
    filtered_users = filter_user_data(user_df, company=company, user_id=user_id, department=department)
    if filtered_users.empty:
        raise HTTPException(status_code=404, detail="No user records found matching the criteria.")

    records = filtered_users.head(limit).to_dict(orient="records")
    total = len(filtered_users)
    return {"count": len(records), "total": total, "data": records}

@app.get("/health")
def health():
    return {"status": "ok"}



