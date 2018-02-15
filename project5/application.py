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

# Create JSON object for Item

# Load main home page
# valid URL for accessing home page



# Add new category
# valid URL for accessing add category page

# View categories to delete
# valid URL for viewing categories to delete

# Delete category
# valid URL to actually delete category from database

# Add new item
# valid URL to add items

# Edit item
# valid URL to edit item

# Delete item
# valid url to delete item from db

# Login Page

# Logout

# Main method
if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5000) 