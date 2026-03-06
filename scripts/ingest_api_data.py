import os
import requests
import pandas as pd
import sqlite3

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, "database", "usage_data.db")

print("Writing SQLite DB to: ", db_path)

conn = sqlite3.connect(db_path)
conn.execute("PRAGMA foreign_keys = ON;")



#User data ingestion
response_users = requests.get("http://127.0.0.1:8000/users", params = {"limit":1000})
response_users.raise_for_status()
data1 = response_users.json()["data"]
df1 = pd.DataFrame(data1)
cursor = conn.cursor()

cursor.execute("""DROP TABLE IF EXISTS usage_logs""")
cursor.execute("""DROP TABLE IF EXISTS users""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    company TEXT,
    department TEXT,
    role TEXT,
    created_at datetime
)
""")
df1.to_sql("users", conn, if_exists="append", index=False)
print(f"Inserted {len(df1)} rows into users table")

#Usage data ingestion
response_usage = requests.get("http://127.0.0.1:8000/usage", params ={"limit":5000})
response_usage.raise_for_status()
data2 = response_usage.json()["data"]
df2 = pd.DataFrame(data2)

cursor.execute("""
CREATE TABLE IF NOT EXISTS usage_logs (
    date datetime NOT NULL,
    user_id INTEGER ,
    app TEXT,
    sessions INTEGER,
    minutes_used INTEGER,
    feature_actions INTEGER,
    errors INTEGER,
   seat_cost_usd INTEGER,
   FOREIGN KEY (user_id) REFERENCES users(user_id)
)
""")
df2.to_sql("usage_logs", conn, if_exists="append", index=False)
print(f"Inserted {len(df2)} rows into usage_logs table")
conn.commit()
conn.close()

print("Data ingestion completed successfully.")