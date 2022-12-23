import json
import requests
import firebase_admin
# from niser_app.local_settings import *
import time


NOTIFICATION_TOKEN_FILE = "../tokens.json"


def send_notification(message_title, message_desc, tokens, image = None):
    access_token_object = firebase_admin.initialize_app().credential.get_access_token()
    # print(credential)

    url = "https://fcm.googleapis.com/v1/projects/appnotifications-28b81/messages:send"

    headers = {
        'Authorization': 'Bearer ' + access_token_object.access_token,
        'Content-Type': 'application/json; UTF-8',
    }

    # del access_token_object
    
    for token in tokens:
    
        payload = {
            "message": {
                "token": token,
                "notification": {
                    "body": message_desc,
                    "title": message_title,
                    "image": image,
                }
            }
        }

        result = requests.post(url, data=json.dumps(payload), headers=headers)
        print(result.json())


if __name__ == "__main__":
    tokens = [
        "dazG5ZCcRw68ulOgg_rdtO:APA91bGVvovZFUu1PCLAbBUHvpQ331sCgD8drTA5IrDbSvjHyCujmZD4vDpkZbnLMKkAX73rrGa1QDCn4DDSr_mu4JZGftx7x2lCdpxfuhWOwgYtj-EvXSyCkyalhJ3AwfR8DpYx_uM0",
        "fWJGY-gBQMObH8K-Gq4zhh:APA91bGQVuronVl1Nk2VGiNXc8NdZjocyJB_HrJMf4SzUJFh4ePOy6myhvo_SKOEUh5bE1FRdTdIqQEDQ8MoS197r_CCkcrWwDFofSJl3S9z23DGIuYUXcpJGE9p8lCckF5RUm7hgseq"
    ]

    t0 = time.time()

    to = tokens
    send_notification("Hello", "This is a test notification", to)
    print(f"Time taken: {time.time() - t0} seconds")

