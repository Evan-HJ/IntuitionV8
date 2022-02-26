import hashlib
from datetime import datetime
from bson.objectid import ObjectId

def hash(string):
    return hashlib.md5(string.encode()).hexdigest()

def strptime(day, time):
    return datetime.strptime(day + ' ' + time, '%Y-%m-%d %H:%M')

def ObjID(id):
    if type(id) == ObjectId: return id
    return ObjectId(id)
