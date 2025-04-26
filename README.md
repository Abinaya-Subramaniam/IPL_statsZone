# 🏏 IPL StatZone - Interactive IPL Analytics Dashboard

![Dashboard Preview](https://abinaya-subramaniam-ipl-statszone-ipl-dashboard-elg7ds.streamlit.app/)

A Streamlit-powered interactive dashboard for analyzing Indian Premier League (IPL) match data from 2008-2024. Compare players, teams, venues, and seasons with beautiful visualizations.

## ✨ Features

- **Player Comparison**: Analyze "Player of the Match" performances  
- **Team Statistics**: Compare win percentages, head-to-head records  
- **Venue Analysis**: Pitch behavior and match results by stadium  
- **Season Trends**: Track team performance across IPL editions  
- **Interactive Visualizations**: Built with Matplotlib/Seaborn  
- **Responsive Design**: Works on desktop and mobile  

## 📋 Requirements

- Python 3.8+  
- Streamlit  
- Pandas  
- NumPy  
- Matplotlib  
- Seaborn

## 🚀 Installation

1. Clone the repository:

    ```bash
    git clone https://Abinaya-Subramaniam/IPL-StatZone.git
    cd IPL-StatZone
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the app:

    ```bash
    streamlit run ipl_dashboard.py
    ```

## 📊 Data Preprocessing

The dataset includes:

- 900+ IPL matches (2008-2024)  
- 15 teams  
- 50+ venues  
- Player of the Match records  

Initial preprocessing steps:

- Handled missing values  
- Standardized team names across seasons  
- Calculated derived metrics (win percentages, margins)  
- Formatted date fields for time-series analysis  

## 🖥️ Usage

- Select comparison type (Player/Team/Venue/Season)  
- Choose items to compare from the sidebar  
- Explore different analysis tabs:  
  - Performance Overview  
  - Trend Analysis  
  - Match Results  
  - Comparative Stats  
  - Detailed Records  

---

Happy analyzing and may the best team win! 🏆
