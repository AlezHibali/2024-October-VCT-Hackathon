import boto3
import json
import os

def process_json(data):
    # Split the concatenated string into individual dictionary strings
    dict_strings = data.replace('"', '').replace("'", '"').split("}{")

    # Create a list to hold the dictionaries
    dicts = []

    # Handle the first dictionary
    first_dict = dict_strings[0] + '}'
    dicts.append(json.loads(first_dict))

    # Handle the remaining dictionaries
    for i in range(1, len(dict_strings)):
        if i == len(dict_strings) - 1:  # Last dict doesn't need the closing brace
            dicts.append(json.loads('{' + dict_strings[i]))
        else:
            dicts.append(json.loads('{' + dict_strings[i] + '}'))

    # Extracting personal info and player info
    personal_info = dicts[0]  # First dictionary for personal info
    agent_infos = dicts[1:-1]  # Remaining dictionaries for player info

    # Print results
    # print("Personal Info:", personal_info)
    # for idx, player_info in enumerate(agent_infos):
    #     print(f"Agent Info {idx + 1}:", player_info)

    return personal_info, agent_infos


def process_data(personal_info, agent_infos):
    # Extract required data from personal_info
    player_id = personal_info['Player ID']
    team_acronym = personal_info['Team Acronym']
    region = personal_info['Region']

    # Initialize lists to collect valid values
    ratings = []
    acs_values = []
    adr_values = []
    kast_values = []
    agent_names = []

    # Loop through agent_infos to gather agent names and valid values
    for agent_info in agent_infos:
        # Append the agent name
        agent_names.append(agent_info.get('Agent', 'Unknown'))

        # Safely collect valid values for each metric
        rating = agent_info.get('Rating', '').strip()
        if rating:  # Only consider non-empty values
            ratings.append(float(rating))

        acs = agent_info.get('ACS', '').strip()
        if acs:  # Only consider non-empty values
            acs_values.append(float(acs))

        adr = agent_info.get('ADR', '').strip()
        if adr:  # Only consider non-empty values
            adr_values.append(float(adr))

        kast = agent_info.get('KAST %', '').strip('%').strip()
        if kast:  # Only consider non-empty values
            kast_values.append(float(kast))

    # Function to calculate the average of the top three valid values
    def average_of_top_three(values):
        if len(values) == 0:
            return 0
        # Sort the values in descending order and take the top three
        top_three = values[:3]
        return sum(top_three) / len(top_three)

    # Calculate averages using the top three valid entries
    avg_rating = average_of_top_three(ratings)
    avg_acs = average_of_top_three(acs_values)
    avg_adr = average_of_top_three(adr_values)
    avg_kast = average_of_top_three(kast_values)

    # Prepare the output
    output = {
        "Player ID": player_id,
        "Team Acronym": team_acronym,
        "Region": region,
        "Agent Names": agent_names[:3],  # Get first three agent names
        "Average Rating": round(avg_rating, 2),  # Rounded to 2 decimal places
        "Average ACS": round(avg_acs, 1),  # Rounded to 1 decimal place
        "Average ADR": round(avg_adr, 1),  # Rounded to 1 decimal place
        "Average KAST": f"{int(avg_kast)}%",  # Convert to integer percentage
    }

    return output

# Set the AWS credentials in the environment variables
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

# Initialize a session using your AWS profile or specific credentials
lambda_client = boto3.client('lambda',region_name="us-east-1", aws_access_key_id=aws_access_key_id, 
      aws_secret_access_key=aws_secret_access_key)

# Set the Lambda function name and payload
function_name = 'VCT-Data-Query-nzfd5'
payload = {
      "agent": "",
      "actionGroup": "",
      "messageVersion": "",
      "function": "query_player",
      "parameters": [{
          "name": "player_id",
          "type": "string",
          "value": "zmjjkk"
        }]
}

try:
    # Invoke the Lambda function
    response = lambda_client.invoke(
        FunctionName=function_name,
        InvocationType='RequestResponse',  # 'RequestResponse' for synchronous, 'Event' for async
        Payload=json.dumps(payload)
    )

    # Read the response
    response_payload = json.load(response['Payload'])

    # print("Response from Lambda:", response_payload)
    # print("Info:", response_payload['response']['functionResponse']['responseBody']['TEXT']['body'])

    data = response_payload['response']['functionResponse']['responseBody']['TEXT']['body']
    
    personal_info, agent_infos = process_json(data)
    # print("Personal Info:", personal_info)
    # for idx, player_info in enumerate(agent_infos):
    #     print(f"Agent Info {idx + 1}:", player_info)

    output = process_data(personal_info, agent_infos)
    print("Output:", output)

except Exception as e:
    print(f"Error invoking Lambda function: {e}")