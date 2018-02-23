import redis
from flask_script import Server, Manager
from rq import Connection, Worker
from webapp import app
from webapp.apis.upload import get_redis_connection

manager = Manager(app)

@manager.command
def runworker():
    with Connection(get_redis_connection()):
        worker = Worker(['webapp'])
        worker.work()

if __name__ == '__main__':
    manager.run()
