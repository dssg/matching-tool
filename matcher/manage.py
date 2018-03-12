import redis
from redis import Redis
from rq import Connection, Worker

redis_connection = Redis(host='redis', port=6379)

def runworker():
    with Connection(redis_connection):
        worker = Worker(['default'])
        worker.work()

if __name__ == '__main__':
    runworker()
