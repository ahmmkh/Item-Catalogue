from flask import Flask, render_template
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Category, CategoryItem, Base

app = Flask(__name__)

engine = create_engine('sqlite:///items.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/categories')
def index():
    categories = session.query(Category).order_by(asc(Category.name))
    return render_template('index.html',categories=categories)

@app.route('/categories/<int:category_id>')
def showCategory(category_id):
    category = session.query(Category).filter_by(id=category_id).one()

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/components')
def components():
    return render_template('components.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/project.html')
def project():
    return render_template('project.html')

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run()
    app.run(host='0.0.0.0', port=3000)
