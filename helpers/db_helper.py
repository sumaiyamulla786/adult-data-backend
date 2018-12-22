from pymongo import MongoClient
import redis

def connect_db(app):
    return MongoClient(app.config['DB_HOST'], app.config['DB_PORT'])

def connect_redis(app):
    return redis.StrictRedis(host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'], db=0)

def fetchPersons(persons, searchFilter, page, skip, limit):
    res = {}
    res["data"] = list(persons.find(searchFilter, None, skip, limit))
    res["totalPages"] = int(persons.count_documents(searchFilter)/50)
    res['nextPage'] =  (int(page) + 1) if(int(page) + 1 <= res["totalPages"]) else -1
    res['previousPage'] = (int(page) - 1) if(int(page) - 1 > 0) else -1
    return res