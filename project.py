from flask import Flask, render_template, request, url_for, redirect
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

app = Flask(__name__)

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
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)

# Facebook Login
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    #Compare two state codes
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = request.data
    print "access token received {} ".format(access_token)


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
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)

    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as {}".format(login_session['username']))
    return output

@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id,access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"

# Show all categories
@app.route('/')
@app.route('/categories')
def index():
    categories = session.query(Category).order_by(asc(Category.name))
    return render_template('index.html',categories=categories)

# Show a single category with list of items
@app.route('/categories/<categoryName>')
def showCategory(categoryName):
    category = session.query(Category).filter_by(name=categoryName).one()
    category_items = session.query(CategoryItem).filter_by(
    category_id=category.id).all()
    return render_template('category.html',category=category,category_items=category_items)

# Show a single Item
@app.route('/categories/<category>/<int:item_id>')
def showItem(category,item_id):
    category = session.query(Category).filter_by(name=category).one()
    item = session.query(CategoryItem).filter_by(id=item_id).one()
    return render_template('category_item.html',category=category,category_item=item)

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
            picture = filename)
        session.add(newCategory)
        #flash('New Category %s Successfully Created' % newCategory.name)
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
        #os.remove(os.path.join(app.config['UPLOADED_ITEMS_DEST'], categoryToDelete.filename))
        #flash('New Category %s Successfully Created' % newCategory.name)
        session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('deleteCategory.html',category=category)

# Add a new item
@app.route('/categories/<category>/newitem', methods=['GET', 'POST'])
def addNewItem(category):
    if 'username' not in login_session:
        return redirect('/login')
    categoryForItems = session.query(Category).filter_by(name=category).one()
    if login_session['user_id'] != category.user_id:
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
        #flash('New Item %s Successfully Created' % newItem.name)
        session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('newItem.html',category=category)

# Update a single Item
@app.route('/<category>/<int:item_id>/updateItem', methods=['GET', 'POST'])
def updateItem(category,item_id):
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
        #flash('New Category %s Successfully Created' % newCategory.name)
        session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('updateItem.html', category=category, item=item)

# Delete a single Item
@app.route('/<category>/<int:item_id>/deleteItem', methods=['GET', 'POST'])
def deleteItem(category,item_id):
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
        #os.remove(os.path.join(app.config['UPLOADED_ITEMS_DEST'], item.filename))
        #flash('New Category %s Successfully Created' % newCategory.name)
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

# Show components page
@app.route('/components')
def components():
    return render_template('components.html')

# Show contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Show services page
@app.route('/services')
def services():
    return render_template('services.html')


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run()
    app.run(host='0.0.0.0', port=3000)
