from flask import Flask, render_template, request, url_for, redirect
from flask_uploads import UploadSet, configure_uploads, IMAGES
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Category, CategoryItem, Base

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
    print("succeed1")
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
