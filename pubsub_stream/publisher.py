import os
import csv
import json
from time import sleep
import base64
from google.cloud import pubsub_v1

credentials_path = '/home/jimbo/.google/credentials/google_credentials.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

publisher = pubsub_v1.PublisherClient()
topic_path = 'projects/suryo-df8/topics/final-project'

def send_record():
    file = open('fraud_dataset.csv')
    csvreader = csv.reader(file)
    header = next(csvreader)
    for row in csvreader:
        attributes = {"step": (int(row[0])), "type": str(row[1]), "amount": float(row[2]), "nameOrig": str(row[3]), "oldbalanceOrg": float(row[4]), "newbalanceOrig": float(row[5]), "nameDest": str(row[6]), "oldbalanceDest": float(row[7]), "newbalanceDest": float(row[8]), "isFraud": int(row[9]), "isFlaggedFraud": int(row[10])}
        try:
            attributes_dumped = json.dumps(attributes)
            future = publisher.publish(topic_path, attributes_dumped.encode('utf-8'))
        except Exception as e:
            print(f"Exception while producing record value - {attributes}: {e}")
        else:
            print(f"Successfully producing record value - {attributes}")

        print(f'published message id {future.result()}')
        sleep(1)

if __name__ == "__main__":
    send_record()