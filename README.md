# PSL-Players_stats

A comprehensive data analysis project focused on extracting, cleaning, and analyzing player statistics from the Pakistan Super League (PSL). This project gathers detailed insights about each player, including their batting, bowling, and personal information, providing a holistic view of player performance.

## 📊 Project Overview

The **PSL-Players_stats** project involves the complete data pipeline—from data extraction to cleaning—ensuring accurate and insightful information about PSL players. The primary aim is to provide a clean dataset that can be used for further analysis and visualization.

### Key Objectives:

- **Data Collection and Cleaning** ([Repo](https://github.com/alysahab/Web-Scraping-PSL-Data))
  - Extract data from PSL player pages (batting, bowling, and personal details).
  - Clean and organize the raw data into structured datasets.
- **Visualization**
  - Provide insights into individual player performances and overall trends.

## 🛠️ Project Structure

```
PSL-Players_stats/
├── Extraction Notebooks/
│    ├── Batters and Bowlers Data Extraction.ipynb
│    └── Players Data Extraction.ipynb
├── Cleaning Notebooks/
│    ├── Batting Data Cleaning.ipynb
│    ├── Bowling Data Cleaning.ipynb
│    ├── Players Data Cleaning.ipynb
│    ├── PSL Title Winners.ipynb
├── Visualization streamlit/
│    ├── app.py
│    ├── visual.py
│    ├── dbhelper.py
└── README.md                 # Project documentation
```

## 📋 Process Breakdown

1. **Data Extraction**
   - Used **Selenium** with **Threading** to scrape batting, bowling, and players' HTML content.
   - Used **BeautifulSoup** to extract data from HTML content.

2. **Data Cleaning**
   - Used **Pandas** for removing inconsistencies, handling missing values and invalid entries, and standardizing data.
   - Separate notebooks for cleaning batting, bowling, and player details.

3. **Database Integration**
   - Data is stored in an **AWS MySQL** database.
   - Data is fetched using MySQL commands in the dbhelper module.

4. **Insights Generation**
   - **Plotly** is used to provide comprehensive insights on each player's performance through interactive visuals in **Streamlit**.
   - Key metrics include:
     - **Batting**: Average, strike rate, total runs, centuries.
     - **Bowling**: Economy rate, wickets, bowling average.
     - **General**: Player playing role and team history.

5. **Deployed in Streamlit**
   - Deployed the [Dashboard](https://psl-players-stats.streamlit.app/) on **Streamlit**.

## 📊 Player Insights

The project offers detailed insights on PSL players, including:

- **Batting Performance**: Run analysis, strike rates, batting average, etc.
- **Bowling Performance**: Wickets, economy rates, and best figures, etc.
- **Player Profiles**: Teams played for, playing role, and overall career trajectory.
- **Historical Trends**: player contributions over seasons.

## 🚀 How to Run the Project

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/PSL-Players_stats.git
   cd PSL-Players_stats
   ```
   
2. **Ensure MySQL Database Setup:**
   - Import the cleaned [dataset](https://www.kaggle.com/datasets/alysahab/complete-psl-data-2016-2024) (batting_data, bowling_data and players_info) into your **MySQL** database (local machine or **AWS**).
   - Update the database connection details in the dbhelper module before running app.py.   


## 📈 Future Enhancements

- Implement a machine learning model for series-winning predictions and player recommendations based on their past performance.

## 🧰 Tools and Technologies

- Python (Pandas, BeautifulSoup, Selenium, Plotly)
- MySQL (local AWS integration)
- Streamlit (for interactive dashboard)

## 📚 References

- [Dashboard](https://psl-players-stats.streamlit.app/)
- [Data](https://www.kaggle.com/datasets/alysahab/complete-psl-data-2016-2024)
- [Data collection and Data cleaning repository](https://github.com/alysahab/Web-Scraping-PSL-Data)

