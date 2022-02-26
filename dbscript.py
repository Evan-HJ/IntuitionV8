'''
NOTE: MongoDB stores:

Tutees: name, usrname, age, school, pwd (Hash), meetings (List of meeting ids), iconID
Tutors: name, usrname, age, school, pwd (Hash), meetings (List of meeting ids), subjects (List), comments (List), iconID
Meeting: tuteeID (List), tutorID, start, end, subject, level, link
'''

from flask_pymongo import PyMongo
from flask import Flask
import json
import secrets, hashlib
from pymongo.errors import *
from helper import *
from random import randint
import zoom
from bson.objectid import ObjectId
from flask import jsonify

app = Flask(__name__);

app.config['MONGO_URI'] = "mongodb+srv://"+ secrets.username +":"+ secrets.password + "@" + secrets.host + "/" + secrets.dbname + "?retryWrites=true&w=majority"
print("mongodb+srv://"+ secrets.username +":"+ secrets.password + "@" + secrets.host + "/" + secrets.dbname + "?retryWrites=true&w=majority")
app.secret_key = 'secretkey'
mongo = PyMongo(app)

db = mongo.db

tuteeDB = db.tutee
tutorDB = db.tutor
meetingDB = db.meeting

all_subjects = ['english','math','science','chinese'];
def reset_db():
    tuteeDB.drop();
    tutorDB.drop();
    meetingDB.drop();
    tuteeDB.create_index('usrname', unique = True)
    tutorDB.create_index('usrname', unique = True)

if __name__ == '__main__': reset_db()

#CODE STARTS HERE

def tuteeLogin(username, pwd):
    # Returns ID of user, or None if wrong pwd
    hash_pwd = hash(pwd)

    result = tuteeDB.find_one({
        'usrname': username,
        'pwd': hash_pwd
    })

    if not result: return None
    return result['_id']

def tutorLogin(username,pwd):
    # Returns ID of user, or None if wrong pwd
    hash_pwd = hash(pwd)

    result = tutorDB.find_one({
        'usrname': username,
        'pwd': hash_pwd
    })

    if result is None: return None
    return result['_id']

def tuteeAdd(name,username,age,school,pwd): #Returns if add was a success
    new_doc = {
        'name': name,
        'usrname': username,
        'age': age,
        'school': school,
        'pwd': hash(pwd),
        'meetings': [],
        'iconID': 1
    }

    try:
        tuteeDB.insert_one(new_doc)
    except DuplicateKeyError:
        return None
    return new_doc

def tutorAdd(name,username,age,school,pwd):
    new_doc = {
        'name': name,
        'usrname': username,
        'pwd': hash(pwd),
        'age': int(age),
        'school': school,
        'meetings': [],
        'comments': [],
        'iconID': 1
    }
    try:
        tutorDB.insert_one(new_doc)
    except DuplicateKeyError:
        return None
    return new_doc

def getTutorDoc(fields): #needed_fields is a list
    res = tutorDB.find_one(fields)
    res.pop('pwd',None)
    return res

def getTuteeDoc(fields):
    res = tuteeDB.find_one(fields)
    res.pop('pwd',None)
    return res

def addMeeting(title, subject, level, start, end, date, tutorID):
    link = zoom.create_meeting(title)
    new_doc = {
        'title': title,
        'subject': subject,
        'level': level,
        'start': start,
        'end': end,
        'date': date,
        'tutorID': ObjID(tutorID),
        'tuteeID': [],
        'link': link
    }
    insertOneObj = meetingDB.insert_one(new_doc)

    tutorDB.update_one({'_id': ObjID(tutorID)}, {
        '$push': {
            'meetings': insertOneObj.inserted_id
        }
    })

    return new_doc

def getMeeting(fields):
    return meetingDB.find_one(fields)

def regForMeeting(tuteeID, meetingID):
    tuteeDB.update_one({'_id': ObjID(tuteeID)},{
        '$push':{
            'meetings': ObjID(meetingID)
        }
    })
    meetingDB.update_one({'_id': ObjID(meetingID)},{
        '$push':{
            'tuteeID': ObjID(tuteeID)
        }
    })

def searchMeeting(fields, upper = {}, lower = {}):
    fields.update({
        key : {'$gte' : value} for key,value in lower.items()
    })
    fields.update({
        key : {'$lte' : value} for key,value in upper.items()
    })
    print("FIELDS: ", fields)
    res = [i for i in meetingDB.find(fields)]

    return res
