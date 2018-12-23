from flask import Blueprint, g, request
from bson.json_util import dumps, loads
from helpers.helpers import getPersonsCount
from helpers.db_helper import fetchPersons
import json

#create adult_data Bluprint 
adult_data = Blueprint('adult_data', __name__)

# /getCount route for getting the total counts for generating bar graph and pie chart on frontend
# used redis to cache the result once and retrieve it again and again as response is not changing
@adult_data.route('/getCount', methods=['GET'])
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

# /persons route for getting the adult_data rows with pagination and filtering support
# caching the first request for page 1 without any filters, as it remains unchanged 
# retrieve it from cache and respon with it for the first call from frontend
@adult_data.route('/persons', methods=['GET'])
def getPersons():
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

# handles all exception on both the routes and returns an internal server error message
@adult_data.app_errorhandler(Exception)
def handle_error(error):
    message = 'internal server error'
    status_code = 500
    success = False
    response = {
        'success': success,
        'error': {
            'type': 'internal error',
            'message': message
        }
    }
    return dumps(response), status_code