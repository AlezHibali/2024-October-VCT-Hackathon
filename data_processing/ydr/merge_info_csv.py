import pandas as pd
import re

# Load the CSV files
base_file = pd.read_csv('expanded_player_data_wcn.csv')
match_file = pd.read_csv('players_info.csv')

def extract_matches_and_percentage(use_str):
    """
    Extracts total matches and use percentage from a string like '(23) 28%'
    """
    if pd.isna(use_str) or use_str == "":
        return None, None  # Return None for both columns if the string is empty or NaN
    
    # Use regex to capture the matches in parentheses and the percentage
    match = re.search(r'\((\d+)\)\s*(\d+)%', use_str)
    
    if match:
        total_matches = int(match.group(1))  # First captured group is total matches
        use_percentage = f"{match.group(2)}%"  # Second captured group is the percentage
        return total_matches, use_percentage
    else:
        return None, None  # Return None if the format doesn't match

def merge_data(base_file, match_file):
    # Initialize new columns for the data to be added with "N/A"
    base_file.loc[:, 'Team Acronym'] = "N/A"
    base_file.loc[:, 'Status'] = "N/A"
    base_file.loc[:, 'Region'] = "N/A"
    base_file.loc[:, 'League'] = "N/A"
    base_file.loc[:, 'League_level'] = "N/A"
    base_file.loc[:, 'Updated At'] = "N/A"

    # Strip whitespace
    match_file['Handle'] = match_file['Handle'].astype(str).str.strip()
    match_file['Player Name'] = match_file['Player Name'].astype(str).str.strip()

    # Create two new columns for Total Matches and Use Percentage
    base_file['Total Matches'], base_file['Use Percentage'] = zip(*base_file['Use %'].apply(extract_matches_and_percentage))
    use_percent_index = base_file.columns.get_loc('Use %')  # Get index of new column
    base_file.drop(columns=['Use %'], inplace=True)
    base_file.insert(use_percent_index, 'Total Matches', base_file.pop('Total Matches'))
    base_file.insert(use_percent_index + 1, 'Use Percentage', base_file.pop('Use Percentage'))
    
    # Create a dictionary from player_info for fast lookup by Handle (Player ID)
    player_info_dict = match_file.set_index('Handle').T.to_dict()

    # Initialize counts and lists for unmatched players
    unmatched_base = 0
    unmatched_match = 0
    unmatched_base_players = []
    unmatched_match_players = []

    # Iterate over base_file rows to fill in new data
    for i, row in base_file.iterrows():
        print(f"Processing row {i+1}/{len(base_file)}", end="\r")
        player_id = row['Player ID']
        real_name = row['Real Name']
        
        match = None
        # Try to match based on Player ID (Handle)
        if player_id in player_info_dict:
            match = player_info_dict[player_id]
        else:
            # If Player ID not found or Real Name is N/A, try matching by Real Name (Player Name)
            if pd.notna(real_name):
                match = match_file[match_file['Player Name'] == real_name]
                match = match.iloc[0].to_dict() if not match.empty else None

        # Fill in data if a match is found
        if match:
            base_file.loc[i, 'Team Acronym'] = match.get('Team Acronym', "N/A")
            base_file.loc[i, 'Status'] = match.get('Status', "N/A")
            base_file.loc[i, 'Region'] = match.get('Region', "NA")
            base_file.loc[i, 'League'] = match.get('League', "N/A")
            base_file.loc[i, 'League_level'] = match.get('League_level', "N/A")
            base_file.loc[i, 'Updated At'] = match.get('Updated At', "N/A")
        else:
            unmatched_base += 1  # Increment unmatched count for base_file
            unmatched_base_players.append(row['Player ID'])  # Add unmatched player ID to list
        
        # If Current Team is N/A or empty, and match is found, fill it with the Team Name from player_info
        if (row['Current Team'] == "N/A" or pd.isna(row['Current Team'])):
            if match:
                base_file.loc[i, 'Current Team'] = match.get('Team Name', "N/A")
            else:
                base_file.loc[i, 'Current Team'] = "N/A"

        # If Real Name is N/A, check in player_info if match is found and fill in Real Name
        if row['Real Name'] == "N/A" or pd.isna(row['Real Name']):
            if match:
                base_file.loc[i, 'Real Name'] = match.get('Player Name', "N/A")
            else:
                base_file.loc[i, 'Real Name'] = "N/A"
        
        # Handle NA in region
        if base_file.loc[i, 'Region'] == "N/A" or pd.isna(base_file.loc[i, 'Region']):
            if match:
                base_file.loc[i, 'Region'] = "NA"

    # Now check for unmatched players in match_file
    for _, match_row in match_file.iterrows():
        if match_row['Handle'] not in base_file['Player ID'].values:
            unmatched_match += 1  # Increment unmatched count for match_file
            unmatched_match_players.append(match_row['Handle'])  # Add unmatched player ID to list

    print("\nCounts of unmatched players:")
    print(f"Players in base_file not found in match_file: {unmatched_base}")
    print(f"Players in match_file not found in base_file: {unmatched_match}")

    # Print all unmatched players from both files
    # print("\nUnmatched players in base_file:")
    # for player_id in unmatched_base_players:
    #     try:
    #         print(player_id)
    #     except Exception as e:
    #         print("PRINT ERROR")

    # print("\nUnmatched players in match_file:")
    # for player_id in unmatched_match_players:
    #     try:
    #         print(player_id)
    #     except Exception as e:
    #         print("PRINT ERROR")

    return base_file

result_df = merge_data(base_file, match_file)
result_df.to_csv('merged_player_profiles_wcn.csv', index=False)

print("Test CSV file created: merged_player_profiles_wcn.csv")
