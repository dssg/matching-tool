import redis
from flask_script import Server, Manager
from rq import Connection, Worker
from matcher.api import app, redis_connection

manager = Manager(app)

@manager.command
def runworker():
    with Connection(redis_connection):
        worker = Worker(['default'])
        worker.work()

if __name__ == '__main__':
    manager.run()
