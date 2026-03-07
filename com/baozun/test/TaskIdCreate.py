import time
import random
import string
import secrets
import uuid
import shortuuid


def getByTimeNs(length=10):
    taskId = str(time.time_ns())
    return taskId[:length]

def generate_random_string(length=10):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def getByUUid():
    return str(uuid.uuid1())

def getByShortUUid(length = 10):
    return str(shortuuid.ShortUUID().random(length))



print(getByTimeNs())
print(generate_random_string())
print(getByUUid().replace('-', ''))
print(getByUUid())
print(getByShortUUid())



