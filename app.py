#rams=() Citation for following file
# Date: 5/19/2022
# Routing inspired/guided by CS340 Flask Starter App
# URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py

from flask import Flask, render_template, redirect, json, request
from flask_mysqldb import MySQL
import os
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

            cursor = db.execute_query(queries['attendees']['update'], (full_name_input, int(id_input)))

            return redirect('/attendees')

        # otherwise we are inserting a new Attendee
        # We do not want Attendees with empty names
        if request.form.get('name'):
            # our one multi-query transaction
            # we need to call execute_queries to have all modifications executed as one
            # and pass in lists of queries and parameters
            cursor = db.execute_queries(queries['attendees']['insert'], [(request.form.get('name'),), (), (request.form.get('seance_id'),)])
        return redirect('/attendees')
            
            
    # displays the table of all attendees
    if request.method == 'GET':
        args = request.args
        # we could potentially ahve no get query parameters, so attendee_to_edit starts as None
        attendee_to_edit = None
        # if we have get query parameter indicating attendee_id we get the info for the dropdown
        if args.get('id'):
            cursor = db.execute_query(queries['attendees']['select_specific'], (int(args.get('id')),))
            attendee_to_edit = cursor.fetchone()
            
        # attendee data to be displayed in table and used for update dropdown
        cursor = db.execute_query(queries['attendees']['select'])
        attendee_data = cursor.fetchall()
        
        # seance data to be used in dropdown for adding an attendee
        cursor = db.execute_query(queries['seances']['select'])
        seance_data = cursor.fetchall()

        return render_template('attendees.j2', attendee_data=attendee_data, seance_data=seance_data, attendee_to_edit=attendee_to_edit)
    

@app.route('/delete_attendee/<int:id>')
def delete_attendee(id):
    query = queries['attendees']['delete']
    cursor = db.execute_query(query, (id,))

    
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
        cursor = db.execute_query(queries['seances']['select_specific'], (int(chosen_seance_id),))
        chosen_seance = cursor.fetchone()


        # query for getting all relevant channeling data
    channeling_query = queries['channelings']['select']
    channeling_params = ()
            # add a filter if a seance_id has been chosen
    if chosen_seance_id:
        channeling_query = queries['channelings']['select_specific']
        channeling_params = (int(chosen_seance_id),)

    cursor = db.execute_query(channeling_query, channeling_params)
    channeling_data = cursor.fetchall()

    # query for getting seance data to populate dropdown
    cursor = db.execute_query(queries['seances']['select'])
    seance_data = cursor.fetchall()

    # query for getting medium data to populate dropdown
    cursor = db.execute_query(queries['mediums']['select'])
    medium_data = cursor.fetchall()

    # query for getting spirit data to populate dropdown
    cursor = db.execute_query(queries['spirits']['select'])
    spirit_data = cursor.fetchall()

    # query for getting method data to populate dropdown
    cursor = db.execute_query(queries['methods']['select'])
    method_data = cursor.fetchall()

    return render_template('channelings.j2', chosen_seance=chosen_seance, channeling_data=channeling_data,
                            seance_data=seance_data, medium_data=medium_data, spirit_data=spirit_data,
                            method_data=method_data)




@app.route('/locations', methods=['GET', 'POST'])
def locations():
    if request.method == 'POST':
        # if POST form has id_input, update form has been submitted
        if request.form.get('id_input'):
            # Process each input to be NULL if empty string
            # execute_query turns None into NULL through cursor.execute
            id_input = request.form['id_input']
            name_input = f'{request.form["new_name"].strip()}' if request.form.get('new_name').strip() != '' else None
            street_input = f'{request.form["new_street_address"].strip()}' if request.form.get('new_street_address').strip() != '' else None
            city_input = f'{request.form["new_city"].strip()}' if request.form.get('new_city').strip() != '' else None
            zip_input = f'{request.form["new_zip"]}' if request.form.get('new_zip') else None
            state_input = f'{request.form["new_state"]}' if request.form.get('new_state') else None
            country_input = f'{request.form["new_country"].strip()}' if request.form.get('new_country').strip() != '' else None
            
            # query for updating location with location_id id_input
            cursor = db.execute_query(queries['locations']['update'], (name_input, street_input, city_input, zip_input, state_input, country_input, id_input))

            
            return redirect('/locations')

        # if POST form has name, create form has been submitted
        if request.form.get('name') is not None:
            # Process each input to be NULL if empty string
            name_input = f'{request.form["name"].strip()}' if request.form.get('name').strip() != '' else None
            street_input = f'{request.form["street_address"].strip()}' if request.form.get('street_address').strip() != '' else None
            city_input = f'{request.form["city"].strip()}' if request.form.get('city').strip() != '' else None
            zip_input = f'{request.form["zip"]}' if request.form.get('zip') else None
            state_input =f'{request.form["state"]}' if request.form.get('state') else None
            country_input = f'{request.form["country"].strip()}' if request.form.get('country') != '' else None
            
            # query for making new location
            cursor = db.execute_query(queries['locations']['insert'], (name_input, street_input, city_input, zip_input, state_input, country_input))


            return redirect('/locations')

        return redirect('/locations')


    # Read functionality
    if request.method == 'GET':
        args = request.args
        # only have a location to edit if id passed in in GET params, othewise it's None
        location_to_edit = None
        if args.get('id'):
            cursor = db.execute_query(queries['locations']['select_specific'], (int(args.get('id')),))
            location_to_edit = cursor.fetchone()
            
            # Removes 'None' from prefill--if a value is NULL, we get empty string instead
            for key, value in location_to_edit.items():
                if value is None:
                    location_to_edit[key] = ''


        # query for displaying all info about Locations in table
        cursor = db.execute_query(queries['locations']['select'])
        location_data = cursor.fetchall()

        return render_template('locations.j2', location_data=location_data, location_to_edit=location_to_edit)

@app.route('/delete_location/<int:id>')
def delete_location(id):
    # removes the location with indicated id
    cursor = db.execute_query(queries['locations']['delete'], (int(id),))
    return redirect('/locations')


@app.route('/mediums', methods=['GET', 'POST'])
def mediums():
    if request.method == 'POST':
        # if the POST form has id_input the update form has been submitted
        # We only want to update if the name is nonempty
        if request.form.get('id_input') and request.form.get('new_name'):
            full_name_input = request.form['new_name'].strip()
            id_input = request.form['id_input']

            cursor = db.execute_query(queries['mediums']['update'], (full_name_input, int(id_input)))
            return redirect('/mediums')

        # otherwise if the POST form has name the insert form has been submitted
        # if name is empty we just skip the insert and redirect back to /mediums
        if request.form.get('name'):
            full_name_input = request.form['name'].strip()
            cursor = db.execute_query(queries['mediums']['insert'], (full_name_input,))
            
        return redirect('/mediums')

    # displays table with all mediums
    if request.method == 'GET':
        args = request.args
        # if there is no medium to edit passed in in the get parameters we just leave medium_to_edit as None
        medium_to_edit = None
        # uses a select query to get info to preselect dropdown menu and prepopulate input
        if args.get('id'):
            cursor = db.execute_query(queries['mediums']['select_specific'], (int(id),))
            medium_to_edit = cursor.fetchone()
            
        # main query for getting info for medium table
        cursor = db.execute_query(queries['mediums']['select'])
        medium_data = cursor.fetchall()

        return render_template('mediums.j2', medium_data=medium_data, medium_to_edit=medium_to_edit)
    
@app.route('/delete_medium/<int:id>')
def delete_medium(id):
    # deletes a medium based on id
    cursor = db.execute_query(queries['mediums']['delete'], (int(id),))
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

            cursor = db.execute_query(query=query)

            return redirect(f'/seanceattendees?seance_id_input={old_seance_id}')

            
        # if form contains also_attended_id we are creating a new entry in SeanceAttendees
        if request.form.get('also_attended_id'):
            attendee_id = request.form.get('also_attended_id')
            seance_id = request.form.get('selected_seance_id')
            
            # inserts a new row into SeanceAttendees intersection table
            query = ('INSERT INTO SeanceAttendees (attendee_id, seance_id) '
                    f'VALUES ({attendee_id}, {seance_id});')
            cursor = db.execute_query(query=query)

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
            cursor = db.execute_query(query=chosen_attendee_query)
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
            cursor = db.execute_query(query=chosen_seance_query)
            chosen_seance = cursor.fetchone()
            
        # query for populating dropdown menu to choose a seance        
        seance_query = ('SELECT Seances.seance_id, Locations.name, Seances.date '
                       'FROM Seances '
                       'LEFT JOIN Locations ON Seances.location_id = Locations.location_id; ')
        cursor = db.execute_query(query=seance_query)
        seance_data = cursor.fetchall()
        
        # query for getting all seances that are not the selected seance
        other_seances = []
        if chosen_seance_id:
            other_seances_query = ('SELECT Seances.date, Locations.name, Seances.seance_id '
                                   'FROM Seances '
                                   'INNER JOIN Locations ON Seances.location_id = Locations.location_id '
                                  f'WHERE seance_id <> {chosen_seance_id};')
            cursor = db.execute_query(query=other_seances_query)
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
        
        cursor = db.execute_query(query=attendee_query)
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
            cursor = db.execute_query(query=not_attended_query)
            not_attended_list = cursor.fetchall()

        # renders the page with prefilled dropdowns
        return render_template('seanceattendees.j2', chosen_seance=chosen_seance, seance_data=seance_data,
                               other_seances=other_seances, chosen_attendee=chosen_attendee,
                               attendee_data=attendee_data, not_attended_list=not_attended_list)

@app.route('/delete_seanceattendee/<int:id>')
def delete_seanceattendee(id):
     # deletes a seance attendence record based on id
    query = f'DELETE FROM SeanceAttendees WHERE seanceattendees_id = {id};'
    cursor = db.execute_query(query=query)

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
            

            cursor = db.execute_query(query=query)


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
            cursor = db.execute_query(query=preselect_query)
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
    port = int(os.environ.get('PORT', 3023))
    app.run(port=port)
