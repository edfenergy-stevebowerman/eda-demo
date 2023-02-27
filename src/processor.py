import os
import logging
import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    logger.info(event)

    key = os.environ['API_KEY']

    response = requests.get('http://api.positionstack.com/v1/forward?access_key=' +
                            key + '&query=' + event['city'] + ',' + event['country'])
    geo = response.json()

    event['latitude'] = geo['data'][0]['latitude']
    event['longitude'] = geo['data'][0]['longitude']

    return event
