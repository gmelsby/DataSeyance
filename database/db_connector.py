# Citation for the following file
# Date:  6/4/2022
# Adapted from CS340 Flask Starter App
# Several modifications made to ensure functionality--original program returned a cursor instead of query results
# Also, original program would time out because it did not call db_connection.ping(True)
# execute_queries function is also original. Alllows mutliple queries to be executed as a single transaction.
# source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/database/db_connector.py
# Added db_connection.ping(True) and execute_queries function ourselves

import MySQLdb
import os
from dotenv import load_dotenv, find_dotenv

# Load our environment variables from the .env file in the root of our project.
load_dotenv(find_dotenv())

# Set the variables in our application with those environment variables
host = os.environ.get("340DBHOST")
user = os.environ.get("340DBUSER")
passwd = os.environ.get("340DBPW")
db = os.environ.get("340DB")

def connect_to_database(host = host, user = user, passwd = passwd, db = db):
    '''
    connects to a database and returns a database objects
    '''
    db_connection = MySQLdb.connect(host,user,passwd,db)
            
    # see info about function at http://www.neotitans.com/resources/python/mysql-python-connection-error-2006.html
    # fixed CS340 Flask Starter App by adding this line--otherwise it times out!
    db_connection.ping(True)
    return db_connection

def execute_query(query, query_params=(), quantity="many"):
    '''
    executes a given SQL query on the given db connection and returns results specified by quantity kwarg

    db_connection: a MySQLdb connection object created by connect_to_database()
    query: string containing SQL query
    query_params: the parameters that fill in variables in the query
    quantity: determines if nothing, fetchone or fetchall is called on the cursor
        accepted values are "zero", "one", and "many"

    returns: the results of the query
    '''

    db_connection = connect_to_database(host, user, passwd, db)
    if db_connection is None:
        print("No connection to the database found! Have you called connect_to_database() first?")
        return None

    if query is None or len(query.strip()) == 0:
        print("query is empty! Please pass a SQL query in query")
        return None
    
    # check that quanity is a valid parameter
    if not (quantity == "zero" or quantity == "many" or quantity == "one"):
        print("make sure quanity is either 'zero', 'many' or 'one'")
        return None

    print("Executing %s with %s" % (query, query_params));
    # Create a cursor to execute query. Why? Because apparently they optimize execution by retaining a reference according to PEP0249
    cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)

    '''
    params = tuple()
    #create a tuple of paramters to send with the query
    for q in query_params:
        params = params + (q)
    '''
    
    cursor.execute(query, query_params)
    # this will actually commit any changes to the database. without this no
    # changes will be committed!
    db_connection.commit()

    if quantity == "zero":
        cursor.close()
        return

    print(f"Fetching quantity {quantity}")
    # sepecifies which cursor method will be called on the cursor based on quantity parameter
    fetchdict = {"many" : cursor.fetchall, "one": cursor.fetchone}
    records = fetchdict[quantity]()
    cursor.close()
    return records

def execute_queries(queries, query_params = ()):
    '''
    Same as execute_query but takes a list of queries and a list of params for each query
    Does not return any records
    '''
    db_connection = connect_to_database(host, user, passwd, db)
    if db_connection is None:
        print("No connection to the database found! Have you called connect_to_database() first?")
        return None
    if queries is None or len(queries) == 0:
        print("You need to pass in a list of SQL queries")
        return None

    cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
    for index, query in enumerate(queries):
        print(f"Executing {query} with {query_params}")
        cursor.execute(query, query_params[index])
        
    db_connection.commit();
    return cursor
