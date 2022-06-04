# Author: Ed Wise
# Date: 
# Description:
from flask import Blueprint, render_template, request
import database.db_connector as db
import toml

queries = toml.load("models/queries.toml")
attendees = Blueprint("attendees", __name__, static_folder="static", template_folder="templates")


@attendees.route('/attendees', methods=['GET', 'POST'])
def attendees_func():
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
                db.execute_queries(queries['attendees']['insert'],
                                   [(content['insert_full_name'],), (), content['seance_id']])
            # insert attendee who has not attended a seance yet
            else:
                db.execute_query(queries['attendees']['insert_inline'], (content['insert_full_name'],), quantity="zero")

        if action == 'delete':
            db.execute_query(queries['attendees'][action], (content['attendee_id'],), quantity="zero")

        if action == 'update':
            full_name_input = request.form['new_name'].strip()
            id_input = request.form['id_input']
            db.execute_query(queries['attendees'][action], (full_name_input, int(id_input)), quantity="zero")

        if action == 'tagupdate':
            edit_form = int(content['id_input'])

    # displays the table of all attendees
    # if request.method == 'GET':
    args = request.args
    # we could potentially ahve no get query parameters, so attendee_to_edit starts as None
    attendee_to_edit = None
    # if we have get query parameter indicating attendee_id we get the info for the dropdown
    if args.get('id'):
        attendee_to_edit = db.execute_query(queries['attendees']['select_specific'], (int(args.get('id')),),
                                            quantity="one")

    # attendee data to be displayed in table and used for insert and update dropdown dropdown
    attendee_data = db.execute_query(queries['attendees']['select'])

    # seance data to be used in dropdown for adding an attendee
    seance_data = db.execute_query(queries['seances']['select'])

    return render_template('attendees.j2', attendee_data=attendee_data, seance_data=seance_data
                           , attendee_to_edit=attendee_to_edit, edit_form=edit_form)