import boto3
import json
import os

def handler(event, context):    
    client = boto3.client('stepfunctions')
    n = int(event['queryStringParameters']['n'])
    response = client.start_execution(
        stateMachineArn=os.environ['STATE_MACHINE_ARN'],
        input=json.dumps({"input": str(n), "function": "fibonacci"})
    )
    return {
        'statusCode': 200,
        'body': "OK"
    }

