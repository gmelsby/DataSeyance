
from flask import Flask, render_template, redirect, json, request
from flask_mysqldb import MySQL
import os
import MySQLdb
import database.db_connector as db

db_connection = db.connect_to_database()

app = Flask(__name__)
mysql = MySQL(app)

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
            
            cursor = db.execute_query(db_connection=db_connection, query=query)

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
            cursor = db.execute_query(db_connection=db_connection, query=preselect_query)
            attendee_to_edit = cursor.fetchone()
            
        # attendee data to be displayed in table and used for update dropdown
        attendee_query = 'SELECT attendee_id, full_name FROM Attendees;'
        cursor = db.execute_query(db_connection=db_connection, query=attendee_query)
        attendee_data = cursor.fetchall()
        
        # seance data to be used in dropdown for adding an attendee
        seance_query = ('SELECT seance_id, Locations.name, Seances.date '
                        'FROM Seances ' 
                        'LEFT JOIN Locations ON Seances.location_id = Locations.location_id;')
                        
        cursor = db.execute_query(db_connection=db_connection, query=seance_query)
        seance_data = cursor.fetchall()

        return render_template('attendees.j2', attendee_data=attendee_data, seance_data=seance_data, attendee_to_edit=attendee_to_edit)
    

@app.route('/delete_attendee/<int:id>')
def delete_attendee(id):
    query = f'DELETE FROM Attendees WHERE attendee_id = {id};'
    cursor = db.execute_query(db_connection=db_connection, query=query)
    
    return redirect('/attendees')


@app.route('/channelings', methods=['GET', 'POST'])
def channelings():
    # our channelings table does not support update, so POST is only creation
    if request.method == 'POST':
        # process our inputs to put in NULL if any are empty
        seance_input = request.form['seance_id'] if request.form.get('seance_id') else 'NULL'
        medium_input = request.form['medium_id'] if request.form.get('medium_id') else 'NULL'
        spirit_input = request.form['spirit_id'] if request.form.get('spirit_id') else 'NULL'
        method_input = request.form['method_id'] if request.form.get('method_id') else 'NULL'
        success_input = 1 if request.form.get('is_successful') is not None else 0
        length_input = request.form['length'] if request.form.get('length') != '' else 'NULL'
        
        # query for adding a new channeling
        query = ('INSERT INTO Channelings (medium_id, seance_id, spirit_id, method_id, is_successful, length_in_minutes) '
                 'VALUES ('
                f'{medium_input}, {seance_input}, {spirit_input}, {method_input}, {success_input}, {length_input});')
                 
        cursor = db.execute_query(db_connection=db_connection, query=query)
        
        # redirect to the inputted seance_id if passed in
        if seance_input != 'NULL':
            return redirect(f'/channelings?id={seance_input}')
        # otherwise just redirect to channelings
        return redirect('/channelings')

    # read functionality
    if request.method == 'GET':
        args = request.args
        # chosen_seance defaults to None unless we have id passed in in GET param
        chosen_seance_id = args.get('id')
        chosen_seance = None
        if chosen_seance_id:
            chosen_seance_query = ('SELECT seance_id, Locations.name, Seances.date '
                                   'FROM Seances '
                                   'LEFT JOIN Locations ON Seances.location_id = Locations.location_id '
                                  f'WHERE Seances.seance_id = {chosen_seance_id}')
            cursor = db.execute_query(db_connection=db_connection, query=chosen_seance_query)
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
        
        cursor = db.execute_query(db_connection=db_connection, query=channeling_query)
        channeling_data = cursor.fetchall()
        
        # query for getting seance data to populate dropdown
        seance_query = ('SELECT seance_id, Locations.name, Seances.date '
                        'FROM Seances ' 
                        'LEFT JOIN Locations ON Seances.location_id = Locations.location_id;')
        cursor = db.execute_query(db_connection=db_connection, query=seance_query)
        seance_data = cursor.fetchall()
        
        # query for getting medium data to populate dropdown
        medium_query = ('SELECT medium_id, full_name FROM Mediums;')
        cursor = db.execute_query(db_connection=db_connection, query=medium_query)
        medium_data = cursor.fetchall()
        
        # query for getting spirit data to populate dropdown
        spirit_query = ('SELECT spirit_id, full_name FROM Spirits;')
        cursor = db.execute_query(db_connection=db_connection, query=spirit_query)
        spirit_data = cursor.fetchall()
        
        # query for getting method data to populate dropdown
        method_query = ('SELECT method_id, name FROM Methods;')
        cursor = db.execute_query(db_connection=db_connection, query=method_query)
        method_data = cursor.fetchall()

        return render_template('channelings.j2', chosen_seance=chosen_seance, channeling_data=channeling_data, 
                                seance_data=seance_data, medium_data=medium_data, spirit_data=spirit_data,
                         method_data=method_data)

@app.route('/delete_channeling/<int:id>')
def delete_channeling(id):
     # deletes a channeling based on id
    query = f'DELETE FROM Channelings WHERE channeling_id = {id};'
    cursor = db.execute_query(db_connection=db_connection, query=query)

    args = request.args
    if args.get('id') is not None:
        return redirect(f'/channelings?id={args.get("id")}')

    # otherwise redirect to all channelings page
    return redirect('/channelings')

 

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
            
            cursor = db.execute_query(db_connection=db_connection, query=query)
            
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

            cursor = db.execute_query(db_connection=db_connection, query=query)

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
            cursor = db.execute_query(db_connection=db_connection, query=preselect_query)
            location_to_edit = cursor.fetchone()
            
            # Removes 'None' from prefill--if a value is NULL, we get empty string instead
            for key, value in location_to_edit.items():
                if value is None:
                    location_to_edit[key] = ''


        # query for displaying all info about Locations in table
        query = ('SELECT location_id, name, street_address, city, zip, state, country '
                 'FROM Locations;')
        cursor = db.execute_query(db_connection=db_connection, query=query)
        location_data = cursor.fetchall()

        return render_template('locations.j2', location_data=location_data, location_to_edit=location_to_edit)

@app.route('/delete_location/<int:id>')
def delete_location(id):
    # removes the location with indicated id
    query = f'DELETE FROM Locations WHERE location_id = {id};'
    cursor = db.execute_query(db_connection=db_connection, query=query)
    
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

            cursor = db.execute_query(db_connection=db_connection, query=query)
            
            return redirect('/mediums')

        # otherwise if the POST form has name the insert form has been submitted
        # if name is empty we just skip the insert and redirect back to /mediums
        if request.form.get('name'):
            full_name_input = request.form['name'].strip()
            query = f'INSERT INTO Mediums (full_name) VALUES ("{full_name_input}");'
            cursor = db.execute_query(db_connection=db_connection, query=query)
            
        return redirect('/mediums')

    # displays table with all mediums
    if request.method == 'GET':
        args = request.args
        # if there is no medium to edit passed in in the get parameters we just leave medium_to_edit as None
        medium_to_edit = None
        # uses a select query to get info to preselect dropdown menu and prepopulate input
        if args.get('id'):
            preselect_query = f"SELECT medium_id, full_name FROM Mediums WHERE medium_id = {args.get('id')};"
            cursor = db.execute_query(db_connection=db_connection, query=preselect_query)
            medium_to_edit = cursor.fetchone()
            
        # main query for getting info for medium table
        query = 'SELECT medium_id, full_name FROM Mediums;'
        cursor = db.execute_query(db_connection=db_connection, query=query)
        medium_data = cursor.fetchall()

        return render_template('mediums.j2', medium_data=medium_data, medium_to_edit=medium_to_edit)
    
@app.route('/delete_medium/<int:id>')
def delete_medium(id):
    # deletes a medium based on id
    query = f'DELETE FROM Mediums WHERE medium_id = {id};'
    cursor = db.execute_query(db_connection=db_connection, query=query)
    
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

            cursor = db.execute_query(db_connection=db_connection, query=query)
            
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
            cursor = db.execute_query(db_connection=db_connection, query=query)
            
        return redirect('/methods')

    # Read functionality
    if request.method == 'GET':
        args = request.args
        # we might not have a preselected method in the query parameters, so default to None and adjust if necessary
        method_to_edit = None
        if args.get('id'):
            preselect_query = f"SELECT method_id, name, description FROM Methods WHERE method_id = {args.get('id')};"
            cursor = db.execute_query(db_connection=db_connection, query=preselect_query)
            method_to_edit = cursor.fetchone()
            
            # Remvoes 'None' from prefilled text input--if a value is NULL we just want an empty string
            for key, value in method_to_edit.items():
                if value is None:
                    method_to_edit[key] = ''
            
        query = 'SELECT method_id, name, description FROM Methods;'
        cursor = db.execute_query(db_connection=db_connection, query=query)
        method_data = cursor.fetchall()

        return render_template('methods.j2', method_data=method_data, method_to_edit=method_to_edit)
    

@app.route('/delete_method/<int:id>')
def delete_method(id):
    # removes method with associated method_id
    query = f'DELETE FROM Methods WHERE method_id = {id};'
    cursor = db.execute_query(db_connection=db_connection, query=query)
    
    return redirect('/methods')


@app.route('/seanceattendees', methods=['GET', 'POST'])
def seanceattendees():
    if request.method == 'POST':
        # if form contains update_seance_id we are updating a row in SeanceaAttendees
        if request.form.get('update_attendee_id'):
            attendee_id = request.form.get('update_attendee_id')
            seance_id = request.form.get('update_seance_id')
            old_seance_id = request.form.get('current_seance_id')
            
            # updates matching entries in SeanceAttendees
            query = ('UPDATE SeanceAttendees '
                    f'SET seance_id = {seance_id} '
                    f'WHERE attendee_id = {attendee_id} '
                    f'AND seance_id = {old_seance_id};')

            cursor = db.execute_query(db_connection=db_connection, query=query)

            return redirect(f'/seanceattendees?seance_id_input={old_seance_id}')

            
        # if form contains also_attended_id we are creating a new entry in SeanceAttendees
        if request.form.get('also_attended_id'):
            attendee_id = request.form.get('also_attended_id')
            seance_id = request.form.get('selected_seance_id')
            
            # inserts a new row into SeanceAttendees intersection table
            query = ('INSERT INTO SeanceAttendees (attendee_id, seance_id) '
                    f'VALUES ({attendee_id}, {seance_id});')
            cursor = db.execute_query(db_connection=db_connection, query=query)

            return redirect(f'/seanceattendees?seance_id_input={seance_id}')


    # read functionality
    if request.method == 'GET':
        args = request.args
        # chosen attendee defaults to None unless we have id passed in in GET args
        chosen_attendee_id = args.get('attendee_id_input')
        chosen_attendee = None
        # we are not supporting autofilling when attendee_id is NULL
        # there are potentially many entries where attendee_id is NULL, and it is hard to tell them apart
        if chosen_attendee_id is not None and chosen_attendee_id != 'None':
            chosen_attendee_query = f'SELECT attendee_id, full_name FROM Attendees WHERE attendee_id = {chosen_attendee_id}'
            cursor = db.execute_query(db_connection=db_connection, query=chosen_attendee_query)
            chosen_attendee = cursor.fetchone()

        # chosen seance defaults to None unless we have id passed in in GET args
        chosen_seance_id = args.get('seance_id_input')
        chosen_seance = None
        # if a seance_id has been passed in, get info about it
        if chosen_seance_id:
            chosen_seance_query = ('SELECT seance_id, Locations.name, Seances.date '
                                   'FROM Seances '
                                   'LEFT JOIN Locations ON Seances.location_id = Locations.location_id '
                                  f'WHERE Seances.seance_id = {chosen_seance_id}')
            cursor = db.execute_query(db_connection=db_connection, query=chosen_seance_query)
            chosen_seance = cursor.fetchone()
            
        # query for populating dropdown menu to choose a seance        
        seance_query = ('SELECT Seances.seance_id, Locations.name, Seances.date '
                       'FROM Seances '
                       'LEFT JOIN Locations ON Seances.location_id = Locations.location_id; ')
        cursor = db.execute_query(db_connection=db_connection, query=seance_query)
        seance_data = cursor.fetchall()
        
        # query for getting all seances that are not the selected seance
        other_seances = []
        if chosen_seance_id:
            other_seances_query = ('SELECT Seances.date, Locations.name, Seances.seance_id '
                                   'FROM Seances '
                                   'INNER JOIN Locations ON Seances.location_id = Locations.location_id '
                                  f'WHERE seance_id <> {chosen_seance_id};')
            cursor = db.execute_query(db_connection=db_connection, query=other_seances_query)
            other_seances = cursor.fetchall()


    
        # query for getting info about all attendees in the SeanceAttendees table for all seances or a particular one
        attendee_query = ('SELECT SeanceAttendees.seance_id, Attendees.attendee_id, Attendees.full_name, SeanceAttendees.seanceattendees_id '
                          'FROM SeanceAttendees '
                          'LEFT JOIN Attendees ON SeanceAttendees.attendee_id = Attendees.attendee_id')
        # add filter if we have chosen a seance
        if chosen_seance_id:
             attendee_query += f' WHERE SeanceAttendees.seance_id = {chosen_seance_id}'
        # needs a semicolon no matter what
        attendee_query += ';'
        
        cursor = db.execute_query(db_connection=db_connection, query=attendee_query)
        attendee_data = cursor.fetchall()
        
        # query for getting all attendees that did not attend the seance
        not_attended_list = []
        if chosen_seance_id:
            not_attended_query = ('SELECT Attendees.attendee_id, Attendees.full_name '
                              'FROM Attendees '
                              'WHERE attendee_id NOT IN ('
                              'SELECT Attendees.attendee_id '
                              'FROM Attendees '
                              'INNER JOIN SeanceAttendees ON Attendees.attendee_id = SeanceAttendees.attendee_id '
                             f'WHERE SeanceAttendees.seance_id = {chosen_seance_id});')
            cursor = db.execute_query(db_connection=db_connection, query=not_attended_query)
            not_attended_list = cursor.fetchall()

        # renders the page with prefilled dropdowns
        return render_template('seanceattendees.j2', chosen_seance=chosen_seance, seance_data=seance_data,
                               other_seances=other_seances, chosen_attendee=chosen_attendee,
                               attendee_data=attendee_data, not_attended_list=not_attended_list)

@app.route('/delete_seanceattendee/<int:id>')
def delete_seanceattendee(id):
     # deletes a seance attendence record based on id
    query = f'DELETE FROM SeanceAttendees WHERE seanceattendees_id = {id};'
    cursor = db.execute_query(db_connection=db_connection, query=query)

    args = request.args
    if args.get('seance_id_input') is not None:
        return redirect(f'/seanceattendees?seance_id_input={args.get("seance_id_input")}')

    # otherwise redirect to all seanceattendees page
    return redirect('/seanceattendees')


        


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
            
            cursor = db.execute_query(db_connection=db_connection, query=query)

            return redirect('/seances')

        # otherwise we are creating a new seance
        else:
            # process out empty strings and turn them into NULLs
            date_input = f'"{request.form["date"]}"' if request.form.get('date') else 'NULL'
            location_id_input = f'{request.form["location_id"]}' if request.form.get('location_id') else 'NULL'

            # query for creating a new Seance
            query = ('INSERT INTO Seances (date, location_id) '
                    f'VALUES ({date_input}, {location_id_input});')

            cursor = db.execute_query(db_connection=db_connection, query=query)

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
        cursor = db.execute_query(db_connection=db_connection, query=seance_query)
        seance_data = cursor.fetchall()

        # gets list of locations to populate dropdowns
        location_query = ("SELECT location_id, name FROM Locations;")
        cursor = db.execute_query(db_connection=db_connection, query=location_query)
        location_data = cursor.fetchall()
        return render_template('seances.j2', seance_data=seance_data, seance_to_edit=seance_to_edit, location_data=location_data)

@app.route('/delete_seance/<int:id>')
def delete_seance(id):
    # removes a seance by id
    query = f'DELETE FROM Seances WHERE seance_id = {id};'
    cursor = db.execute_query(db_connection=db_connection, query=query)
    
    return redirect('/seances')


@app.route('/spirits', methods=['GET', 'POST'])
def spirits():
    # if method is POST we are either Creating or Updating
    if request.method == 'POST':
        # if POST request has id_input we are updating
        if request.form.get('id_input') and request.form.get('new_name'):
            full_name_input = request.form['new_name'].strip()
            id_input = request.form['id_input']

            query = ('UPDATE Spirits ' 
                     f'SET full_name = "{full_name_input}" '
                     f'WHERE spirit_id = {id_input};')

            cursor = db.execute_query(db_connection=db_connection, query=query)
            
            return redirect('/spirits')

        # if POST request has name we are creating
        if request.form.get('name').strip() != '':
            full_name_input = request.form['name'].strip()
            query = f'INSERT INTO Spirits (full_name) VALUES ("{full_name_input}");'
            cursor = db.execute_query(db_connection=db_connection, query=query)
            
        return redirect('/spirits')

    # Read functionality
    if request.method == 'GET':
        args = request.args
        # sprit_to_edit defaults to None unless id is passed in Get params
        spirit_to_edit = None
        if args.get('id'):
            preselect_query = f"SELECT spirit_id, full_name FROM Spirits WHERE spirit_id = {args.get('id')};"
            cursor = db.execute_query(db_connection=db_connection, query=preselect_query)
            spirit_to_edit = cursor.fetchone()

        # gets info about all spirits in our db to display in table
        query = 'SELECT spirit_id, full_name FROM Spirits;'
        cursor = db.execute_query(db_connection=db_connection, query=query)
        spirit_data = cursor.fetchall()

        return render_template('spirits.j2', spirit_data=spirit_data, spirit_to_edit=spirit_to_edit)
    
@app.route('/delete_spirit/<int:id>')
def delete_spirit(id):
    # deletes spirit based on id
    query = f'DELETE FROM Spirits WHERE spirit_id = {id};'
    cursor = db.execute_query(db_connection=db_connection, query=query)
    
    return redirect('/spirits')



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5005))
    app.run(port=port, debug=True)