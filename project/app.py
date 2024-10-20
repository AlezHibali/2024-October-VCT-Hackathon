from flask import Flask, render_template, request, Response
import time
import waitress
import re
import random
import boto3
import os

CURRENT_FUN_FACT_INDEX = 0

# Set the AWS credentials in the environment variables
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

# Initialize the Bedrock client
bedrock_client = boto3.client("bedrock-agent-runtime",region_name="us-east-1", aws_access_key_id=aws_access_key_id, 
      aws_secret_access_key=aws_secret_access_key)


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message", "")
    
    def generate_response():
        if user_message:
            # # EXAMPLE
            # response = "Team formation: <Alez 1>, <Alez 2>, <Alez 3>, <Alez 4>, <Alez 5>. \nThis is a response from the bot. Processing more data... Here's some additional information... Final response complete."
            # for char in response:
            #     yield f"{char}"
            #     time.sleep(0.01)  # Simulate typing effect

            # Invoke the Bedrock agent
            response = bedrock_client.invoke_agent(
                agentId='KP6HZVL1HR',      # Identifier for Agent
                agentAliasId='BMSKKW5PF7', # Identifier for Agent Alias
                sessionId='vct-agent-session',    # Identifier used for the current session
                inputText=user_message
            )

            output = ""
            stream = response.get('completion')
            if stream:
                for event in stream:
                    chunk = event.get('chunk')
                    if chunk:
                        output += chunk.get('bytes').decode()

            # Replace newline characters with HTML <br> to preserve formatting
            formatted_output = output.replace("\n", "<br>")

            for char in formatted_output:
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
    # HARDCODED FUN FACTS
    fun_facts = [
        "EDward Gaming (EDG) became the first global champions from China in 2024 after defeating Team Heretics 3-2 in an epic grand final.",
        "EDG's player ZmjjKK set a new VCT best-of-five kill record with 111 kills and was named the first-ever official Champions MVP in 2024.",
        "The 2025 VCT season will introduce a revamped format, starting with a 12-team double-elimination bracket for each region, eliminating the group and play-in stages from 2024.",
        "Riot Games announced that the 2025 VCT Masters events will be held in Bangkok and Toronto, with the Champions event in Paris.",
        "The 2026 VCT Champions will take place in China, and the 2027 event will be hosted in the Americas.",
        "VCT features regional Challengers events that feed into international Masters and Champions tournaments.",
        "The inaugural VCT Champions event in 2022 was won by OpTic Gaming in Los Angeles.",
        "VCT matches are played on the latest map pool, which Riot Games updates regularly to keep the competitive meta fresh.",
        "Players and teams earn Circuit Points in VCT events, which determine their qualification for Masters and Champions tournaments."
    ]

    # Select a random fun fact diff from last one
    global CURRENT_FUN_FACT_INDEX
    new_index = CURRENT_FUN_FACT_INDEX
    while new_index == CURRENT_FUN_FACT_INDEX:
        new_index = random.randint(0, len(fun_facts) - 1)
    CURRENT_FUN_FACT_INDEX = new_index
    fact = fun_facts[new_index]

    return {"fun_fact": fact}


# python -m waitress --host=0.0.0.0 --port=5001 project.app:app
if __name__ == "__main__":
    waitress.serve(app, host="0.0.0.0", port=5001)
