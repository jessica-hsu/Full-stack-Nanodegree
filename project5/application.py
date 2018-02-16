# !/usr/bin/env python

from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Catalog, Item

app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create JSON object for Categories
@app.route('/category/JSON')

# Create JSON object for Item
@app.route('/items/JSON')

# Load main home page
# valid URL for accessing home page
@app.route('/')
@app.route('/catalog')

# View items in selected category
# valid URL for viewing items of a category
@app.route('/category/<int:category_id>')

# Add new category
# valid URL for accessing add category page
@app.route('/category/add')

# View categories to delete
# valid URL for viewing categories to delete
@app.route('/category/delete')

# Delete category
# valid URL to actually delete category from database
@app.route('/category/delete/confirm')

# Add new item
# valid URL to add items
@app.route('/category/<int:category_id>/add')

# Edit item
# valid URL to edit item
@app.route('/category/<int:category_id>/<int:item_id>/edit')

# Delete item
# valid url to delete item from db
@app.route('/category/<int:category_id>/<int:item_id>/delete')

# Login Page
@app.route('/login')

# Logout
@app.route('/logout')

# Main method
if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5000)
