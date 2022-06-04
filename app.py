# Citation for following file
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
    edit_form = -1

    # we had a post so we are going to look at a parameter passed from a hidden form value
    # get form values as dict

    if request.method == 'POST':

        content = request.form.to_dict()
        # this hidden form value will tell us what to do
        action = content['action']

        # We do not want Attendees with empty names
        if action == 'insert' and content.get('insert_full_name').strip():
            # our one multi-query transaction
            # we need to call execute_queries to have all modifications executed as one
            # and pass in lists of queries and parameters
            if content.get('seance_id'):
                db.execute_queries(queries['attendees']['insert'], [(content['insert_full_name'],), (), content['seance_id']])
            # insert attendee who has not attended a seance yet
            else:
                db.execute_query(queries['attendees']['insert_inline'], (content['insert_full_name'],), quantity="none")


        if action == 'delete':
            db.execute_query(queries['attendees'][action], (content['attendee_id'],), quantity="none")


        if action == 'update':
            full_name_input = request.form['new_name'].strip()
            id_input = request.form['id_input']
            db.execute_query(queries['attendees'][action], (full_name_input, int(id_input)), quantity="none")

        if action == 'tagupdate':
            edit_form = int(content['id_input'])
            
    # displays the table of all attendees
    # if request.method == 'GET':
    args = request.args
    # we could potentially ahve no get query parameters, so attendee_to_edit starts as None
    attendee_to_edit = None
    # if we have get query parameter indicating attendee_id we get the info for the dropdown
    if args.get('id'):
        attendee_to_edit = db.execute_query(queries['attendees']['select_specific'], (int(args.get('id')),), quantity="one")


    # attendee data to be displayed in table and used for insert and update dropdown dropdown
    attendee_data = db.execute_query(queries['attendees']['select'])


    # seance data to be used in dropdown for adding an attendee
    seance_data = db.execute_query(queries['seances']['select'])

    return render_template('attendees.j2', attendee_data=attendee_data, seance_data=seance_data
                           , attendee_to_edit=attendee_to_edit, edit_form=edit_form)





@app.route('/channelings', methods=['GET', 'POST'])
def channelings():
    channeling_query = queries['channelings']['select']
    channeling_params = ()
    channeling_id_to_edit = -1
    chosen_seance = None
    if request.method == 'POST':
        content = request.form.to_dict()
        print(content)
        action = content['action']
        for key, value in content.items():
            if key == 'action':
                continue
            if not value:
                content[key] = None
            else:
                content[key] = int(value)

        if action == 'insert':
            db.execute_query(queries['channelings'][action], (
             content['medium_id'],
             content['spirit_id'],
             content['method_id'],
             content['seance_date'],
             content['is_successful'],
             content['length_in_minutes']
            ), quantity="none")

        if action == 'delete':
            db.execute_query(queries['channelings'][action], 
            (int(content['channeling_id']),), quantity="none")

        if action == 'tagupdate':
            channeling_id_to_edit = int(content['channeling_id'])

        if action == 'update':
            db.execute_query(queries['channelings'][action], (
             content['medium_id'],
             content['spirit_id'],
             content['method_id'],
             content['seance_id'],
             content['is_successful'],
             content['length_in_minutes'],
             content['id_input']
            ), quantity="none")

    # use args if request.method is "POST" OR "GET"--useful for linking from other pages
    if request.args.get('chosen_seance_id'): 
        channeling_query = queries['channelings']['select_specific']
        channeling_params = (int(request.args['chosen_seance_id']),)
        chosen_seance = db.execute_query(queries['seances']['select_specific'], channeling_params, quantity="one")


    # query for getting seance data to populate dropdown
    seance_data = db.execute_query(queries['seances']['select'])

    
    # queryfor getting location data to populate add seance dropdown
    location_data = db.execute_query(queries['locations']['select'])


    # query for getting medium data to populate dropdown
    medium_data = db.execute_query(queries['mediums']['select'])


    # query for getting spirit data to populate dropdown
    spirit_data = db.execute_query(queries['spirits']['select'])


    # query for getting method data to populate dropdown
    method_data = db.execute_query(queries['methods']['select'])


    channeling_data = db.execute_query(channeling_query, channeling_params)

    return render_template('channelings.j2', channeling_id_to_edit=channeling_id_to_edit, chosen_seance=chosen_seance, channeling_data=channeling_data,
                            seance_data=seance_data, medium_data=medium_data, spirit_data=spirit_data,
                            method_data=method_data, location_data=location_data)



@app.route('/locations', methods=['GET', 'POST'])
def locations():
    channeling_params = ()
    location_to_edit = -1
    if request.method == 'POST':
        content = request.form.to_dict()
        print(content)
        action = content['action']
        for key, value in content.items():
            if key == 'action':
                continue
            if not value:
                content[key] = None
            else:
                content[key] = value

        if action == 'insert':

            db.execute_query(queries['locations'][action], (
                content['location_name'],
                content['street_address'],
                content['city'],
                content['zip'],
                content['state'],
                content['country']
            ), quantity="none")

        if action == 'delete':
            db.execute_query(queries['locations'][action], (
                int(content['location_id']),), quantity="none")

        if action == 'tagupdate':
            location_to_edit = int(content['location_id'])

        if action == 'update':
            db.execute_query(queries['locations'][action], (
                content['location_name'],
                content['street_address'],
                content['city'],
                content['zip'],
                content['state'],
                content['country'],
                int(content['location_id'])
            ), quantity="none")

        # query for displaying all info about Locations in table
    location_data = db.execute_query(queries['locations']['select'])


    return render_template('locations.j2', location_data=location_data, location_to_edit=location_to_edit)



@app.route('/mediums', methods=['GET', 'POST'])
def mediums():
    # method will be post or get, get will pass to line 468
    medium_to_edit = -1
    if request.method == 'POST':

        # we had a post so we are going to look at a parameter passed from a hidden form value
        # get form values as dict
        content = request.form.to_dict()
        # this hidden form value will tell us what to do
        action = content['action']
        #hidden value says upddate
        if action == 'tagupdate':
           medium_to_edit = int(content['medium_id'])

        # only update if replacement name is nonempty
        if action == 'update' and content.get('full_name').strip():
            #get update query from toml and send it with parameters (see /home/ed/DataSeyance/models/queries.toml)
            db.execute_query(queries['mediums'][action]
                             , (content['full_name'].strip(), int(content['medium_id'])), quantity="none")
        # get insert query from toml and send it with parameter (see /home/ed/DataSeyance/models/queries.toml)
        # only allow insertion if string is nonempty
        if action == 'insert' and content.get('full_name').strip():
            db.execute_query(queries['mediums'][action], (content['full_name'].strip(),), quantity="none")

        if action == 'delete':
            db.execute_query(queries['mediums'][action], (content['medium_id'],), quantity="none")

    medium_data = db.execute_query(queries['mediums']['select'])


    return render_template('mediums.j2', medium_data=medium_data, medium_to_edit=medium_to_edit)
    

@app.route('/methods', methods=['GET', 'POST'])
def methods():
    method_to_edit = -1
    if request.method == 'POST':

        # we had a post so we are going to look at a parameter passed from a hidden form value
        # get form values as dict
        content = request.form.to_dict()
        # this hidden form value will tell us what to do
        action = content['action']
        # hidden value says upddate
        if action == 'tagupdate':
            method_to_edit = int(content['method_id'])

        if action == 'update' and content.get('name').strip():
            # get update query from toml and send it with parameters (see /home/ed/DataSeyance/models/queries.toml)
            db.execute_query(queries['methods'][action]
                             , (content['name'].strip(), content['description'].strip() ,int(content['method_id'])), quantity="none")
        # get insert query from toml and send it with parameter (see /home/ed/DataSeyance/models/queries.toml)
        if action == 'insert' and content.get('name').strip():
            db.execute_query(queries['methods'][action], (content['name'].strip(), content['description'].strip(),), quantity="none")

        # use delete query from toml to delete method of passed-in id
        if action == 'delete':
            db.execute_query(queries['methods'][action], (content['method_id'],), quantity="none")

    method_data = db.execute_query(queries['methods']['select_detailed'])


    return render_template('methods.j2', method_data=method_data, method_to_edit=method_to_edit)


@app.route('/seanceattendees', methods=['GET', 'POST'])
def seanceattendees():
    seanceattendees_id_to_edit = -1
    seanceattendees_to_edit = None
    if request.method == 'POST':
        content = request.form.to_dict()
        action = content['action']

        if content['action'] == 'insert':

            db.execute_query(queries['seanceattendees'][action], (
                int(content['attendee_id']),
                int(content['seance_id']),
            ), quantity="none")


        if content['action'] == 'delete':
            db.execute_query(queries['seanceattendees'][action], (
                int(content['seanceattendees_id']),
            ), quantity="none")



        if content['action'] == 'tagupdate':
            seanceattendees_id_to_edit = int(content['seanceattendees_id_to_edit'])
            seanceattendees_to_edit = db.execute_query(queries['seanceattendees']['inline_tag']
                                      ,  (seanceattendees_id_to_edit,), quantity="one")



        if content['action'] == 'update':
            db.execute_query(queries['seanceattendees']['inline_update'], (
                int(content['seance_id']),
                int(content['attendee_id']),
                int(content['seanceattendees_id']),
            ), quantity="none")



    args = request.args
    # chosen attendee defaults to None unless we have id passed in in GET args
    chosen_attendee_id = args.get('attendee_id_input')
    chosen_attendee = None
    # we are not supporting autofilling when attendee_id is NULL
    # there are potentially many entries where attendee_id is NULL, and it is hard to tell them apart
    if chosen_attendee_id is not None:
        chosen_attendee = db.execute_query(queries['attendees']['select_specific'], (int(chosen_attendee_id),), quantity="one")


    # chosen seance defaults to None unless we have id passed in in GET args
    chosen_seance_id = args.get('seance_id_input')
    chosen_seance = None
    # if a seance_id has been passed in, get info about it
    if chosen_seance_id:
        chosen_seance = db.execute_query(queries['seances']['select_specific'], (int(chosen_seance_id),), quantity="one")


    # query for populating dropdown menu to choose a seance
    seance_data = db.execute_query(queries['seances']['select'])


    # query for getting info about all attendees in our database
    all_attendees_query = queries['attendees']['select']
    all_attendees = db.execute_query(all_attendees_query)


    attendee_query = queries['seanceattendees']['select']
    
    attendee_params = ()
    if chosen_seance_id:
         attendee_query = queries['seanceattendees']['select_specific']
         attendee_params = (int(chosen_seance_id),)

    attendee_data = db.execute_query(query=attendee_query, query_params=attendee_params)

    # renders the page with prefilled dropdowns
    return render_template('seanceattendees.j2', chosen_seance=chosen_seance, seance_data=seance_data,
                           chosen_attendee=chosen_attendee,
                           attendee_data=attendee_data,
                           all_attendees=all_attendees,
                           seanceattendees_id_to_edit=seanceattendees_id_to_edit,
                           seanceattendees_to_edit=seanceattendees_to_edit)



@app.route('/seances', methods=['GET', 'POST'])
def seances():
    if request.method == 'POST':
        # if form has id_input we are updating
        if request.form.get('id_input'):
            # if any input is empty string we want it to be NULL instead
            id_input = request.form['id_input']
            date_input = f'{request.form["new_date"]}' if request.form.get('new_date') else None
            location_id_input = f'{request.form["new_location_id"]}' if request.form.get('new_location_id') else None

            # query for updating seance with matching id
            db.execute_query(queries['seances']['update'], (date_input, location_id_input, id_input))
            return redirect('/seances')

        # otherwise we are creating a new seance
        else:
            # process out empty strings and turn them into NULLs
            date_input = f'{request.form["date"]}' if request.form.get('date') else None
            location_id_input = f'{request.form["location_id"]}' if request.form.get('location_id') else None

            # query for creating a new Seance
            db.execute_query(queries['seances']['insert'], (date_input, location_id_input))
            return redirect('/seances')

    # Read functionality
    if request.method == 'GET':
        args = request.args
        # there may not be a passed-in seance id to edit--default to None and adjusts if needed
        seance_to_edit = None
        if args.get('id'):
            seance_to_edit = db.execute_query(queries['seances']['select_specific'], (int(args.get('id')),))


        # gets list of seances to display in table and populate dropdowns
        seance_data = db.execute_query(queries['seances']['select'])

        # gets list of locations to populate dropdowns
        location_data = db.execute_query(queries['locations']['select_minimal'])
        return render_template('seances.j2', seance_data=seance_data, seance_to_edit=seance_to_edit, location_data=location_data)

@app.route('/delete_seance/<int:id>')
def delete_seance(id):
    # removes a seance by id
    db.execute_query(queries['seances']['delete'], (int(id),))
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

        if action == 'update' and content.get('new_name').strip():
            #get update query from toml and send it with parameters (see /home/ed/DataSeyance/models/queries.toml)
            print(int(content['id_input']))
            db.execute_query(queries['spirits'][action]
                             , (content['new_name'].strip(), int(content['id_input'])))
        # get insert query from toml and send it with parameter (see /home/ed/DataSeyance/models/queries.toml)
        # only allow insertion if name is nonempty
        if action == 'insert' and content.get('insert_full_name').strip():
            db.execute_query(queries['spirits'][action], (content['insert_full_name'].strip(),))

        if action == 'delete':
            db.execute_query(queries['spirits'][action], (content['spirit_id'],))

    spirit_data = db.execute_query(queries['spirits']['select'])

    return render_template('spirits.j2', spirit_data=spirit_data,  edit_form=edit_form)



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3023))
    app.run(port=port, debug=True)
