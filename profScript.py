import pymongo
from pymongo import MongoClient

import psycopg2
from psycopg2.extras import RealDictCursor

import json
from datetime import time, date, datetime

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, (datetime, time)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))


CONNECTION_STRING = "mongodb://127.0.0.1:27017/rocket"
client = MongoClient(CONNECTION_STRING)
rdb = client['hurricane']

cnx = psycopg2.connect(user="dbuser", database="hurricane", host="localhost", port="5432", password="12345678")
cursor = cnx.cursor(cursor_factory=RealDictCursor)

scoll = rdb['Hurricane']
cursor.execute("select * from hurricane")
results = cursor.fetchall()
print(len(results))
jout = json.dumps(results, default=json_serial)
aaa = json.loads(jout)
print(len(aaa))
scoll.insert_many(aaa)

scoll = rdb['Observation']
cursor.execute("select * from observation")
results = cursor.fetchall()
print(len(results))
jout = json.dumps(results, default=json_serial)
aaa = json.loads(jout)
print(len(aaa))
scoll.insert_many(aaa)
