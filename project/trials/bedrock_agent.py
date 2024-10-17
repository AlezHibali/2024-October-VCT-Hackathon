import boto3
import os

# Set the AWS credentials in the environment variables
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

# Initialize the Bedrock client
bedrock_client = boto3.client("bedrock-agent-runtime",region_name="us-east-1", aws_access_key_id=aws_access_key_id, 
      aws_secret_access_key=aws_secret_access_key)

response = bedrock_client.invoke_agent(
    agentId='KP6HZVL1HR',      # Identifier for Agent
    agentAliasId='RXUHMKTWFJ', # Identifier for Agent Alias
    sessionId='session123',    # Identifier used for the current session
    inputText='Build a team of five Chinese players'
)

print(response)

output = ""

stream = response.get('completion')
if stream:
    for event in stream:
        chunk = event.get('chunk')
        if chunk:
            output += chunk.get('bytes').decode()

print(output)
