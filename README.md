# Software_Usage_Dashboard
This project that simulates SaaS usage data ingestion, stores the data in a SQLite database, and provides an interactive dashboard for analyzing application usage and estimated software spend.

The project demonstrates a lightweight data pipeline, basic data modeling, and interactive analytics using Python and Streamlit.

## Tech Stack

- Python
- SQLite
- Pandas
- Streamlit
- FastAPI (Mock API)
- Uvicorn

## Project Overview

Many companies struggle to understand how their employees use software applications and how much those tools actually cost. This project simulates a simple software usage intelligence platform that ingests application activity data and visualizes usage patterns.

The dashboard allows users to:

- Filter usage data by company, department, and date
- View application usage metrics
- Analyze estimated SaaS spend by application
- Explore usage data interactively

---

## Key Features

**Simulated Software Usage API**

A mock API generates realistic SaaS usage activity.

**Data Ingestion Pipeline**

Python scripts retrieve API data and store it in a structured SQLite database.

**Data Modeling**

Usage data and user data are joined to create an enriched dataset for analytics.

**Interactive Dashboard**

A Streamlit dashboard provides filters and visualizations for usage insights.

**Estimated SaaS Spend**

The dashboard estimates SaaS spend by multiplying active users by seat cost.

---

## Project Structure
saas-usage-intelligence-dashboard
│
├── api/
│ └── mock_api_server.py
│
├── dashboard/
│ └── app.py
│
├── database/
│ └── usage_data.db
│
├── scripts/
│ ├── generate_data.py
│ └── ingest_api_data.py
│
├── requirements.txt
├── README.md
└── .gitignore

### Install Dependencies
pip install -r requirements.txt

### Start the Mock API
uvicorn api.mock_api_server:app --reload

### Run Data Ingestion
python scripts/ingest_api_data.py

### Launch the Dashboard
streamlit run dashboard/app.py


---
## Future Improvements
- Cloud database integration
- Real SaaS API integrations
- Additional usage analytics
- Advanced cost optimization insights
---

## Author
Built as a portfolio project demonstrating data engineering and analytics workflows using Python.


