import redis
pool=redis.ConnectionPool(host='127.0.0.1',port=6379,db=0)
cache = redis.StrictRedis(connection_pool=pool)
print("链接成功")