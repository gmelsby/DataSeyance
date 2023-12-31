# Author: Ed Wise and Greg Melsby
# Date:  6\4\2022

from flask import Blueprint, render_template, request
import database.db_connector as db
import toml
# our queries are read from here
queries = toml.load("models/queries.toml")
seances = Blueprint("seances", __name__, static_folder="static", template_folder="templates")


@seances.route('/seances', methods=['GET', 'POST'])
def seances_func():
    # method will be post or get, get will pass to line 55
    # initialize variable to tag record on row being updated
    seance_to_edit = -1
    if request.method == 'POST':
        # we had a post so we are going to look at a parameter passed from a hidden form value
        # get form values as dict
        content = request.form.to_dict()
        print(content)
        # this hidden form value will tell us what to do
        action = content['action']
        # hidden value says upddate
        if action == 'tagupdate':
            seance_to_edit = int(content['edit_form'])
            print('seance_to_edit', seance_to_edit)

        if action == 'update':
            # Change value to None if empty string passed in
            content['date'] = None if not content['date'] else content['date']
            content['name'] = None if not content['name'] else content['name']
            # get update query from toml and send it with parameters (see models/queries.toml)
            db.execute_query(queries['seances'][action]
                             , (content['date'], content['name'], content['seance_id'] ),
                             quantity="zero")
        # get insert query from toml and send it with parameter (see models/queries.toml)
        if action == 'insert':
            # Change value to None if empty string passed in
            content['date'] = None if not content['date'] else content['date']
            content['location_id'] = None if not content['location_id'] else content['location_id']

            db.execute_query(queries['seances'][action], (content['date'], content['location_id'],),
                             quantity="zero")

        # use delete query from toml to delete method of passed-in id
        if action == 'delete':
            db.execute_query(queries['seances'][action], (content['seance_id'],), quantity="zero")

        # gets list of seances to display in table and populate dropdowns
    seance_data = db.execute_query(queries['seances']['select'])

        # gets list of locations to populate dropdowns
    location_data = db.execute_query(queries['locations']['select_minimal'])
    return render_template('seances.j2', seance_data=seance_data, seance_to_edit=seance_to_edit
                           , location_data=location_data)

