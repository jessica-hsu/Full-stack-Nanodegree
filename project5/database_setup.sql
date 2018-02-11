-- Create database catalog for project 5.

-- Check if catalog db exists. If YES, drop database. If NO, create database.
DROP DATABASE IF EXISTS catalog;
CREATE DATABASE catalog;

-- connect to catalog database so tables will be created in the correct db
\c catalog

-- Drop/Create user table
DROP TABLE IF EXISTS user CASCADE; --CASCADE needed to remove dependency
CREATE TABLE user (
	user_id serial not null,
	name text not null,
  email text not null,
	PRIMARY KEY(user_id)
);

-- Drop/Create category table
DROP TABLE IF EXISTS category CASCADE; --CASCADE needed to remove dependency
CREATE TABLE category (
	category_id serial not null,
	name text not null,
  created_by int references user(user_id) not null,
	PRIMARY KEY(category_id)
);

-- Drop/Create item table
DROP TABLE IF EXISTS item;
CREATE TABLE item (
	item_id serial not null,
	category int references category(category_id) not null,
	created_by int references user(user_id) not null,
  name text not null,
	PRIMARY KEY(item_id)
);
