# Search for tags "<...>" and replace them with your own values also rename this file to "local_settings.py"
IP = "<serverIP>"  # e.g.: 127.0.0.1
PORT = "<serverPort>"  # e.g.: 8000
PROTOCOL = "http"  #  http/https
DOMAIN = f"{PROTOCOL}://{IP}:{PORT}"

AUTH_USER_MODEL = 'authtools.User'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = '<server email addres>'
EMAIL_HOST_PASSWORD = '<your 16 digit password generated in google account in the App Passwords section>'
EMAIL_USE_TLS = True

DEFAULT_FROM_EMAIL = '<Name of the App>'  # e.g.: SDG App

SERVICE_JSON = '<path to your firebase service json>.json'  # for example view .gitignore file

NOTIFICATION_TOKEN_FILE = "tokens.json"

import firebase_admin
# put your own project name below (ofcourse after you create one)
access_token_object = firebase_admin.initialize_app().credential.get_access_token()
NOTIFICATION_REQUEST_URL = "https://fcm.googleapis.com/v1/projects/<project name in firebase>/messages:send"
NOTIFICATION_REQUEST_HEADER = {
    'Authorization': 'Bearer ' + access_token_object.access_token,
    'Content-Type': 'application/json; UTF-8',
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '',  # name of your database
        'USER': '',  # username of your database, probably "postgres"
        'PASSWORD': '',  # password of your database
        'HOST': '127.0.0.1', # probably won't need to change this
        'PORT': '5432',  # won't need to change this either
    }
}