#!/usr/bin/env python
# continue database setup by populating catalog database with records

import psycopg2

# Open connection to the PostgreSQL database.  Returns a connection
def open():
    conn = psycopg2.connect("dbname=catalog")
    return conn

# commits connection, takes existing connection and cursor and closes them
def close(conn, cursor):
    conn.commit()
    cursor.close()
    conn.close()

# Add the first user to the User table
def populateUser():
    conn = open()
    cursor = conn.cursor()
    sql = "INSERT INTO user (name, email) VALUES ('admin', 'admin@gmail.com')"
    cursor.execute(sql)
    close(conn, cursor)

# Add a few categories in Category table
def populateCategory():
    conn = open()
    cursor = conn.cursor()
    sql = "INSERT INTO category (name, created_by) VALUES ()"
    cursor.execute(sql)
    close(conn, cursor)

# Add a few items in each existing category
def populateItem():
    conn = open()
    cursor = conn.cursor()
    sql = "INSERT INTO item (category, created_by, name) VALUES ()"
    cursor.execute(sql)
    close(conn, cursor)

# main method to execute the functions
if __name__ == '__main__':
    populateUser()  # add user
    populateCategory()  # add categories
    populateItem()  # add items
    print "Catalog database populated."
