import random
import hashlib
from datetime import datetime

def genVID(email):  
    """A random string generator which take the email address as an
    input so that even by mistake it doesn't generate the same string
    for two different users. Then it prepares a random salt and hashes
    it with sha3-256. Finally it returns the first 10 and last 10
    characters of the 64 digit long hash.

    Args:
        email (str): The email address of the user

    Returns:
        str: A random string of length 20
    """
    salt = str(random.random()) + str(datetime.now())  # A random string
    m = hashlib.sha3_256((salt + email).encode('utf-8')).hexdigest()
    return m[:10] + m[-10:]

def getIP(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def readableDuration(ts):
    if ts < 60:
        return 'Just Now'
    elif ts < 3600:
        return str(int(ts/60)) + ' minutes ago'
    elif ts < 7200:
        return 'An hour ago'
    elif ts < 86400:
        return str(int(ts/3600)) + ' hours ago'
    elif ts < 86400*2:
        return 'Yesterday'
    elif ts < 86400*7:
        return str(int(ts/86400)) + ' days ago'
    elif ts < 86400*14:
        return 'A week ago'
    elif ts < 86400*30:
        return str(int(ts/(86400*7))) + ' weeks ago'
    elif ts < 86400*60:
        return 'A month ago'
    elif ts < 86400*365:
        return str(int(ts/(86400*30))) + ' months ago'
    elif ts < 86400*365*2:
        return 'An year ago'
    else:
        return str(int(ts/(86400*365))) + ' years ago'
