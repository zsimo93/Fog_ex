import redis


class Database():
    db = redis.StrictRedis(host='localhost', port=6379, db=0)
