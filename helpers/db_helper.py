from pymongo import MongoClient
import redis
import math

# helper function to connect with mongodb and return connection object
def connect_db(app):
    return MongoClient(app.config['DB_HOST'], app.config['DB_PORT'])

# helper function to connect with redis and return connection object
def connect_redis(app):
    return redis.StrictRedis(host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'], db=0)

# helper function to fetched persons from db with filtering and pagination parameters
# also generates the pagination parameters for response
def fetchPersons(persons, searchFilter, page, skip, limit):
    res = {}
    res["data"] = list(persons.find(searchFilter, None, skip, limit))
    res["totalPages"] = math.ceil(persons.count_documents(searchFilter)/50)
    res['nextPage'] =  (page + 1) if(page + 1 <= res["totalPages"]) else -1
    res['previousPage'] = (page - 1) if(page - 1 > 0) else -1
    if(res["totalPages"] == 0):
        res["totalPages"] = -1
    return res