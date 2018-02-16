# populate catalog database with dummy database
# !/usr/bin/env python

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Catalog, Item

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# method to add and commit
def add_to_database(record):
    session.add(record)
    session.commit()

# Create some Categories
furniture = Category(name='Furniture')
add_to_database(furniture)

stationary = Category(name='Stationary')
add_to_database(stationary)

food = Category(name='Food')
add_to_database(food)

electronics = Category(name='Electronics')
add_to_database(electronics)

# Add items to each category
item = Item(name='Chair', description='Thing you sit on', category_id=1)
add_to_database(item)

item = Item(name='Table', description='Thing you put things on', category_id=1)
add_to_database(item)

item = Item(name='Closet', description='Thing you put things in', category_id=1)
add_to_database(item)
