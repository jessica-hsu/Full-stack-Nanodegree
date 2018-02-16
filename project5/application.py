# !/usr/bin/env python

from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item

app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# global variables - to be used for every page rendering
# load all categories. To be used in side bar for every page
all_categories = all_categories = session.query(Category).all()

# Create JSON object for Categories
# @app.route('/category/JSON')
#
# # Create JSON object for Item
# @app.route('/items/JSON')

# Load main home page
# valid URL for accessing home page
@app.route('/')
@app.route('/catalog')
def load_main_page():
	# render results to home page
	return render_template('index.html', categories=all_categories)


# View items in selected category
# valid URL for viewing items of a category
@app.route('/category/<int:category_id>')
def view_category_items(category_id):
	# query to retrieve all items under selected category
	items = session.query(Item).filter_by(category_id=category_id).all()
	return render_template('show-items.html',categories=all_categories,items=items)

# Add new category
# valid URL for accessing add category page
@app.route('/category/add', methods=['GET', 'POST'])
def add_category():
	new_name = requset.form['category-name']	# get new category name from form
	if (request.method == 'POST'):	# post to database when user clicks submit
		new_category = Category(name=new_name)
		session.add(new_category)
		session.commit()
	return redirect('/')	# go back to home page to see new category appear

# View categories to delete
# valid URL for viewing categories to delete
@app.route('/category/delete')
def view_categories_to_delete():
	return render_template('delete-category.html', categories=all_categories)

# Delete category
# valid URL to actually delete category from database
@app.route('/category/delete/confirm')


# # Add new item
# # valid URL to add items
# @app.route('/category/<int:category_id>/add')
#
# # Edit item
# # valid URL to edit item
# @app.route('/category/<int:category_id>/<int:item_id>/edit')
#
# # Delete item
# # valid url to delete item from db
# @app.route('/category/<int:category_id>/<int:item_id>/delete')
#
# # Login Page
# @app.route('/login')
#
# # Logout
# @app.route('/logout')

# Main method
if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5000)
