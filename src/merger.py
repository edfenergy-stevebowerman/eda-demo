import boto3
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    logger.info(event)

    results = event['results']
    filename = event['filename']

    # Convert JSON back into CSV
    data = '"' + '","'.join(results[0].keys()) + '"\n'
    for row in results:
        for col in row.values():
            if isinstance(col, str):
                data += '"' + str(col) + '",'
            else:
                data += str(col) + ','
        data = data[:-1] +'\n'
    data = data[:-1]

    # Write CSV to output bucket.
    s3 = boto3.client('s3')
    output_bucket = os.environ['OUTPUT_BUCKET']
    response = s3.put_object(Body=data, Bucket=output_bucket, Key=filename)

    return response