from flask import Flask, render_template, request, Response
import time
import waitress
import random
import boto3
import os
from project.utils import process_json, process_data
import json
from botocore.config import Config
import uuid

CURRENT_FUN_FACT_INDEX = 0

# Set the AWS credentials in the environment variables
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

# Initialize AWS clients
lambda_client = boto3.client('lambda',region_name="us-east-1", aws_access_key_id=aws_access_key_id, 
      aws_secret_access_key=aws_secret_access_key)

# bedrock_client = boto3.client("bedrock-agent-runtime",region_name="us-east-1", aws_access_key_id=aws_access_key_id, 
#       aws_secret_access_key=aws_secret_access_key)
# agentId = "KP6HZVL1HR"
# agentAliasId = "BMSKKW5PF7"

my_config = Config(
    region_name="sa-east-1",
    read_timeout=180,  # Set the desired read timeout (in seconds)
    connect_timeout=60  # You can also adjust the connect timeout if needed
)

bedrock_client = boto3.client("bedrock-agent-runtime", aws_access_key_id=aws_access_key_id, 
      aws_secret_access_key=aws_secret_access_key, config=my_config)

agentId = "ERJAR1TKQ1"
agentAliasId = "X7DHXGLQGQ" # v5

def get_lambda_response(player_id):
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
            "value": player_id
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
        data = response_payload['response']['functionResponse']['responseBody']['TEXT']['body']
        
        personal_info, agent_infos = process_json(data)
        output = process_data(personal_info, agent_infos)

        # print(output)
        return output

    except Exception as e:
        print(f"Error invoking Lambda function: {e}")
        return None


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message", "")
    
    def generate_response():
        if user_message:
            # EXAMPLE
            # file_path = "assets/text/dummy_error.txt"
            # with open(file_path, 'r') as file:
            #     output = file.read()

            # Invoke the Bedrock agent
            session_id = str(uuid.uuid4())
            print(f"Session ID: {session_id}")
            
            response = bedrock_client.invoke_agent(
                agentId=agentId,      # Identifier for Agent
                agentAliasId=agentAliasId, # Identifier for Agent Alias
                sessionId=session_id,    # Identifier used for the current session
                inputText=user_message
            )

            output = ""
            stream = response.get('completion')
            if stream:
                for event in stream:
                    chunk = event.get('chunk')
                    if chunk:
                        output += chunk.get('bytes').decode()

            # Handle error message
            if output == "Sorry, I am unable to assist you with this request.":
                output = "Sorry, I am unable to assist you with this request.\\n You are receiving this message possibly due to a glitch or excessive traces in our bot. Please try again!"

            for char in output:
                yield f"{char}"
                time.sleep(0.01)  # Simulate typing effect

        else:
            fallback_message = "I didn't catch that. Could you please repeat?"
            for char in fallback_message:
                yield f"{char}"
                time.sleep(0.01)  # Simulate typing effect

    return Response(generate_response(), mimetype='text/event-stream')


@app.route('/api/funfact', methods=['GET'])
def fun_fact():
    with open('assets/text/fun_facts.txt', 'r') as file:
        fun_facts = file.readlines()

    # Remove newline characters from each fact
    fun_facts = [fact.strip() for fact in fun_facts]

    # Select a random fun fact diff from last one
    global CURRENT_FUN_FACT_INDEX
    new_index = CURRENT_FUN_FACT_INDEX
    while new_index == CURRENT_FUN_FACT_INDEX:
        new_index = random.randint(0, len(fun_facts) - 1)
    CURRENT_FUN_FACT_INDEX = new_index
    fact = fun_facts[new_index]

    return {"fun_fact": fact}


"""
API endpoint to get player data by invoking a Lambda function.
"""
@app.route('/api/player/<string:player_id>', methods=['GET'])
def player_data(player_id):
    output = get_lambda_response(player_id)
    if output is not None:
        return {"player_stat": output}
    else:
        return {"error": "Unable to retrieve player data."}


@app.route('/api/wait_message', methods=['GET'])
def wait_messs():
    def generate_response():
        with open('assets/text/bot_wait.txt', 'r') as file:
            wait_messages = file.readlines()

        # Remove newline characters from each fact
        wait_messages = [msg.strip() for msg in wait_messages]
        output = random.choice(wait_messages)  # Select a random wait message

        for char in output:
            yield f"{char}"
            time.sleep(0.05)  # Simulate typing effect

    return Response(generate_response(), mimetype='text/event-stream')


# python -m waitress --host=0.0.0.0 --port=5001 project.app:app
if __name__ == "__main__":
    waitress.serve(app, host="0.0.0.0", port=5001)
