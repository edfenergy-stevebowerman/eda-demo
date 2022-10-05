import boto3
import os
import logging
import json
import csv

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    logger.info(event)

    # Retrieve data from S3 via EventBridge notification
    s3 = boto3.client('s3')
    bucket = event['detail']['bucket']['name']
    key = event['detail']['object']['key']
    data = s3.get_object(Bucket=bucket, Key=key)
    content = data['Body'].read().decode('UTF-8').split('\n')

    # Convert CSV data into JSON. First row is header, which defines JSON attribute keys
    payload = list(csv.DictReader(content))
    
    # Submit JSON data into state-machine.
    sfn_client = boto3.client('stepfunctions')

    state_machine_arn = os.environ['STATE_MACHINE']

    response = sfn_client.start_execution(
        stateMachineArn=state_machine_arn,
        input=json.dumps({
            "filename": key,
            "payload": payload
        })
    )

    logger.info(response)