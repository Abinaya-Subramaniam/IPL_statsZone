import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap

cricket_palette = {
    'primary': '#004ba0',  
    'secondary': '#d4af37',  
    'accent': '#2e8b57',  
    'highlight': '#e53935',  
    'background': '#f5f5f5'
}

st.set_page_config(
    page_title="IPL StatZone",
    page_icon="🏏",
    layout="wide"
)

@st.cache_data
def load_data():
    return pd.read_csv('./processed_ipl_dataset.csv')  

df = load_data()

st.title("🏏IPL StatZone - Analytics Dashboard (2008-2024)")
st.markdown("""
The **Indian Premier League (IPL)** is a professional Twenty20 cricket league in India, known for its thrilling matches, star players, and unforgettable moments.  

Use the Sidebar and Compare **players**, **teams**, **venues**, and **seasons** with rich visuals🔥.  
""")



if st.button("☰ Menu"):
    st.session_state.show_sidebar = not st.session_state.get("show_sidebar", False)

if st.session_state.get("show_sidebar", False):
    with st.sidebar:
        st.header("Comparison Filters")
        comparison_type = st.radio(
            "Select Comparison Type:",
            ("Player", "Team", "Venue", "Season")
        )

selection1 = None
selection2 = None

if comparison_type == "Player":
    players = sorted(df['player_of_match'].dropna().unique())
    selection1 = st.sidebar.selectbox("Select Player 1:", players)
    selection2 = st.sidebar.selectbox("Select Player 2:", [''] + players)
    
elif comparison_type == "Team":
    teams = sorted(set(df['team1'].unique()).union(set(df['team2'].unique())))
    selection1 = st.sidebar.selectbox("Select Team 1:", teams)
    selection2 = st.sidebar.selectbox("Select Team 2:", [''] + teams)
    
elif comparison_type == "Venue":
    venues = sorted(df['venue'].dropna().unique())
    selection1 = st.sidebar.selectbox("Select Venue 1:", venues)
    selection2 = st.sidebar.selectbox("Select Venue 2:", [''] + venues)
    
elif comparison_type == "Season":
    seasons = sorted(df['season'].unique())
    selection1 = st.sidebar.selectbox("Select Season 1:", seasons)
    selection2 = st.sidebar.selectbox("Select Season 2:", [''] + seasons)

def perform_analysis(comparison_type, selection1, selection2=None):
    st.header(f"{comparison_type} Analysis")
    
    if not selection1:
        st.warning("Please select at least one item to analyze")
        return
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Performance Overview", 
        "Trend Analysis", 
        "Match Results", 
        "Comparative Stats", 
        "Detailed Records"
    ])
    
    with tab1:
        st.subheader("Performance Overview")
        
        if comparison_type == "Player":
            player_matches = df[df['player_of_match'] == selection1]
            num_awards = len(player_matches)
            teams = set(player_matches['team1']).union(set(player_matches['team2']))
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Player of Match Awards", num_awards)
            with col2:
                st.metric("Teams Played against", len(teams))
            with col3:
                st.metric("First Award", player_matches['date'].min())
            
            fig, ax = plt.subplots(figsize=(10,4))
            sns.countplot(data=player_matches, x='season', color=cricket_palette['primary'])
            plt.title(f"{selection1}'s POTM Awards by Season")
            plt.xlabel("Season")
            plt.ylabel("Number of Awards")
            st.pyplot(fig)
            
        elif comparison_type == "Team":
            team_wins = df[df['winner'] == selection1]
            team_matches = df[(df['team1'] == selection1) | (df['team2'] == selection1)]
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Matches", len(team_matches))
            with col2:
                st.metric("Wins", len(team_wins))
            with col3:
                st.metric("Win Percentage", f"{len(team_wins)/len(team_matches)*100:.1f}%")
            
            fig, ax = plt.subplots(figsize=(10,4))
            team_season = team_matches.groupby(['season', 'winner']).size().unstack().fillna(0)
            team_season['losses'] = team_season.sum(axis=1) - team_season.get(selection1, 0)
            team_season[[selection1, 'losses']].plot(kind='bar', stacked=True, 
                                                    color=[cricket_palette['primary'], cricket_palette['highlight']], 
                                                    ax=ax)
            plt.title(f"{selection1}'s Performance by Season")
            plt.xlabel("Season")
            plt.ylabel("Number of Matches")
            st.pyplot(fig)
            
        elif comparison_type == "Venue":
            venue_matches = df[df['venue'] == selection1]
            home_team = venue_matches['city'].iloc[0] if 'city' in df.columns else "N/A"
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Matches Hosted", len(venue_matches))
            with col2:
                st.metric("Home City", home_team)
            with col3:
                st.metric("First Match", venue_matches['date'].min())
            
            fig, ax = plt.subplots(figsize=(8,6))
            venue_matches['result'].value_counts().plot(
                kind='pie', autopct='%1.1f%%', 
                colors=[cricket_palette['primary'], cricket_palette['secondary']],
                ax=ax
            )
            plt.title(f"Match Results at {selection1}")
            st.pyplot(fig)
            
        elif comparison_type == "Season":
            season_matches = df[df['season'] == selection1]
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Matches", len(season_matches))
            with col2:
                st.metric("Teams Participated", len(set(season_matches['team1']).union(set(season_matches['team2']))))
            with col3:
                st.metric("Super Overs", len(season_matches[season_matches['super_over'] == 'Y']))
            
            fig, ax = plt.subplots(figsize=(10,4))
            season_matches['winner'].value_counts().sort_values().plot(
                kind='barh', color=cricket_palette['primary'])
            plt.title(f"Team Wins in {selection1} Season")
            plt.xlabel("Number of Wins")
            st.pyplot(fig)
    
    with tab2:
        st.subheader("Trend Analysis")
        
        if comparison_type == "Player":
            player_trend = df[df['player_of_match'] == selection1].groupby('season').size()
            
            if selection2:
                player2_trend = df[df['player_of_match'] == selection2].groupby('season').size()
                fig, ax = plt.subplots(figsize=(10,5))
                player_trend.plot(kind='line', marker='o', label=selection1, color=cricket_palette['primary'])
                player2_trend.plot(kind='line', marker='o', label=selection2, color=cricket_palette['highlight'])
                plt.title(f"POTM Awards Trend: {selection1} vs {selection2}")
            else:
                fig, ax = plt.subplots(figsize=(10,5))
                player_trend.plot(kind='line', marker='o', color=cricket_palette['primary'])
                plt.title(f"{selection1}'s POTM Awards Trend")
            
            plt.xlabel("Season")
            plt.ylabel("Number of Awards")
            plt.grid(linestyle='--', alpha=0.5)
            plt.legend()
            st.pyplot(fig)
            
        elif comparison_type == "Team":
            team_trend = df[(df['team1'] == selection1) | (df['team2'] == selection1)]
            team_trend = team_trend.groupby(['season', 'winner']).size().unstack().fillna(0)
            team_trend['Win %'] = (team_trend.get(selection1, 0) / 
                                 (team_trend.sum(axis=1)) * 100)
            
            if selection2:
                team2_trend = df[(df['team1'] == selection2) | (df['team2'] == selection2)]
                team2_trend = team2_trend.groupby(['season', 'winner']).size().unstack().fillna(0)
                team2_trend['Win %'] = (team2_trend.get(selection2, 0) / 
                                      (team2_trend.sum(axis=1)) * 100)
                
                fig, ax = plt.subplots(figsize=(10,5))
                team_trend['Win %'].plot(kind='line', marker='o', label=selection1, color=cricket_palette['primary'])
                team2_trend['Win %'].plot(kind='line', marker='o', label=selection2, color=cricket_palette['highlight'])
                plt.title(f"Win Percentage Trend: {selection1} vs {selection2}")
            else:
                fig, ax = plt.subplots(figsize=(10,5))
                team_trend['Win %'].plot(kind='line', marker='o', color=cricket_palette['primary'])
                plt.title(f"{selection1}'s Win Percentage Trend")
            
            plt.xlabel("Season")
            plt.ylabel("Win Percentage")
            plt.ylim(0, 100)
            plt.grid(linestyle='--', alpha=0.5)
            plt.legend()
            st.pyplot(fig)
            
        elif comparison_type == "Venue":
            venue_trend = df[df['venue'] == selection1].groupby('season').size()
            
            if selection2:
                venue2_trend = df[df['venue'] == selection2].groupby('season').size()
                fig, ax = plt.subplots(figsize=(10,5))
                venue_trend.plot(kind='line', marker='o', label=selection1, color=cricket_palette['primary'])
                venue2_trend.plot(kind='line', marker='o', label=selection2, color=cricket_palette['highlight'])
                plt.title(f"Matches Hosted Trend: {selection1} vs {selection2}")
            else:
                fig, ax = plt.subplots(figsize=(10,5))
                venue_trend.plot(kind='line', marker='o', color=cricket_palette['primary'])
                plt.title(f"{selection1}'s Matches Hosted Trend")
            
            plt.xlabel("Season")
            plt.ylabel("Number of Matches")
            plt.grid(linestyle='--', alpha=0.5)
            plt.legend()
            st.pyplot(fig)
            
        elif comparison_type == "Season":
            season1_data = df[df['season'] == selection1]
            avg_runs1 = season1_data['target_runs'].mean()
            win_margin1 = season1_data['result_margin'].mean()
            
            if selection2:
                season2_data = df[df['season'] == selection2]
                avg_runs2 = season2_data['target_runs'].mean()
                win_margin2 = season2_data['result_margin'].mean()
                
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12,5))
                
                ax1.bar([selection1, selection2], [avg_runs1, avg_runs2], 
                       color=[cricket_palette['primary'], cricket_palette['highlight']])
                ax1.set_title("Average Target Runs")
                ax1.set_ylabel("Runs")

                ax2.bar([selection1, selection2], [win_margin1, win_margin2], 
                       color=[cricket_palette['primary'], cricket_palette['highlight']])
                ax2.set_title("Average Win Margin")
                ax2.set_ylabel("Runs/Wickets")
                
                st.pyplot(fig)
            else:
                st.write(f"Average Target Runs in {selection1}: {avg_runs1:.1f}")
                st.write(f"Average Win Margin in {selection1}: {win_margin1:.1f}")
    
    with tab3:
        st.subheader("Match Results Analysis")
        
        if comparison_type == "Player":
            player_matches = df[df['player_of_match'] == selection1]
            
            fig, ax = plt.subplots(figsize=(8,4))
            player_matches['result'].value_counts().plot(
                kind='bar', color=cricket_palette['primary'])
            plt.title(f"Match Result Types for {selection1}'s POTM Awards")
            plt.xlabel("Result Type")
            plt.ylabel("Count")
            st.pyplot(fig)

            fig, ax = plt.subplots(figsize=(8,4))
            sns.histplot(player_matches['result_margin'], bins=10, 
                        color=cricket_palette['accent'], kde=True)
            plt.title(f"Win Margins in {selection1}'s POTM Matches")
            plt.xlabel("Win Margin (Runs/Wickets)")
            st.pyplot(fig)
            
        elif comparison_type == "Team":
            team_matches = df[(df['team1'] == selection1) | (df['team2'] == selection1)]
            team_matches['team_role'] = np.where(team_matches['team1'] == selection1, 'Team1', 'Team2')
            team_matches['outcome'] = np.where(team_matches['winner'] == selection1, 'Won', 'Lost')
            
            fig, ax = plt.subplots(figsize=(8,6))
            sns.countplot(data=team_matches, x='toss_decision', hue='outcome',
                         palette=[cricket_palette['primary'], cricket_palette['highlight']])
            plt.title(f"Toss Decision Impact for {selection1}")
            plt.xlabel("Toss Decision")
            plt.ylabel("Count")
            st.pyplot(fig)
            
            fig, ax = plt.subplots(figsize=(8,4))
            team_matches['result'].value_counts().plot(
                kind='pie', autopct='%1.1f%%', 
                colors=[cricket_palette['primary'], cricket_palette['secondary']],
                ax=ax
            )
            plt.title(f"Result Types for {selection1}'s Matches")
            st.pyplot(fig)
            
        elif comparison_type == "Venue":
            venue_matches = df[df['venue'] == selection1]
            
            fig, ax = plt.subplots(figsize=(10,5))
            venue_matches['winner'].value_counts().head(10).sort_values().plot(
                kind='barh', color=cricket_palette['primary'])
            plt.title(f"Most Successful Teams at {selection1}")
            plt.xlabel("Number of Wins")
            st.pyplot(fig)
            
            fig, ax = plt.subplots(figsize=(10,5))
            sns.countplot(data=venue_matches, x='season', hue='result',
                         palette=[cricket_palette['primary'], cricket_palette['secondary']])
            plt.title(f"Match Results by Season at {selection1}")
            plt.xlabel("Season")
            plt.ylabel("Count")
            plt.xticks(rotation=45)
            st.pyplot(fig)
            
        elif comparison_type == "Season":
            season_matches = df[df['season'] == selection1]
            
            fig, ax = plt.subplots(figsize=(8,5))
            sns.histplot(season_matches['result_margin'], bins=15, 
                        color=cricket_palette['accent'], kde=True)
            plt.title(f"Win Margins Distribution in {selection1}")
            plt.xlabel("Win Margin (Runs/Wickets)")
            st.pyplot(fig)
            
            fig, ax = plt.subplots(figsize=(8,5))
            sns.scatterplot(data=season_matches, x='target_runs', y='result_margin',
                           hue='result', palette=[cricket_palette['highlight'], cricket_palette['primary']])
            plt.title(f"Target Runs vs. Result Margin in {selection1}")
            plt.xlabel("Target Runs")
            plt.ylabel("Result Margin")
            st.pyplot(fig)
    
    with tab4:
        st.subheader("Comparative Statistics")
        
        if not selection2:
            st.info("Select a second item to compare in the sidebar")
        else:
            if comparison_type == "Player":
                player1_matches = df[df['player_of_match'] == selection1]
                player2_matches = df[df['player_of_match'] == selection2]
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(f"{selection1} POTM Awards", len(player1_matches))
                with col2:
                    st.metric(f"{selection2} POTM Awards", len(player2_matches))
                
                fig, ax = plt.subplots(figsize=(10,5))
                player1_matches.groupby('season').size().plot(
                    kind='bar', color=cricket_palette['primary'], 
                    position=0, width=0.4, label=selection1)
                player2_matches.groupby('season').size().plot(
                    kind='bar', color=cricket_palette['highlight'], 
                    position=1, width=0.4, label=selection2)
                plt.title(f"POTM Awards Comparison: {selection1} vs {selection2}")
                plt.xlabel("Season")
                plt.ylabel("Number of Awards")
                plt.legend()
                st.pyplot(fig)
                
            elif comparison_type == "Team":
                team1_matches = df[(df['team1'] == selection1) | (df['team2'] == selection1)]
                team1_wins = len(team1_matches[team1_matches['winner'] == selection1])
                
                team2_matches = df[(df['team1'] == selection2) | (df['team2'] == selection2)]
                team2_wins = len(team2_matches[team2_matches['winner'] == selection2])
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(f"{selection1} Matches", len(team1_matches))
                    st.metric(f"{selection1} Wins", team1_wins)
                    st.metric(f"{selection1} Win %", f"{team1_wins/len(team1_matches)*100:.1f}%")
                with col2:
                    st.metric(f"{selection2} Matches", len(team2_matches))
                    st.metric(f"{selection2} Wins", team2_wins)
                    st.metric(f"{selection2} Win %", f"{team2_wins/len(team2_matches)*100:.1f}%")
                
                h2h = df[((df['team1'] == selection1) & (df['team2'] == selection2)) | 
                       ((df['team1'] == selection2) & (df['team2'] == selection1))]
                h2h_wins = h2h['winner'].value_counts()
                
                fig, ax = plt.subplots(figsize=(6,6))
                h2h_wins.plot(kind='pie', autopct='%1.1f%%', 
                             colors=[cricket_palette['primary'], cricket_palette['highlight']],
                             ax=ax)
                plt.title(f"Head-to-Head: {selection1} vs {selection2}")
                st.pyplot(fig)
                
            elif comparison_type == "Venue":
                venue1_matches = df[df['venue'] == selection1]
                venue2_matches = df[df['venue'] == selection2]
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(f"{selection1} Matches", len(venue1_matches))
                    st.metric(f"{selection1} Avg Target", f"{venue1_matches['target_runs'].mean():.1f}")
                with col2:
                    st.metric(f"{selection2} Matches", len(venue2_matches))
                    st.metric(f"{selection2} Avg Target", f"{venue2_matches['target_runs'].mean():.1f}")
                
                fig, ax = plt.subplots(figsize=(10,5))
                sns.boxplot(data=pd.concat([
                    venue1_matches.assign(Venue=selection1),
                    venue2_matches.assign(Venue=selection2)
                ]), x='Venue', y='result_margin', 
                palette=[cricket_palette['primary'], cricket_palette['highlight']])
                plt.title(f"Win Margin Comparison: {selection1} vs {selection2}")
                plt.ylabel("Win Margin (Runs/Wickets)")
                st.pyplot(fig)
                
            elif comparison_type == "Season":
                season1_matches = df[df['season'] == selection1]
                season2_matches = df[df['season'] == selection2]
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(f"{selection1} Matches", len(season1_matches))
                    st.metric(f"{selection1} Avg Target", f"{season1_matches['target_runs'].mean():.1f}")
                    st.metric(f"{selection1} Super Overs", len(season1_matches[season1_matches['super_over'] == 'Y']))
                with col2:
                    st.metric(f"{selection2} Matches", len(season2_matches))
                    st.metric(f"{selection2} Avg Target", f"{season2_matches['target_runs'].mean():.1f}")
                    st.metric(f"{selection2} Super Overs", len(season2_matches[season2_matches['super_over'] == 'Y']))
                
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14,6))
                
                season1_matches['winner'].value_counts().head(5).sort_values().plot(
                    kind='barh', color=cricket_palette['primary'], ax=ax1)
                ax1.set_title(f"Top Teams in {selection1}")
                
                season2_matches['winner'].value_counts().head(5).sort_values().plot(
                    kind='barh', color=cricket_palette['highlight'], ax=ax2)
                ax2.set_title(f"Top Teams in {selection2}")
                
                st.pyplot(fig)
    
    with tab5:
        st.subheader("Detailed Records")
        
        if comparison_type == "Player":
            player_matches = df[df['player_of_match'] == selection1]
            st.write(f"### All Matches Where {selection1} Won Player of the Match")
            st.dataframe(player_matches.sort_values('date', ascending=False).reset_index(drop=True))
            
        elif comparison_type == "Team":
            team_matches = df[(df['team1'] == selection1) | (df['team2'] == selection1)]
            st.write(f"### All Matches Involving {selection1}")
            st.dataframe(team_matches.sort_values('date', ascending=False).reset_index(drop=True))
            
        elif comparison_type == "Venue":
            venue_matches = df[df['venue'] == selection1]
            st.write(f"### All Matches at {selection1}")
            st.dataframe(venue_matches.sort_values('date', ascending=False).reset_index(drop=True))
            
        elif comparison_type == "Season":
            season_matches = df[df['season'] == selection1]
            st.write(f"### All Matches in {selection1} Season")
            st.dataframe(season_matches.sort_values('date').reset_index(drop=True))

perform_analysis(comparison_type, selection1, selection2)

st.markdown("---")
st.markdown("""
**IPL Analytics Dashboard**  
Data from 2008-2024 
""")