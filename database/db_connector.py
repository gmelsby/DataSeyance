# Citation for the following file
# Date: 5/19/2022
# Mostly Copied from CS340 Flask Starter App
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
            
            
    db_connection.ping(True)
    return db_connection

def execute_query(query, query_params=(), quantity="many"):
    '''
    executes a given SQL query on the given db connection and returns a Cursor object

    db_connection: a MySQLdb connection object created by connect_to_database()
    query: string containing SQL query
    query_params: the parameters that fill in variables in the query
    quantity: determines if fetchone or fetchall is called on the cursor

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
    if not (quantity == "many" or quantity == "one"):
        print("make sure quanity is either 'many' or 'one'")
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
    db_connection.commit();

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

if __name__ == '__main__':
    print("Executing a sample query on the database using the credentials from db_credentials.py")
    db = connect_to_database()
    query = "SELECT * from bsg_people;"
    results = execute_query(db, query);
    print("Printing results of %s" % query)

    for r in results.fetchall():
        print(r)