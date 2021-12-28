import os
import pytz
from datetime import datetime
from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError

credentials_path = 'pubsub-onboardtest-key.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

tz = pytz.timezone('US/Central')

timeout = 5.0

subscriber = pubsub_v1.SubscriberClient()
subscription_path = 'projects/tall-ridge/subscriptions/onboardtest-sub'

def callback(message):
    print(f'recieved message: {message}')
    print(f'data: {message.data}')
    #this acknowledgement will tell pubsub to delete the message, otherwise, retain for 7 days
    if message.attributes:
        print("Attributes:")
        for key in message.attributes:
            value = message.attributes.get(key)
            print(f"{key}: {value}")
            
    message.ack()

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f'listening for msgs on {subscription_path}')
    
with subscriber:
    try:
        streaming_pull_future.result()
    except TimeoutError:
        streaming_pull_future.cancel()
        streaming_pull_future.result()