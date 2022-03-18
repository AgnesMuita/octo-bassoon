# from helpdesk import models
from students import models
import time
import string
import random
import datetime


def getTimestamp(datetime_string=None, datetime_format=None):
    if not datetime_string:
        return int(time.time())
    else:
        datetime_format = datetime_format if datetime_format else "%Y-%m-%d %H:%M:%S"
        return time.mktime(datetime.datetime.strptime(datetime_string, datetime_format).timetuple())


def generateToken(size=10, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))
