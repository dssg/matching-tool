import redis
from flask_script import Server, Manager
from rq import Connection, Worker
from webapp import app
from webapp.apis.upload import redis_connection

manager = Manager(app)

@manager.command
def runworker():
    with Connection(redis_connection):
        worker = Worker(['webapp'])
        worker.work()

if __name__ == '__main__':
    manager.run()
