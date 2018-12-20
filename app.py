from flask import Flask, g, jsonify, request
from pymongo import MongoClient
from helpers.helpers import getPersonsCount
from bson.json_util import dumps
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def connect_db():
    return MongoClient("localhost", 27017)

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g,'db'):
        g.db.close()

@app.route('/getCount', methods=['GET'])
def getCount():
    db = g.db.adultDataDB
    persons = db.person
    res = getPersonsCount(persons)
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
    res = {}
    res["data"] = list(persons.find(filter, None, skip, limit))
    res["totalPages"] = int(persons.count_documents(filter)/50)
    res['nextPage'] =  (int(page) + 1) if(int(page) + 1 <= res["totalPages"]) else -1
    res['previousPage'] = (int(page) - 1) if(int(page) - 1 > 0) else -1
    return dumps(res)

if __name__ == "__main__":
    app.run(debug=True)
    