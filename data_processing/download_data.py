"""
Download game data from amazon g3 database
create folder under current dir

database file structure:

/vct-hackathon-2024 (root)
→ /fandom
  → *.xml
→ /game-changers
  → /esports-data
    → *.json.gz
  → /games
    → /2022
      → *.json.gz
    → /2023
      → *.json.gz
    → /2024
      → *.json.gz
→ /vct-challengers
  → /esports-data
    → *.json.gz
  → /games
    → /2023
      → *.json.gz
    → /2024
      → *.json.gz
→ /vct-international
  → /esports-data
    → *.json.gz
  → /games
    → /2022
      → *.json.gz
    → /2023
      → *.json.gz
    → /2024
      → *.json.gz

"""

import requests
import json
import gzip
import shutil
import time
import os
from io import BytesIO

S3_BUCKET_URL = "https://vcthackathon-data.s3.us-west-2.amazonaws.com"

# (game-changers, vct-international, vct-challengers)
LEAGUE = "game-changers"

# (2022, 2023, 2024)
YEAR = 2022

def download_gzip_and_write_to_json(file_name, valid_file_name = None):
    if os.path.isfile(f"{file_name}.json"):
        return False

    remote_file = f"{S3_BUCKET_URL}/{file_name}.json.gz"
    response = requests.get(remote_file, stream=True)

    if response.status_code == 200:
        gzip_bytes = BytesIO(response.content)
        with gzip.GzipFile(fileobj=gzip_bytes, mode="rb") as gzipped_file:
            if valid_file_name == None:
                with open(f"{file_name}.json", 'wb') as output_file:
                    shutil.copyfileobj(gzipped_file, output_file)
                print(f"{file_name}.json written")
            else:
                with open(f"{valid_file_name}.json", 'wb') as output_file:
                    shutil.copyfileobj(gzipped_file, output_file)
                print(f"{valid_file_name}.json written")
        
        # # Print the content that was written to the file
        # with open(f"{file_name}.json", 'r') as output_file:
        #     content = output_file.read()
        #     print(f"Content of {file_name}.json:\n{content[:500]}...\n")  # Print the first 500 characters for brevity
        
        return True
    elif response.status_code == 404:
        # Ignore
        return False
    else:
        print(response)
        print(f"Failed to download {file_name}")
        return False


def download_esports_files():
    directory = f"{LEAGUE}/esports-data"

    if not os.path.exists(directory):
        os.makedirs(directory)

    esports_data_files = ["leagues", "tournaments",
                          "players", "teams", "mapping_data"]
    for file_name in esports_data_files:
        download_gzip_and_write_to_json(f"{directory}/{file_name}")

def download_games():
    start_time = time.time()

    local_mapping_file = f"{LEAGUE}/esports-data/mapping_data.json"
    with open(local_mapping_file, "r") as json_file:
        mappings_data = json.load(json_file)

    local_directory = f"{LEAGUE}/games/{YEAR}"
    if not os.path.exists(local_directory):
        os.makedirs(local_directory)

    game_counter = 0
    MAX_GAMES = 10000

    for esports_game in mappings_data:
        if game_counter >= MAX_GAMES:
            break
        
        # Replace invalid characters in the filename
        sanitized_file_name = esports_game['platformGameId'].replace(':', '_')

        s3_game_file = f"{LEAGUE}/games/{YEAR}/{esports_game['platformGameId']}"

        s3_game_file_name = f"{LEAGUE}/games/{YEAR}/{sanitized_file_name}"

        response = download_gzip_and_write_to_json(s3_game_file, s3_game_file_name)
        
        if response == True:
            game_counter += 1
            if game_counter % 10 == 0:
                print(f"----- Processed {game_counter} games, current run time: {round((time.time() - start_time)/60, 2)} minutes")

if __name__ == "__main__":
    download_esports_files()
    download_games()