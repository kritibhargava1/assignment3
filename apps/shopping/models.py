"""
This file defines the database models
"""


from pydal import Field
from .common import db, auth
from pydal.validators import IS_NOT_EMPTY


# Define a helper function to get the current user's ID
def get_user_id():
    return auth.current_user.get('id') if auth.current_user else None

# Define the shopping list table
db.define_table(
    'shopping_list',
    Field('item_name', 'string', requires=IS_NOT_EMPTY()),
    Field('purchased', 'boolean', default=False),
    Field('user_id', 'reference auth_user', default=get_user_id),  # Ensure get_user_id is correctly defined
)
db.commit()

