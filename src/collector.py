import boto3
import logging
import json
import csv

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    logger.info(event)

    # Retrieve data from S3 via EventBridge Pipes notification
    # Logically it should be possible to transform the message passed into the
    # statemachine to remove some of the processing in this Lambda.

    body = json.loads(event[0]['body'])
    bucket = body['Records'][0]['s3']['bucket']['name']
    key = body['Records'][0]['s3']['object']['key']

    s3 = boto3.client('s3')
    data = s3.get_object(Bucket=bucket, Key=key)
    content = data['Body'].read().decode('UTF-8').split('\n')

    # Convert CSV data into JSON. First row is header, which defines JSON attribute keys
    payload = list(csv.DictReader(content))

    return {
        "filename": key,
        "payload": payload
    }
