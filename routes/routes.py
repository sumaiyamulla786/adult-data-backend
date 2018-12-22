from flask import Blueprint, g, request
from bson.json_util import dumps, loads
from helpers.helpers import getPersonsCount
from helpers.db_helper import fetchPersons
import json

getCount = Blueprint('getCount', __name__)

@getCount.route('/getCount', methods=['GET'])
def show():
    res = g.redis_db.get('getCount')
    if(not res):
        db = g.db.adultDataDB
        persons = db.person
        res = getPersonsCount(persons)
        g.redis_db.set('getCount', json.dumps(res))
    else:
        res = json.loads(res)
    return dumps(res)

getPersons = Blueprint('getPersons', __name__)

@getPersons.route('/persons', methods=['GET'])
def show():
    db = g.db.adultDataDB
    persons = db.person
    page = request.args.get('page')
    if (not page):
        page = '1'
    page = int(page)
    sex = request.args.get('sex')
    race = request.args.get('race')
    relationship = request.args.get('relationship')
    limit = 50
    skip = (page - 1) * limit
    searchFilter = {}
    if(sex or race or relationship):
        if(sex):
            searchFilter["sex"] = sex
        if(race):
            searchFilter["race"] = race
        if(relationship):
            searchFilter["relationship"] = relationship
    if(page == '1' and not sex and not race and not relationship):
        res = g.redis_db.get('initialPage')
        if(not res):
            res = fetchPersons(persons, searchFilter, page, skip, limit)
            g.redis_db.set('initialPage', dumps(res))
        else:
            res = loads(res)
        return dumps(res)
    else:
        res = fetchPersons(persons, searchFilter, page, skip, limit)
        return dumps(res)