import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine

Base = declarative_base()

# create table for categories
class Category(Base):
	__tablename__ = 'category'

	# column names
	id = Column(Integer, primary_key=True)
	name = Column(String(200), nullable=False)

	# return as JSON object
	@property
	def serialize(self):
		return {
			'id': self.id,
			'name': self.name,
		}


# create table for category items
class Item(Base):
	__tablename__ = 'item'

	# column names
	id = Column(Integer, primary_key=True)
	name = Column(String(200), nullable=False)
	description = Column(String(500))
	category_id = Column(Integer, ForeignKey('category.id'))
	# cascade will delete all items in category if said category gets deleted
	category = relationship(Category, backref=backref('items', uselist=True, cascade='delete, all'))

	# return as JSON object
	@property
	def serialize(self):
		return {
			'id': self.id,
			'name': self.name,
			'description': self.description,
		}

engine = create_engine('sqlite:///catalog.db')

Base.metadata.create_all(engine)
