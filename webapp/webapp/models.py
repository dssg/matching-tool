from webapp.database import Base
from flask_security import UserMixin, RoleMixin
from sqlalchemy.orm import relationship, backref
from sqlalchemy import BigInteger, Boolean, DateTime, Column, Interval, Integer, \
                       String, ForeignKey


class RolesUsers(Base):
    __tablename__ = 'roles_users'
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), ForeignKey('user.id'))
    role_id = Column('role_id', Integer(), ForeignKey('role.id'))


class Role(Base, RoleMixin):
    __tablename__ = 'role'
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))


class User(Base, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    username = Column(String(255))
    password = Column(String(255))
    last_login_at = Column(DateTime())
    current_login_at = Column(DateTime())
    last_login_ip = Column(String(100))
    current_login_ip = Column(String(100))
    login_count = Column(Integer)
    active = Column(Boolean())
    confirmed_at = Column(DateTime())
    roles = relationship('Role', secondary='roles_users',
                         backref=backref('users', lazy='dynamic'))


class Upload(Base):
    __tablename__ = 'upload_log'
    id = Column(String(255), primary_key=True)
    jurisdiction_slug = Column(String(255))
    event_type_slug = Column(String(255))
    user_id = Column(Integer, ForeignKey('user.id'))
    given_filename = Column(String(255))
    upload_start_time = Column(DateTime())
    upload_complete_time = Column(DateTime())
    upload_status = Column(Boolean())
    validate_start_time = Column(DateTime())
    validate_complete_time = Column(DateTime())
    validate_status = Column(Boolean())
    num_rows = Column(Integer)
    file_size = Column(BigInteger)
    file_hash = Column(String(255))
    s3_upload_path = Column(String(255))


class MergeLog(Base):
    __tablename__ = 'merge_log'
    id = Column(Integer, primary_key=True)
    upload_id = Column(String(255), ForeignKey('upload_log.id'))
    new_unique_rows = Column(Integer)
    total_unique_rows = Column(Integer)
    merge_start_timestamp = Column(DateTime())
    merge_complete_timestamp = Column(DateTime())

class MatchLog(Base):
    __tablename__ = 'match_log'
    id = Column(String(255), primary_key=True)
    upload_id = Column(String(255), ForeignKey('upload_log.id'))
    match_start_timestamp = Column(DateTime())
    match_complete_timestamp = Column(DateTime())
    match_status = Column(Boolean())
    runtime = Column(Interval())
