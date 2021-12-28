import os
import pytz
from datetime import datetime
from google.cloud import pubsub_v1


credentials_path = 'pubsub-onboardtest-key.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

publisher = pubsub_v1.PublisherClient()
topic_path = 'projects/tall-ridge/topics/onboardtest'

tz = pytz.timezone('US/Central')

def publish_msg():
    data = 'the backfill has begun at ' + str(datetime.now(tz))
    data = data.encode('utf-8')
    attributes = {
        'targetclientname':'bionova',
        'backfillstartdate':'2021-01-01',
        'marketplacetypes':'AMZN,WMT'
    }
    

    future = publisher.publish(topic_path, data, **attributes)
    print(f'published message id {future.result()}')


publish_msg()