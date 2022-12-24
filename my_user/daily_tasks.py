import json
import requests
from niser_app.local_settings import DEFAULT_FROM_EMAIL, NOTIFICATION_REQUEST_URL, NOTIFICATION_REQUEST_HEADER, NOTIFICATION_TOKEN_FILE
from django.core.mail import EmailMultiAlternatives
from time import sleep
import threading

class My_Send_Email(threading.Thread):
    def __init__(self, to: list, message: str, subject: str, sender: str = DEFAULT_FROM_EMAIL, cc: list = None):
        self.to = to
        self.message = message
        self.subject = subject
        self.sender = sender
        self.cc = cc
        super().__init__()

    def run(self):
        """Send email to all the emails in the list.

        Args:
            to (list): List of email addresses who will receive the email.
            message (str): The message to be sent in HTML format.
            subject (str): The subject of the email.
            sender (str, optional): The sender name of the email. Defaults to DEFAULT_FROM_EMAIL from local settings.
        """
        msg = EmailMultiAlternatives(self.subject, self.message, self.sender, self.to, cc=self.cc)
        msg.send()


class My_Send_Notification(threading.Thread):
    def __init__(self, message: str, title: str, tokens: list = None, image: str = None, check: bool=True):
        self.message = message
        self.title = title
        self.tokens = tokens
        self.image = image
        self.check = check
        super().__init__()
    
    def run(self):
        """Send notification to all tokens. If tokens is not provided, it will read from tokens.json file.
        It takes some time to send these notifications. If check is true, it will check if any new tokens
        are added in the meantime and send them the notification.

        Args:
            message (str): The message to be sent.
            title (str): The title of the notification.
            tokens (list, optional): List of tokens. Defaults to None.
            image (str, optional): The cover image url to be sent in the notification. Defaults to None.
            check (bool, optional): If true, it will check if any new tokens are added in the meantime
                and send them the notification. Defaults to True.
        """
        message = self.message
        title = self.title
        tokens = self.tokens
        image = self.image
        check = self.check
        if not tokens:
            try:
                with open(NOTIFICATION_TOKEN_FILE) as f:
                    tokens = json.load(f)
            except FileNotFoundError:
                tokens = []

        non_working_tokens = []
        for token in tokens:
            if image: payload = {"message": {"token": token, "notification": {"body": message, "title": title, "image": image}}}
            else: payload = {"message": {"token": token, "notification": {"body": message, "title": title}}}
            
            result = requests.post(NOTIFICATION_REQUEST_URL, data=json.dumps(payload), headers=NOTIFICATION_REQUEST_HEADER)
            # {'error': {'code': 404, 'message': 'Requested entity was not found.', 'status': 'NOT_FOUND', 'details': [{'@type': 'type.googleapis.com/google.firebase.fcm.v1.FcmError', 'errorCode': 'UNREGISTERED'}]}}
            # {'name': 'projects/appnotifications-28b81/messages/0:1671819112768910%fbb99cf6fbb99cf6'}
            if result.json().get("error"): non_working_tokens.append(token)
            sleep(2)
        
        
        # my_send_notification is called generally with check = True.
        # It takes some time to send notifications to all tokens. Now,
        # if some new tokens are added in the meantime, it also send
        # them the notification. It also keeps track of the non_working_tokens
        # and while updating the tokens.json file, it removes them.
        if check and not tokens:
            tokens = set(tokens)
            
            with open(NOTIFICATION_TOKEN_FILE) as f:
                updated_tokens = set(json.load(f))
            
            if updated_tokens != tokens:
                with open(NOTIFICATION_TOKEN_FILE, "w") as f:
                    json.dump(list(updated_tokens-set(non_working_tokens)), f)

                My_Send_Notification(
                    message, title,
                    tokens = updated_tokens-tokens,
                    image = image,
                    check = False
                ).start()