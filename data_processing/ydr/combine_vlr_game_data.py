import pandas as pd
import ast
import re

# Read the CSV file
file_path = 'D:\\Coding\\VCT_agent\\data_processing\\player_profiles_region.csv'
player_data = pd.read_csv(file_path)

# Function to normalize the All Time Agent Stats
def normalize_agent_stats(row):
    agent_stats = row['All Time Agent Stats']

    # Check if the agent stats are empty or contain the placeholder
    if pd.isna(agent_stats) or agent_stats == "[{'record': 'record not found'}]":
        return None  # Skip this row
    
    agents = ast.literal_eval(agent_stats)
    agents_df = pd.DataFrame(agents)

    # Add other columns to the new DataFrame
    for col in player_data.columns:
        if col != 'All Time Agent Stats':
            agents_df[col] = row[col]
    
    return agents_df

# Expand the All Time Agent Stats and concatenate back to a single DataFrame
expanded_rows = []
for index, row in player_data.iterrows():
    expanded_row = normalize_agent_stats(row)
    if expanded_row is not None:
        expanded_rows.append(expanded_row)

# Combine all expanded DataFrames into one
expanded_player_data = pd.concat(expanded_rows, ignore_index=True)

# Replace empty cells with 'N/A'
expanded_player_data.fillna('N/A', inplace=True)

# Clean the 'Current Team' column
def clean_team_name(team_name):
    # Use regex to extract the team name
    match = re.search(r"'Team Name': '([^']*)'", team_name)
    if match:
        team = match.group(1)  # Extract the team name
        return team if team != 'Team not found' else 'N/A'
    return 'N/A'  # Default if no match found

# Apply the cleaning function to 'Current Team'
expanded_player_data['Current Team'] = expanded_player_data['Current Team'].apply(clean_team_name)

# Rearranging columns
# Define the desired order of columns
desired_columns = [
    'Player ID', 'Real Name', 'Current Team', 'Recent Matches', 
    'Past Teams', 'Player Region',
    'Agent', 'Use %', 'Rounds Played', 'Rating', 
    'ACS', 'K/D', 'ADR', 'KAST %', 'KPR', 'APR', 
    'FKPR', 'FDPR', 'Kills', 'Deaths', 'Assists', 
    'First Bloods', 'First Deaths',
    'Event Placements', '60 days Agent Stats'
]

# Reindex the DataFrame according to the desired column order
expanded_player_data = expanded_player_data[desired_columns]

# Save the expanded DataFrame to a new CSV file
expanded_file_path = 'D:\\Coding\\VCT_agent\\data_processing\\expanded_player_profiles.csv'
expanded_player_data.to_csv(expanded_file_path, index=False)

# Display the first few rows of the expanded dataset
print(expanded_player_data.head())
print(f"Data saved to {expanded_file_path}")
