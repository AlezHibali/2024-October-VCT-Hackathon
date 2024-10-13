import boto3
import os

# Set the AWS credentials in the environment variables
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

# Initialize the Bedrock client
bedrock_client = boto3.client('bedrock',region_name="us-east-1", aws_access_key_id=aws_access_key_id, 
      aws_secret_access_key=aws_secret_access_key)

# agent_id = "YJALJUYVIR"

# Call GetFoundationModel API to check model properties
response = bedrock_client.get_foundation_model(
    modelIdentifier='anthropic.claude-3-5-sonnet-20240620-v1:0'
)

print(response)

# {'ResponseMetadata': {'RequestId': '5b83e975-20fa-489f-89ca-c53a092b79fc', 'HTTPStatusCode': 200, 'HTTPHeaders': {'date': 'Sun, 13 Oct 2024 22:29:20 GMT', 'content-type': 'application/json', 'content-length': '460', 'connection': 'keep-alive', 'x-amzn-requestid': '5b83e975-20fa-489f-89ca-c53a092b79fc'}, 'RetryAttempts': 0}, 'modelDetails': {'modelArn': 'arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-5-sonnet-20240620-v1:0', 'modelId': 'anthropic.claude-3-5-sonnet-20240620-v1:0', 'modelName': 'Claude 3.5 Sonnet', 'providerName': 'Anthropic', 'inputModalities': ['TEXT', 'IMAGE'], 'outputModalities': ['TEXT'], 'responseStreamingSupported': True, 'customizationsSupported': [], 'inferenceTypesSupported': ['ON_DEMAND'], 'modelLifecycle': {'status': 'ACTIVE'}}}