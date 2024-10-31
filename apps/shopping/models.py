"""
This file defines the database models
"""

import datetime
from .common import db, Field, auth
from pydal.validators import IS_NOT_EMPTY

def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None

def get_time():
    return datetime.datetime.utcnow()


db.define_table(
    'shopping_list',
    Field('user_id', 'reference auth_user', readable=False, writable=False),
    Field('item_name', 'string', requires=IS_NOT_EMPTY()),
    Field('purchased', 'boolean', default=False),
)


db.commit()
