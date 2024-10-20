import pandas as pd
import os

# Load the merged CSV file
merged_file_path = 'merged_player_profiles.csv'
merged_data = pd.read_csv(merged_file_path)

# Define columns for each file type
basic_data_columns = ['Player ID', 'Real Name', 'Current Team', 'Player Region', 'Team Acronym', 'Status', 'Region', 'League', 'League_level']
others_columns = ['Player ID', 'Real Name', 'Recent Matches', 'Past Teams', 'Event Placements', '60 days Agent Stats']
all_time_agent_data_columns = ['Player ID', 'Real Name', 'Agent', 'Use %', 'Rounds Played', 'Rating', 'ACS', 'K/D', 'ADR', 'KAST %', 
                                'KPR', 'APR', 'FKPR', 'FDPR', 'Kills', 'Deaths', 'Assists', 'First Bloods', 
                                'First Deaths']

# Define categories and their corresponding league levels
categories = {
    'vct-challengers': 'vct-challengers',
    'vct-international': 'vct-international',
    'game-changers': 'game-changers',
    'no-league': None  # For players not in any league
}

# Create base directory for categorized data
base_dir = 'categorized-vct-player-stat'
os.makedirs(base_dir, exist_ok=True)

# Initialize lists to store categorized data
for category, league_level in categories.items():
    category_dir = os.path.join(base_dir, category)
    os.makedirs(category_dir, exist_ok=True)

    # Filter data based on League_level
    if league_level:
        filtered_data = merged_data[merged_data['League_level'] == league_level]
    else:
        filtered_data = merged_data[~merged_data['League_level'].isin(categories.values())]

    # Save basic_data.csv
    basic_data = filtered_data[basic_data_columns].drop_duplicates(subset=['Player ID'])
    basic_data.to_csv(os.path.join(category_dir, 'basic_data.csv'), index=False)

    # Save others.csv
    others = filtered_data[others_columns].drop_duplicates(subset=['Player ID'])
    others.to_csv(os.path.join(category_dir, 'others.csv'), index=False)

    # Save all_time_agent_data.csv
    all_time_agent_data = filtered_data[all_time_agent_data_columns]
    all_time_agent_data.to_csv(os.path.join(category_dir, 'all_time_agent_data.csv'), index=False)

print("CSV files have been categorized and saved successfully.")
