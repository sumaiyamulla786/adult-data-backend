from flask import Flask, g, request
from pymongo import MongoClient
from helpers.helpers import getPersonsCount
from bson.json_util import dumps, loads
from flask_cors import CORS
import redis
import json

app = Flask(__name__)
CORS(app)

def connect_db():
    return MongoClient("localhost", 27017)

def connect_redis():
    return redis.StrictRedis(host="localhost", port=6379, db=0)

@app.before_request
def before_request():
    g.redis_db = connect_redis()
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g,'db'):
        g.db.close()

@app.route('/getCount', methods=['GET'])
def getCount():
    res = g.redis_db.get('getCount')
    if(not res):
        db = g.db.adultDataDB
        persons = db.person
        res = getPersonsCount(persons)
        g.redis_db.set('getCount', json.dumps(res))
    else:
        res = json.loads(res)
    return dumps(res)

@app.route('/persons', methods=['GET'])
def getPersons():
    db = g.db.adultDataDB
    persons = db.person
    page = request.args.get('page')
    if (not page):
        page = '1'
    sex = request.args.get('sex')
    race = request.args.get('race')
    relationship = request.args.get('relationship')
    limit = 50
    skip = int(page) * limit
    filter = {}
    if(sex or race or relationship):
        if(sex):
            filter["sex"] = sex
        if(race):
            filter["race"] = race
        if(relationship):
            filter["relationship"] = relationship
    if(page == '1' and not sex and not race and not relationship):
        res = g.redis_db.get('initialPage')
        if(not res):
            res = fetchPersons(persons, filter, page, skip, limit)
            g.redis_db.set('initialPage', dumps(res))
        else:
            res = loads(res)
        return dumps(res)
    else:
        res = fetchPersons(persons, filter, page, skip, limit)
        return dumps(res)
    
def fetchPersons(persons, filter, page, skip, limit):
    res = {}
    res["data"] = list(persons.find(filter, None, skip, limit))
    res["totalPages"] = int(persons.count_documents(filter)/50)
    res['nextPage'] =  (int(page) + 1) if(int(page) + 1 <= res["totalPages"]) else -1
    res['previousPage'] = (int(page) - 1) if(int(page) - 1 > 0) else -1
    return res

if __name__ == "__main__":
    app.run(debug=True)
    