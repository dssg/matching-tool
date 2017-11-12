from webapp.app import app, security
from webapp.models import User, Role
from webapp.database import Base, db_session
from webapp.utils import create_statement_from_goodtables_schema, load_schema_file
from sqlalchemy import create_engine
import contextlib
import testing.postgresql

from flask_security import SQLAlchemySessionUserDatastore
from flask_security.utils import encrypt_password


@contextlib.contextmanager
def rig_test_client():
    with testing.postgresql.Postgresql() as postgresql:
        dburl = postgresql.url()
        engine = create_engine(dburl)
        Base.metadata.create_all(engine)
        db_session.bind = engine
        user_datastore = SQLAlchemySessionUserDatastore(db_session,
                                                        User, Role)
        app.config['SQLALCHEMY_DATABASE_URI'] = dburl
        app.config['WTF_CSRF_ENABLED'] = False
        init_app_with_options(app, user_datastore)
        yield app.test_client()


def authenticate(
        client,
        email="boone_hmis@example.com",
        password="password",
        endpoint=None,
        **kwargs):
    data = dict(email=email, password=password, remember='y')
    return client.post(endpoint or '/login', data=data, **kwargs)


def logout(client, endpoint=None, **kwargs):
    return client.get(endpoint or '/logout', **kwargs)


def create_roles(ds):
    for role in ('boone_hmis', 'boone_jail', 'clark_hmis', 'clark_jail'):
        ds.create_role(name=role)
    ds.commit()


def create_users(ds):
    users = [
        ('boone_hmis@example.com', 'boone hmis', 'password', ['boone_hmis'], True),
        ('boone_jail@example.com', 'boone jail', 'password', ['boone_jail'], True),
        ('clark_hmis@example.com', 'clark hmis', 'password', ['clark_hmis'], True),
        ('clark_jail@example.com', 'clark jail', 'password', ['clark_jail'], True),
    ]
    count = len(users)

    for u in users[:count]:
        pw = u[2]
        if pw is not None:
            pw = encrypt_password(pw)
        roles = [ds.find_or_create_role(rn) for rn in u[3]]
        ds.commit()
        user = ds.create_user(
            email=u[0],
            username=u[1],
            password=pw,
            active=u[4])
        ds.commit()
        for role in roles:
            ds.add_role_to_user(user, role)
        ds.commit()


def populate_data(app, user_datastore):
    with app.app_context():
        create_roles(user_datastore)
        create_users(user_datastore)


def init_app_with_options(app, datastore, **options):
    security.datastore = datastore
    populate_data(app, datastore)

def create_and_populate_raw_table(raw_table, data, db_engine):
    schema = load_schema_file('test')
    create = create_statement_from_goodtables_schema(schema, raw_table)
    db_engine.execute(create)
    for row in data:
        db_engine.execute('insert into "{}" values (%s, %s, %s, %s, %s)'.format(raw_table), *row)
    db_engine.execute('insert into upload_log (id, jurisdiction_slug, service_provider_slug) values (%s, %s, %s)', raw_table, 'test', 'test')
