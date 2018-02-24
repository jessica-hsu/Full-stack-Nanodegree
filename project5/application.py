# !/usr/bin/env python

from flask import Flask, render_template, request, redirect, url_for, jsonify, session as login_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from database_setup import Base, Category, Item, User
# import things for GitHub login
from flask_github import GitHub

app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# if you don't scope it, you will have problems and a huge headache
session = scoped_session(DBSession)

SECRET_KEY = "`[i=H`fe3}DP/be/FyhE:--9v|AdTqt.j@EJlfm/Um?pZ`KJy&(dp7,719WnM})"
GITHUB_CLIENT_ID = ""
GITHUB_CLIENT_SECRET = ""
github = GitHub(app)

# Create JSON object for Categories
@app.route('/category/JSON')
def categoryJSON():
	category = session.query(Category).all()
	return jsonify(category=[c.serialize for c in category])

# Create JSON object for Item
@app.route('/items/JSON')
def itemJSON(category_id):
	item = session.query(Item).filter_by(category_id=category_id)
	return jsonify(item=[i.serialize for i in item])

# Load main home page
# valid URL for accessing home page
@app.route('/')
def load_main_page():
	# render results to home page
	all_categories = session.query(Category).all()
	if ('name' in login_session):
		logged_in_name = login_session['name']
	else:
		logged_in_name = "Random Stranga"
	return render_template('index.html', categories=all_categories, the_user_name=logged_in_name)

# View items in selected category
# valid URL for viewing items of a category
@app.route('/category/<category_id>')
def view_category_items(category_id):
	all_categories = session.query(Category).all()
	current_category = session.query(Category).filter_by(id=category_id).first()
	# query to retrieve all items under selected category
	items = session.query(Item).filter_by(category_id=category_id)
	if ('name' in login_session):
		logged_in_name = login_session['name']
	else:
		logged_in_name = "Random Stranga"
	return render_template('show-items.html',categories=all_categories,items=items
						   ,category=current_category, the_user_name=logged_in_name)

# Add new category
# valid URL for accessing add category page
# LOGIN REQUIRED
@app.route('/category/add', methods=['GET', 'POST'])
def add_category():
	if (request.method == 'POST'):	# post to database when user clicks submit
		new_name = request.form['category-name']	# get new category name from form
		new_category = Category(name=new_name)
		session.add(new_category)
		session.commit()
		return redirect(url_for('load_main_page', the_user_name=login_session['name']))
	else:
		all_categories = session.query(Category).all()
		if ('name' in login_session):
			logged_in_name = login_session['name']
		else:
			logged_in_name = "Random Stranga"
		return render_template('add-category.html', categories=all_categories, the_user_name=logged_in_name)

# View categories to delete
# valid URL for viewing categories to delete
# LOGIN REQUIRED
@app.route('/category/delete')
def view_categories_to_delete():
	if ('name' in login_session):
		logged_in_name = login_session['name']
		deleted_categories = session.query(Category).filter_by(user_id=login_session['id']).all()
		all_categories = session.query(Category).all()
		return render_template('delete-category.html', categories=all_categories, deleted=deleted_categories,
								the_user_name=logged_in_name)
	else:
		logged_in_name = "Random Stranga"
		all_categories = session.query(Category).all()
		return render_template('delete-category.html', categories=all_categories, the_user_name=logged_in_name)

# Delete category
# valid URL to actually delete category from database
# LOGIN REQUIRED
@app.route('/category/<category_id>/delete')
def delete_category_now(category_id):
	category_to_delete = session.query(Category).filter_by(id=category_id).first()
	session.delete(category_to_delete)
	session.commit()
	return redirect(url_for('view_categories_to_delete', the_user_name=login_session['name']))	# if successful, go back to see available categories to delete

# Add new item
# valid URL to add items
# LOGIN REQUIRED
@app.route('/category/<category_id>/add', methods=['GET', 'POST'])
def add_item(category_id):
	category = session.query(Category).filter_by(id=category_id).first()
	if (request.method == 'POST'):
		new_item_name = request.form['item-name']
		new_item_description = request.form['item-description']
		new_item = Item(name=new_item_name, description=new_item_description, category_id=category_id)
		session.add(new_item)
		session.commit()
		# redirect to see all items in selected category
		return redirect(url_for('view_category_items', category_id=category_id, category_name=category.name, the_user_name=login_session['name']))
	else:
		all_categories = session.query(Category).all()
		if ('name' in login_session):
			logged_in_name = login_session['name']
		else:
			logged_in_name = "Random Stranga"
		return render_template('add-item.html', categories=all_categories,category=category, the_user_name=logged_in_name)

# Edit item
# valid URL to edit item
# LOGIN REQUIRED
@app.route('/category/<category_id>/<item_id>/edit', methods=['GET', 'POST'])
def edit_item(category_id, item_id):
	category = session.query(Category).filter_by(id=category_id).first()
	item_to_edit = session.query(Item).filter_by(id=item_id).first()
	if (request.method == 'POST'):
		new_name = request.form['item-name']
		new_description = request.form['item-description']
		item_to_edit.name = new_name
		item_to_edit.description = new_description
		session.add(item_to_edit)
		session.commit()
		# redirect to see all items in selected category
		return redirect(url_for('view_category_items', category_id=category_id, the_user_name=login_session['name']))
	else:
		all_categories = session.query(Category).all()
		if ('name' in login_session):
			logged_in_name = login_session['name']
		else:
			logged_in_name = "Random Stranga"
		return render_template('edit-item.html', categories=all_categories, item=item_to_edit,
								category=category, item_id=item_id, the_user_name=logged_in_name)

# Delete item
# valid url to delete item from db
# LOGIN REQUIRED
@app.route('/category/<category_id>/<item_id>/delete')
def delete_item(category_id, item_id):
	item_to_delete = session.query(Item).filter_by(id=item_id).first()
	session.delete(item_to_delete)
	session.commit()
	# redirect to see all items in selected category
	return redirect(url_for('view_category_items', category_id=category_id, the_user_name=login_session['name']))

# Login Page
@app.route('/login')
def login():
	# redirect to GitHub for authentication
	return github.authorize()
	# set session variables
	# login_session['id'] = 1
	# login_session['name'] = 'admin'
	# # check database if this user email exists. If yes, get name and id from DB. If not, also add to database
	# if ('name' in login_session):
	# 	return redirect(url_for('load_main_page', the_user_name=login_session['name']))
	# else:

# Logout
@app.route('/logout')
def logout():
	# release session variables
	del login_session['id']
	del login_session['name']
	return redirect(url_for('load_main_page'))

# GitHub authorization handler
@app.route('/github-callback')
@github.authorized_handler
def authorized(oauth_token):
	# if somehow failed, go back to home page
	if (oauth_token is None):
		flash("Login failed.")
		return redirect(url_for('load_main_page'))

	# check if user already in database
	user = session.query(User).filter_by(access_token=oauth_token).first()

	if (user is None):	# user not in db, so get user profile for name and email and add to database
		u = github.get('user')
		user = User(name=u.name, email=u.email, access_token=oauth_token)
		session.add(user)
		session.commit()
	else:	# user already in db, set session variables with query results
		login_session['name'] = user.name
		login_session['id'] = user.id


# Main method
if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5000)
