from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask import flash
from flask_uploads import UploadSet, configure_uploads, IMAGES
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Category, CategoryItem, Base, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
import os

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog App"

# Instantiate the uploads object
photos = UploadSet('photos', IMAGES)

# Providing upload destination
app.config['UPLOADED_PHOTOS_DEST'] = 'static/'
configure_uploads(app, photos)

# Connect to Database and create database session
engine = create_engine('sqlite:///items.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# Show login page
@app.route('/login')
def login():
    # Create anti-forgery state token
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


# GOOGLE Login
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data
    print(code)
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    return render_template('hello.html', username=login_session['username'],
                           picture=login_session['picture'],
                           userID=login_session['user_id'])


@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Facebook Login
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    # Compare two state codes
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = request.data

    # Exchange client token for a long-lived server-side token
    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = 'https://graph.facebook.com/v2.8/me?access_token=%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # Get user picture
    url = 'https://graph.facebook.com/v2.8/me/picture?access_token=%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    print user_id
    if not user_id:
        user_id = createUser(login_session)
        print "created user_id"
        print user_id

    login_session['user_id'] = user_id

    return render_template('hello.html', username=login_session['username'], picture=login_session['picture'], userID=login_session['user_id'])
    flash("Now logged in as {}".format(login_session['username']))


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


# JSON APIs to view Restaurant Information

@app.route('/categories/<category>/JSON')
def CategoryJSON(category):
    catalog = session.query(Category).filter_by(name=category).one()
    items = session.query(CategoryItem).filter_by(
        category_id=catalog.id).all()
    return jsonify(CatalogItems=[i.serialize for i in items])


@app.route('/categories/<category>/<int:item_id>/JSON')
def CategoryItemJSON(category, item_id):
    category = session.query(Category).filter_by(name=category).one()
    Catalog_Item = session.query(CategoryItem).filter_by(id=item_id).one()
    return jsonify(Catalog_Item=Catalog_Item.serialize)


@app.route('/categories/JSON')
def CategoriesJSON():
    categories = session.query(Category).all()
    return jsonify(Categories=[r.serialize for r in categories])


# Show all categories
@app.route('/')
@app.route('/categories')
def index():
    categories = session.query(Category).order_by(asc(Category.name))
    return render_template('index.html', categories=categories)


# Show a single category with list of items
@app.route('/categories/<categoryName>')
def showCategory(categoryName):
    category = session.query(Category).filter_by(name=categoryName).one()
    category_items = session.query(CategoryItem).filter_by(
        category_id=category.id).all()
    return render_template('category.html', category=category, category_items=category_items)


# Show a single Item
@app.route('/categories/<category>/<int:item_id>')
def showItem(category, item_id):
    category = session.query(Category).filter_by(name=category).one()
    item = session.query(CategoryItem).filter_by(id=item_id).one()
    return render_template('category_item.html', category=category, category_item=item)


# Add a new category
@app.route('/categories/new', methods=['GET', 'POST'])
def newCategory():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        newCategory = Category(
            name=request.form['name'],
            user_id=login_session['user_id'],
            picture=filename)
        session.add(newCategory)
        flash('New Category %s Successfully Created' % newCategory.name)
        session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('newCategory.html')


# Delete a category
@app.route('/categories/<category>/delete', methods=['GET', 'POST'])
def deleteCategory(category):
    categoryToDelete = session.query(Category).filter_by(name=category).one()
    if 'username' not in login_session:
        return redirect('/login')
    if categoryToDelete.user_id != login_session['user_id']:
        return "<script>"
        "function myFunction() {"
        +"alert('You are not authorized to delete this Category. "
        +"Please create your own category in order to delete.');}"
        +"</script>"
        +"<body onload='myFunction()'>"
    if request.method == 'POST':
        session.delete(categoryToDelete)
        # os.remove(os.path.join('/static', categoryToDelete.picture))
        flash('Category: %s Successfully Deleted' % categoryToDelete.name)
        session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('deleteCategory.html', category=category)


# Add a new item
@app.route('/categories/<category>/newitem', methods=['GET', 'POST'])
def addNewItem(category):
    if 'username' not in login_session:
        return redirect('/login')
    categoryForItems = session.query(Category).filter_by(name=category).one()
    if login_session['user_id'] != categoryForItems.user_id:
        return "<script>function myFunction() {"
        +"alert('You are not authorized to add items to this category. "
        +"Please create your own category in order to add items.');}"
        +"</script>"
        +"<body onload='myFunction()'>"
    if request.method == 'POST':
        filename = photos.save(request.files['photo'])

        newItem = CategoryItem(name=request.form['name'],
                               description=request.form['description'],
                               price=request.form['price'],
                               picture=filename,
                               category=categoryForItems)

        session.add(newItem)
        flash('New Item %s Successfully Created' % newItem.name)
        session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('newItem.html', category=category)


# Update a single Item
@app.route('/<category>/<int:item_id>/updateItem', methods=['GET', 'POST'])
def updateItem(category, item_id):
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(name=category).one()
    item = session.query(CategoryItem).filter_by(id=item_id).one()
    if login_session['user_id'] != category.user_id:
        return "<script>function myFunction() {"
        +"alert('You are not authorized to edit items to this category. "
        +"Please create your own category in order to edit items.');}"
        +"</script>"
        +"<body onload='myFunction()'>"
    if request.method == 'POST':
        if request.form['name']:
            item.name = request.form['name']
        if request.form['description']:
            item.description = request.form['description']
        if request.form['price']:
            item.price = request.form['price']
        if 'photo' in request.files:
            filename = photos.save(request.files['photo'])
            item.picture = filename
        session.add(item)
        flash('Category: %s Successfully Updated' % newCategory.name)
        session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('updateItem.html', category=category, item=item)


# Delete a single Item
@app.route('/<category>/<int:item_id>/deleteItem', methods=['GET', 'POST'])
def deleteItem(category, item_id):
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(name=category).one()
    item = session.query(CategoryItem).filter_by(id=item_id).one()
    if login_session['user_id'] != category.user_id:
        return "<script>function myFunction() {"
        +"alert('You are not authorized to delete items to this category. "
        +"Please create your own category in order to delete items.');}"
        +"</script>"
        +"<body onload='myFunction()'>"
    if request.method == 'POST':
        session.delete(item)
        # os.remove(os.path.join('/static', item.picture))
        flash('Item: %s Successfully Deleted' % item.name)
        session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('deleteItem.html', category=category, item=item)


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('index'))
    else:
        flash("You were not logged in")
        return redirect(url_for('index'))


# Show about page
@app.route('/about')
def about():
    return render_template('about.html')


# Show contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.run()
    app.run(host='0.0.0.0', port=3000)
