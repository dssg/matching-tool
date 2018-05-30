from flask import render_template
from flask_security import Security, login_required, \
     SQLAlchemySessionUserDatastore
from webapp import app
from webapp.config import config as app_config
from webapp.database import db_session, engine
from webapp.models import User, Role
from webapp.apis.upload import upload_api
from webapp.apis.chart import chart_api
from webapp.apis.jobs import jobs_api
from webapp.utils import generate_master_table_name
import click
import s3fs

# Setup Flask-Security
user_datastore = SQLAlchemySessionUserDatastore(db_session,
                                                User, Role)
security = Security(app, user_datastore)
app.register_blueprint(upload_api)
app.register_blueprint(chart_api)
app.register_blueprint(jobs_api)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
@login_required
def home(path):
    return render_template('index.html')


@app.route('/health-check')
def health_check():
    return 'OK!'


@app.teardown_appcontext
def shutdown_session(exception=None):
    print('removing session!')
    db_session.remove()


@app.cli.command()
@click.argument('jurisdiction')
@click.argument('event_type')
def expunge(jurisdiction, event_type):
    """Expunges all data for a given jurisdiction and event type"""
    s3 = s3fs.S3FileSystem()

    base_path = app_config['base_path'].format(jurisdiction=jurisdiction, event_type=event_type)
    match_cache_path = app_config['match_cache_path'].format(jurisdiction=jurisdiction)
    master_table = generate_master_table_name(jurisdiction, event_type)

    msg = 'Expunge all data for jurisdiction {} and event_type {}?'.format(jurisdiction, event_type)
    msg += '\n\ns3 paths (recursive!): {}, {}'.format(base_path, match_cache_path)
    msg += '\n\ndatabase tables: {}'.format(master_table)
    msg += '\n\nYou should not do this while the system is validating or matching.'
    msg += '\n\nRemove all this?'
    shall = input("%s (y/N) " % msg).lower() == 'y'
    click.echo(shall)
    if not shall:
        click.echo("Expunge aborted")

    click.echo("Removing base path " + base_path)
    s3.rm(base_path, recursive=True)
    click.echo("Removing match cache path" + match_cache_path)
    s3.rm(match_cache_path, recursive=True)
    click.echo("Truncating master database table " + master_table)
    engine.execute('truncate {}'.format(master_table))
