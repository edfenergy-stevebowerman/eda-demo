import boto3
import logging
import json
import csv

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    logger.info(event)

    bucket = ""
    key = ""

    # If event originates from SQS + AWS Pipes

    if isinstance(event, list):
        if "Records" in event:
            body = json.loads(event[0]['body'])
            bucket = body['Records'][0]['s3']['bucket']['name']
            key = body['Records'][0]['s3']['object']['key']

        else:
            raise Exception("Invalid input message, expecting SQS array")

    # If event originates from EventBridge

    elif set(["source", "detail-type", "detail"]).issubset(event):
        if event["source"] == 'aws.s3' and event['detail-type'] == 'Object Created':
            bucket = event['detail']['bucket']['name']
            key = event['detail']['object']['key']
        else:
            raise Exception(
                "Invalid input message, expecting S3 EventBridge event")

    else:
        raise Exception(
            "Invalid input message, expecting SQS array or EventBridge structure")

    s3 = boto3.client('s3')
    data = s3.get_object(Bucket=bucket, Key=key)
    content = data['Body'].read().decode('UTF-8').split('\n')

    # Convert CSV data into JSON. First row is header, which defines JSON attribute keys
    payload = list(csv.DictReader(content))

    return {
        "filename": key,
        "payload": payload
    }
