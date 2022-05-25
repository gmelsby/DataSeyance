from flask import Flask, render_template, redirect, json, request
from flask_mysqldb import MySQL
import os
import MySQLdb
import database.db_connector as db
import toml

app = Flask(__name__)
mysql = MySQL(app)

queries = toml.load("models/queries.toml")

@app.route('/')
def root():
    return redirect("/index", code=302)


@app.route('/index')
def index():
    return render_template('index.j2')

@app.route('/attendees', methods=['GET', 'POST'])
def attendees():
    if request.method == 'POST':
        # if the POST request has id_input the update form has been submitted
        # We only want to update if the name is nonempty
        if request.form.get('id_input') and request.form.get('new_name'):
            # prepare entered strings for SQL Query
            full_name_input = request.form['new_name'].strip()
            id_input = request.form['id_input']
            
            query = ('UPDATE Attendees '
                     f'SET full_name = "{full_name_input}" '
                     f'WHERE attendee_id = {id_input};')
            
            cursor = db.execute_query(query=query)
            mysql.connection.commit()

            return redirect('/attendees')

        # otherwise we are inserting a new Attendee
        # We do not want Attendees with empty names
        if request.form.get('name'):
            full_name_input = request.form['name'].strip()
            # Because we are potentially inserting into our intersection table too, we want an array of queries
            # These will be executed sequentially
            queries = [f'INSERT INTO Attendees (full_name) VALUES ("{full_name_input}");']
            # if a seance_id has been selected we also add the Attendee to the SeanceAttendees table
            if request.form['seance_id']:
                queries.append(f'SET @new_attendee_id = LAST_INSERT_ID();')
                seance_id_input = request.form['seance_id']
                queries.append('INSERT INTO SeanceAttendees (attendee_id, seance_id) '
                         f'VALUES (@new_attendee_id, {seance_id_input});')
                
            # These queries must be executed all at once in a unit
            # We only commit when all are executed
            cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
            for query in queries:
                cursor.execute(query)
            mysql.connection.commit()
            
        return redirect('/attendees')
            
            
    # displays the table of all attendees
    if request.method == 'GET':
        args = request.args
        # we could potentially ahve no get query parameters, so attendee_to_edit starts as None
        attendee_to_edit = None
        # if we have get query parameter indicating attendee_id we get the info for the dropdown
        if args.get('id'):
            preselect_query = f"SELECT attendee_id, full_name FROM Attendees WHERE attendee_id = {args.get('id')};"
            cursor = db.execute_query(query=preselect_query)
            attendee_to_edit = cursor.fetchone()
            
        # attendee data to be displayed in table and used for update dropdown
        attendee_query = 'SELECT attendee_id, full_name FROM Attendees;'
        cursor = db.execute_query(query=attendee_query)
        attendee_data = cursor.fetchall()
        
        # seance data to be used in dropdown for adding an attendee
        seance_query = ('SELECT seance_id, Locations.name, Seances.date '
                        'FROM Seances ' 
                        'LEFT JOIN Locations ON Seances.location_id = Locations.location_id;')
                        
        cursor = db.execute_query(query=seance_query)
        seance_data = cursor.fetchall()

        return render_template('attendees.j2', attendee_data=attendee_data, seance_data=seance_data, attendee_to_edit=attendee_to_edit)
    

@app.route('/delete_attendee/<int:id>')
def delete_attendee(id):
    query = f'DELETE FROM Attendees WHERE attendee_id = {id};'
    cursor = db.execute_query(query=query)
    mysql.connection.commit()
    
    return redirect('/attendees')


@app.route('/channelings', methods=['GET', 'POST'])
def channelings():
    if request.method == 'POST':
        content = request.form.to_dict()
        print(content)



    # if request.method == 'GET':
    args = request.args
#     # chosen_seance defaults to None unless we have id passed in in GET param
    chosen_seance_id = args.get('id')
    chosen_seance = None
    if chosen_seance_id:
        chosen_seance_query = ('SELECT seance_id, Locations.name, Seances.date '
                               'FROM Seances '
                               'LEFT JOIN Locations ON Seances.location_id = Locations.location_id '
                              f'WHERE Seances.seance_id = {chosen_seance_id}')
        cursor = db.execute_query( query=chosen_seance_query)
        chosen_seance = cursor.fetchone()

        # query for getting all relevant channeling data
    channeling_query = ('SELECT Channelings.channeling_id, Mediums.full_name AS medium_name, Spirits.full_name AS spirit_name, '
                       'Methods.name AS method_name, Seances.date, Locations.name AS location_name, '
                       'Channelings.is_successful, Channelings.length_in_minutes '
                       'FROM Channelings '
                       'LEFT JOIN Mediums ON Channelings.medium_id = Mediums.medium_id '
                       'LEFT JOIN Spirits ON Channelings.spirit_id = Spirits.spirit_id '
                       'LEFT JOIN Methods ON Channelings.method_id = Methods.method_id '
                       'LEFT JOIN Seances ON Channelings.seance_id = Seances.seance_id '
                       'LEFT JOIN Locations ON Seances.location_id = Locations.location_id')
            # add a filter if a seance_id has been chosen
    if chosen_seance_id:
        channeling_query += f' WHERE Seances.seance_id = {chosen_seance_id}'
    # add a semicolon whether we have a filter or not
        channeling_query += ';'

    cursor = db.execute_query(query=channeling_query)
    channeling_data = cursor.fetchall()

    # query for getting seance data to populate dropdown
    seance_query = ('SELECT seance_id, Locations.name, Seances.date '
                    'FROM Seances ' 
                    'LEFT JOIN Locations ON Seances.location_id = Locations.location_id;')
    cursor = db.execute_query(query=seance_query)
    seance_data = cursor.fetchall()

    # query for getting medium data to populate dropdown
    medium_query = ('SELECT medium_id, full_name FROM Mediums;')
    cursor = db.execute_query(query=medium_query)
    medium_data = cursor.fetchall()

    # query for getting spirit data to populate dropdown
    spirit_query = ('SELECT spirit_id, full_name FROM Spirits;')
    cursor = db.execute_query(query=spirit_query)
    spirit_data = cursor.fetchall()

    # query for getting method data to populate dropdown
    method_query = ('SELECT method_id, name FROM Methods;')
    cursor = db.execute_query(query=method_query)
    method_data = cursor.fetchall()

    return render_template('channelings.j2', chosen_seance='None', channeling_data=channeling_data,
                            seance_data=seance_data, medium_data=medium_data, spirit_data=spirit_data,
                            method_data=method_data)



@app.route('/locations', methods=['GET', 'POST'])
def locations():
    if request.method == 'POST':
        # if POST form has id_input, update form has been submitted
        if request.form.get('id_input'):
            # Process each input to be NULL if empty string
            id_input = request.form['id_input']
            name_input = f'"{request.form["new_name"].strip()}"' if request.form.get('new_name').strip() != '' else 'NULL'
            street_input = f'"{request.form["new_street_address"].strip()}"' if request.form.get('new_street_address').strip() != '' else 'NULL'
            city_input = f'"{request.form["new_city"].strip()}"' if request.form.get('new_city').strip() != '' else 'NULL'
            zip_input = f'"{request.form["new_zip"]}"' if request.form.get('new_zip') else 'NULL'
            state_input = f'"{request.form["new_state"]}"' if request.form.get('new_state') else 'NULL'
            country_input = f'"{request.form["new_country"].strip()}"' if request.form.get('new_country').strip() != '' else 'NULL'
            
            # query for updating location with location_id id_input
            query = ('UPDATE Locations '
                    f'SET name = {name_input}, '
                    f'street_address = {street_input}, '
                    f'city = {city_input}, '
                    f'zip = {zip_input}, '
                    f'state = {state_input}, '
                    f'country = {country_input} '
                    f'WHERE location_id = {id_input}')
            
            cursor = db.execute_query(query=query)
            mysql.connection.commit()
            
            return redirect('/locations')

        # if POST form has name, create form has been submitted
        if request.form.get('name') is not None:
            # Process each input to be NULL if empty string
            name_input = f'"{request.form["name"].strip()}"' if request.form.get('name').strip() != '' else 'NULL'
            street_input = f'"{request.form["street_address"].strip()}"' if request.form.get('street_address').strip() != '' else 'NULL'
            city_input = f'"{request.form["city"].strip()}"' if request.form.get('city').strip() != '' else 'NULL'
            zip_input = f'"{request.form["zip"]}"' if request.form.get('zip') else 'NULL'
            state_input =f'"{request.form["state"]}"' if request.form.get('state') else 'NULL'
            country_input = f'"{request.form["country"].strip()}"' if request.form.get('country') != '' else 'NULL'
            
            # query for making new location
            query = ('INSERT INTO Locations (name, street_address, city, zip, state, country) '
                    f'VALUES ({name_input}, {street_input}, {city_input}, {zip_input}, {state_input}, {country_input});')

            cursor = db.execute_query(query=query)
            mysql.connection.commit()

            return redirect('/locations')

        return redirect('/locations')


    # Read functionality
    if request.method == 'GET':
        args = request.args
        # only have a location to edit if id passed in in GET params, othewise it's None
        location_to_edit = None
        if args.get('id'):
            preselect_query = ('SELECT location_id, name, street_address, city, zip, state, country '
                               'FROM Locations '
                               f'WHERE location_id = {args.get("id")};')
            cursor = db.execute_query(query=preselect_query)
            location_to_edit = cursor.fetchone()
            
            # Removes 'None' from prefill--if a value is NULL, we get empty string instead
            for key, value in location_to_edit.items():
                if value is None:
                    location_to_edit[key] = ''


        # query for displaying all info about Locations in table
        query = ('SELECT location_id, name, street_address, city, zip, state, country '
                 'FROM Locations;')
        cursor = db.execute_query(query=query)
        location_data = cursor.fetchall()

        return render_template('locations.j2', location_data=location_data, location_to_edit=location_to_edit)

@app.route('/delete_location/<int:id>')
def delete_location(id):
    # removes the location with indicated id
    query = f'DELETE FROM Locations WHERE location_id = {id};'
    cursor = db.execute_query(query=query)
    mysql.connection.commit()
    
    return redirect('/locations')


@app.route('/mediums', methods=['GET', 'POST'])
def mediums():
    if request.method == 'POST':
        # if the POST form has id_input the update form has been submitted
        # We only want to update if the name is nonempty
        if request.form.get('id_input') and request.form.get('new_name'):
            full_name_input = request.form['new_name'].strip()
            id_input = request.form['id_input']

            query = ('UPDATE Mediums ' 
                     f'SET full_name = "{full_name_input}" '
                     f'WHERE medium_id = {id_input};')

            cursor = db.execute_query(query=query)
            mysql.connection.commit()
            
            return redirect('/mediums')

        # otherwise if the POST form has name the insert form has been submitted
        # if name is empty we just skip the insert and redirect back to /mediums
        if request.form.get('name'):
            full_name_input = request.form['name'].strip()
            query = f'INSERT INTO Mediums (full_name) VALUES ("{full_name_input}");'
            cursor = db.execute_query(query=query)
            mysql.connection.commit()
            
        return redirect('/mediums')

    # displays table with all mediums
    if request.method == 'GET':
        args = request.args
        # if there is no medium to edit passed in in the get parameters we just leave medium_to_edit as None
        medium_to_edit = None
        # uses a select query to get info to preselect dropdown menu and prepopulate input
        if args.get('id'):
            preselect_query = f"SELECT medium_id, full_name FROM Mediums WHERE medium_id = {args.get('id')};"
            cursor = db.execute_query(query=preselect_query)
            medium_to_edit = cursor.fetchone()
            
        # main query for getting info for medium table
        query = 'SELECT medium_id, full_name FROM Mediums;'
        cursor = db.execute_query(query=query)
        medium_data = cursor.fetchall()

        return render_template('mediums.j2', medium_data=medium_data, medium_to_edit=medium_to_edit)
    
@app.route('/delete_medium/<int:id>')
def delete_medium(id):
    # deletes a medium based on id
    query = f'DELETE FROM Mediums WHERE medium_id = {id};'
    cursor = db.execute_query(query=query)
    mysql.connection.commit()
    
    return redirect('/mediums')


@app.route('/methods', methods=['GET', 'POST'])
def methods():
    # if the reqeust if of method POST we are either updating or creating
    if request.method == 'POST':
        # if id_input is in the request we are updating
        # makes sure new_name is not empty string
        if request.form.get('id_input') and request.form.get('new_name'):
            name_input = request.form['new_name'].strip()
            id_input = request.form['id_input']
            # if description_input is empty string we skip processing it and instead send in null
            description_input = 'NULL'
            if request.form.get('new_description'):
                description_input = f'"{request.form["new_description"]}"'


            # update query to change attributes of method with matching id_input
            query= ('UPDATE Methods ' 
                     f'SET name = "{name_input}", '
                     f'description = {description_input} '
                     f'WHERE method_id = {id_input};')

            cursor = db.execute_query(query=query)
            mysql.connection.commit()
            
            return redirect('/methods')

        # Create functionality--to be skipped if submitted name is empty
        if request.form.get('name'):
            name_input = request.form['name'].strip()
            # description is optional so initially set to NULL in case of empty string
            description_input = 'NULL'
            if request.form.get('description'):
                description_input = f'"{request.form["description"]}"'
            # creates new method
            query = f'INSERT INTO Methods (name, description) VALUES ("{name_input}", {description_input});'
            cursor = db.execute_query(query=query)
            mysql.connection.commit()
            
        return redirect('/methods')

    # Read functionality
    if request.method == 'GET':
        args = request.args
        # we might not have a preselected method in the query parameters, so default to None and adjust if necessary
        method_to_edit = None
        if args.get('id'):
            preselect_query = f"SELECT method_id, name, description FROM Methods WHERE method_id = {args.get('id')};"
            cursor = db.execute_query(query=preselect_query)
            method_to_edit = cursor.fetchone()
            
            # Remvoes 'None' from prefilled text input--if a value is NULL we just want an empty string
            for key, value in method_to_edit.items():
                if value is None:
                    method_to_edit[key] = ''
            
        query = 'SELECT method_id, name, description FROM Methods;'
        cursor = db.execute_query(query=query)
        method_data = cursor.fetchall()

        return render_template('methods.j2', method_data=method_data, method_to_edit=method_to_edit)
    

@app.route('/delete_method/<int:id>')
def delete_method(id):
    # removes method with associated method_id
    query = f'DELETE FROM Methods WHERE method_id = {id};'
    cursor = db.execute_query(query=query)
    mysql.connection.commit()
    
    return redirect('/methods')


@app.route('/seanceattendees')
def seanceattendees():
    return render_template('seanceattendees.j2')

@app.route('/seances', methods=['GET', 'POST'])
def seances():
    if request.method == 'POST':
        # if form has id_input we are updating
        if request.form.get('id_input'):
            # if any input is empty string we want it to be NULL instead
            id_input = request.form['id_input']
            date_input = f'"{request.form["new_date"]}"' if request.form.get('new_date') else 'NULL'
            location_id_input = f'{request.form["new_location_id"]}' if request.form.get('new_location_id') else 'NULL'

            # query for updating seance with matching id
            query = ('UPDATE Seances '
                    f'SET date = {date_input}, '
                    f'location_id = {location_id_input} '
                    f'WHERE seance_id = {id_input};')
            
            cursor = db.execute_query(query=query)
            mysql.connection.commit()

            return redirect('/seances')

        # otherwise we are creating a new seance
        else:
            # process out empty strings and turn them into NULLs
            date_input = f'"{request.form["date"]}"' if request.form.get('date') else 'NULL'
            location_id_input = f'{request.form["location_id"]}' if request.form.get('location_id') else 'NULL'

            # query for creating a new Seance
            query = ('INSERT INTO Seances (date, location_id) '
                    f'VALUES ({date_input}, {location_id_input});')

            cursor = db.execute_query(query=query)
            mysql.connection.commit()

            return redirect('/seances')

    # Read functionality
    if request.method == 'GET':
        args = request.args
        # there may not be a passed-in seance id to edit--default to None and adjusts if needed
        seance_to_edit = None
        if args.get('id'):
            preselect_query = ("SELECT Seances.seance_id, Locations.name, Seances.date, Locations.location_id "
                               "FROM Seances "
                               "LEFT JOIN Locations ON Seances.location_id = Locations.location_id "
                               f"WHERE Seances.seance_id = {args.get('id')};")
            cursor = db.execute_query(db_connection, query=preselect_query)
            seance_to_edit = cursor.fetchone()

        # gets list of seances to display in table and populate dropdowns
        seance_query = ("SELECT Seances.seance_id, Locations.name, Seances.date "
                        "FROM Seances "
                        "LEFT JOIN Locations ON Seances.location_id = Locations.location_id;")
        cursor = db.execute_query(query=seance_query)
        seance_data = cursor.fetchall()

        # gets list of locations to populate dropdowns
        location_query = ("SELECT location_id, name FROM Locations;")
        cursor = db.execute_query(query=location_query)
        location_data = cursor.fetchall()
        return render_template('seances.j2', seance_data=seance_data, seance_to_edit=seance_to_edit, location_data=location_data)

@app.route('/delete_seance/<int:id>')
def delete_seance(id):
    # removes a seance by id
    query = f'DELETE FROM Seances WHERE seance_id = {id};'
    cursor = db.execute_query(query=query)
    mysql.connection.commit()
    
    return redirect('/seances')


@app.route('/spirits', methods=['GET', 'POST'])
def spirits():
    # method will be post or get, get will pass to line 468
    edit_form = -1
    if request.method == 'POST':
        # we had a post so we are going to look at a parameter passed from a hidden form value
        # get form values as dict
        content = request.form.to_dict()
        # this hidden form value will tell us what to do
        action = content['action']
        #hidden value says upddate
        if action == 'tagupdate':
           edit_form = int(content['id_input'])

        if action == 'update':
            #get update query from toml and send it with parameters (see /home/ed/DataSeyance/models/queries.toml)
            print(int(content['id_input']))
            db.execute_query(query=queries['spirits'][action]
                             , query_params=(content['new_name'], int(content['id_input'])))
        # get insert query from toml and send it with parameter (see /home/ed/DataSeyance/models/queries.toml)
        if action == 'insert':
            db.execute_query(query=queries['spirits'][action], query_params=(content['insert_full_name'],))

        if action == 'delete':
            db.execute_query(query=queries['spirits'][action], query_params=(content['spirit_id'],))

    spirit_data = db.execute_query(query=queries['spirits']['select'])

    return render_template('spirits.j2', spirit_data=spirit_data,  edit_form=edit_form)




if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5005))
    app.run(port=port, debug=True)