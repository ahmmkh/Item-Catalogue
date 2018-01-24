from flask import Flask, render_template, request, url_for, redirect
from flask_uploads import UploadSet, configure_uploads, IMAGES
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Category, CategoryItem, Base
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

# Delete a single Item
@app.route('/<category>/<int:item_id>/deleteItem', methods=['GET', 'POST'])
def deleteItem(category,item_id):
    category = session.query(Category).filter_by(name=category).one()
    item = session.query(CategoryItem).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(item)
        #os.remove(os.path.join(app.config['UPLOADED_ITEMS_DEST'], item.filename))
        #flash('New Category %s Successfully Created' % newCategory.name)
        session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('deleteItem.html', category=category, item=item)

# Update a single Item
@app.route('/<category>/<int:item_id>/updateItem', methods=['GET', 'POST'])
def updateItem(category,item_id):
    category = session.query(Category).filter_by(name=category).one()
    item = session.query(CategoryItem).filter_by(id=item_id).one()
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

# Add a new category
@app.route('/categories/new', methods=['GET', 'POST'])
def newCategory():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        newCategory = Category(
            name=request.form['name'],
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
    categoryForItems = session.query(Category).filter_by(name=category).one()
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
