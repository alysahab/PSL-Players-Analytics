# PSL Cricket Analytics Dashboard

An interactive, cloud‐backed Streamlit visualization dashboard for the Pakistan Super League (2016–2024).  
*(Data ingestion & ETL pipeline is maintained in a separate repository; see [**ETL Pipeline**](https://github.com/alysahab/PSL-Web-Scraping-ETL).)*


## 🏏 Project Overview

This repository hosts the **visualization layer** of a comprehensive PSL analytics platform:

- **Streamlit dashboard** presenting batting and bowling KPIs, leaderboards, and player-specific analytics.  
- **Dynamic data access** via SQL + Python backed by AWS MySQL RDS for real-time querying.  
- **Cloud-based storage** ensures scalable, secure data hosting and supports scheduled ETL updates.  

---

## ✨ Features

- **Streamlit Interface:**  
  - Sidebar filters for Season, Batsman, Bowler, and module views (**Overall** vs. **Player**).  
  - Dual tabs for **Charts** & **Details** (raw data tables).  

- **Overall Modules:**  
  - Top 10 Runs, Batting Average, Strike Rate, Boundaries.  
  - Top 10 Wickets, Bowling Average, Economy Rate, Strike Rate.  

- **Player Modules:**  
  - **Batting**: KPI metrics (Matches, Runs, Avg, SR, Fours, Sixes, 50s, 100s) and charts (Runs by season, vs. opponent, dismissal & wicket‐type breakdowns).  
  - **Bowling**: KPI metrics (Innings, Balls, Runs conceded, Wickets, Bowling Avg, Economy Rate, Strike Rate, Dot Ball %, Maidens, Best Bowling Innings) and charts (Wickets by season, avg & SR vs. teams, wickets/economy trends, distribution percentages).  

- **SQL + Python Integration:**  
  - All data queries executed via SQLAlchemy in `dbhelper.py` using Python.  
  - **Streamlit caching** minimizes redundant queries and speeds up interactions.  

- **Cloud-Based Storage:**  
  - AWS MySQL RDS hosting a normalized, indexed schema (`idx_batsman_season`, `idx_bowling_season`).  
  - Supports dynamic, scheduled ETL updates for up-to-date analytics.  

---

## 🏗 Technical Architecture

<div align="center">
  
| Layer            | Technologies                                   |
|------------------|------------------------------------------------|
| **Visualization**| Streamlit, Plotly Express (`app.py` & `visuals.py`)                     |
| **Backend**      | Python, SQLAlchemy, PyMySQL (`dbhelper.py`)    |
| **Database**     | AWS MySQL RDS                                  |
| **ETL Pipeline** | Python, Selenium, BeautifulSoup, Pandas [ETL](https://github.com/alysahab/PSL-Web-Scraping-ETL) |
| **Deployment**   | Streamlit Cloud / AWS EC2                      |
  
</div>


VIEW VISUALIZATION [DASHBOARD](https://psl-players-stats.streamlit.app/)

