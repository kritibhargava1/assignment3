"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

from py4web import action, request, abort, URL
from .common import db, session, auth
from py4web.utils.url_signer import URLSigner

# Initialize URL signer for secure URLs
url_signer = URLSigner(session)

@action('index')
@action.uses('index.html', db, auth.user)
def index():
    # Render the index page with URLs for each action
    return dict(
        load_data_url=URL('load_items', signer=url_signer),
        add_item_url=URL('add_item', signer=url_signer),
        mark_purchased_url=URL('mark_purchased', signer=url_signer),
        delete_item_url=URL('delete_item', signer=url_signer),
    )

@action('load_items')
@action.uses(db, auth.user)
def load_items():
    # Retrieve items for the logged-in user, sorted by purchased status
    items = db(db.shopping_list.user_id == auth.user_id).select(orderby=~db.shopping_list.purchased)
    return dict(items=[item.as_dict() for item in items])

@action('add_item', method=["POST"])
@action.uses(db, auth.user)
def add_item():
    item_name = request.json.get('item_name')
    if not item_name:
        abort(400, "Item name is required")
    # Insert a new item for the current user
    db.shopping_list.insert(user_id=auth.user_id, item_name=item_name, purchased=False)
    return dict(success=True)

@action('mark_purchased/<item_id>', method=["POST"])
@action.uses(db, auth.user)
def mark_purchased(item_id):
    # Retrieve the item, ensuring it belongs to the logged-in user
    item = db.shopping_list(item_id) or abort(404)
    if item.user_id != auth.user_id:
        abort(403)
    # Toggle the purchased status
    item.update_record(purchased=not item.purchased)
    return dict(success=True)

@action('delete_item/<item_id>', method=["POST"])
@action.uses(db, auth.user)
def delete_item(item_id):
    # Retrieve the item, ensuring it belongs to the logged-in user
    item = db.shopping_list(item_id) or abort(404)
    if item.user_id != auth.user_id:
        abort(403)
    # Delete the item
    item.delete_record()
    return dict(success=True)
