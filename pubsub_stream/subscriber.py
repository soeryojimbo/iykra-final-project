from curses.ascii import ACK
import os
from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError

credentials_path = '/home/jimbo/.google/credentials/google_credentials.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

timeout = 5.0

subscriber = pubsub_v1.SubscriberClient()
subsciption_path = 'projects/suryo-df8/subscriptions/final-project-sub'

def callback(message):
    print(f'Received message: {message}')
    print(f'data: {message.data}')
    message.ack()

streaming_pull_future = subscriber.subscribe(subsciption_path, callback=callback)
print(f'Listening for messages on {subsciption_path}')

with subscriber:                                                # wrap subscriber in a 'with' block to automate response
    try:
        # streaming_pull_future.result(timeout=timeout)
        streaming_pull_future.result()                          # going without timeout will wait and block
    except TimeoutError:
        streaming_pull_future.cancel()                          # trigger the shutdown
        streaming_pull_future.result()                          # block until the shutdown is complete