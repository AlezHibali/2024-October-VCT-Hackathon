import requests
import json
import gzip
import shutil
import time
import os
import boto3
from io import BytesIO


session = boto3.Session(
    aws_access_key_id='KEY_ID',
    aws_secret_access_key='THE_KEY',
    region_name='us-east-1'
)

s3 = session.client('s3')
BUCKET_NAME ='vct-hack-bucket'

S3_BUCKET_URL = "https://vcthackathon-data.s3.us-west-2.amazonaws.com"

# (game-changers, vct-international, vct-challengers)
LEAGUE = "game-changers"

# (2022, 2023, 2024)
YEAR = 2024

def report_bucket_usage():
    bucket_name = BUCKET_NAME  # Replace with your bucket name
    size, file_count = get_bucket_size(bucket_name)

    # Print results
    print(f"Bucket Usage: {size / (1024 ** 2):.2f} MB")
    print(f"Total files: {file_count}")

def get_bucket_size(bucket_name):
    total_size = 0
    total_files = 0

    # List all objects in the bucket
    paginator = s3.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=bucket_name):
        if 'Contents' in page:
            for obj in page['Contents']:
                total_size += obj['Size']
                total_files += 1

    return total_size, total_files

def move_file_to_s3(local_file_path, s3_file_path):
    bucket_name ='vct-hack-bucket'
    print(local_file_path, " moved to s3")
    s3.upload_file(local_file_path, bucket_name, s3_file_path)
    
    # Wait until the object exists in S3
    waiter = s3.get_waiter('object_exists')
    waiter.wait(Bucket=bucket_name, Key=s3_file_path)

    print(f"{local_file_path} successfully uploaded to S3 as {s3_file_path}")

def download_gzip_and_write_to_json(file_name, valid_file_name = None):
    if os.path.isfile(f"{file_name}.json"):
        return False

    remote_file = f"{S3_BUCKET_URL}/{file_name}.json.gz"
    response = requests.get(remote_file, stream=True)

    if response.status_code == 200:
        gzip_bytes = BytesIO(response.content)
        with gzip.GzipFile(fileobj=gzip_bytes, mode="rb") as gzipped_file:
            # Determine the filename to use
            output_file_name = f"{valid_file_name}.json" if valid_file_name is not None else f"{file_name}.json"

            # Write the gzipped file to the output
            with open(output_file_name, 'wb') as output_file:
                shutil.copyfileobj(gzipped_file, output_file)
                print(f"{output_file.name} written")

            # Print the file name and delete the file
            move_file_to_s3(output_file_name, output_file_name)
            os.remove(output_file_name)
            print(f"{output_file_name} has been deleted")
            
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

    # Define the path to your S3 bucket and file
    s3_bucket_name = 'vct-hack-bucket'
    s3_mapping_file = f"{LEAGUE}/esports-data/mapping_data.json"

    # Download the mapping data from S3
    s3_client = session.client('s3')

    # Create a temporary local file path for the mapping data
    local_mapping_file = 'temp_mapping_data.json'

    # Download the file from S3
    s3_client.download_file(s3_bucket_name, s3_mapping_file, local_mapping_file)

    # Load the mapping data from the downloaded file
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
        
        if response:
            game_counter += 1
            if game_counter % 10 == 0:
                print(f"----- Processed {game_counter} games, current run time: {round((time.time() - start_time)/60, 2)} minutes")

    # Clean up the temporary mapping data file after processing
    os.remove(local_mapping_file)


if __name__ == "__main__":
    download_esports_files()
    download_games()
    report_bucket_usage()
    
