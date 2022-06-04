# Author: Ed Wise and Greg Melsby
# Date:  6\4\2022

from flask import Blueprint, render_template, request, flash
import database.db_connector as db
import toml

# our queries are read from here
queries = toml.load("models/queries.toml")
seanceattendees = Blueprint("seanceattendees", __name__, static_folder="static", template_folder="templates")


@seanceattendees.route('/seanceattendees', methods=['GET', 'POST'])
def seanceattendees_func():
    # get this query early becasue we want to look at existing records in our insert and not insert duplicate records
    attendee_query = queries['seanceattendees']['select']
    # initialize variable to tag record on row being updated
    seanceattendees_id_to_edit = -1
    seanceattendees_to_edit = None
    duplicate_event = False
    if request.method == 'POST':

        content = request.form.to_dict()

        # we do not get an action tag if we nav from seance button to attendees here so we handle that here.
        if 'action' in content.keys():
            action = content['action']
        else:
            content['action'] = None

        if content['action'] == 'insert':

            # get existing records
            attendee_data = db.execute_query(query=attendee_query)
            attendee_records = [(record['attendee_id'], record['seance_id']) for record in attendee_data]

            # see if requested insert already exists
            if (int(content['attendee_id']),int(content['seance_id'])) in attendee_records:
                # if so this variable will alert user that the record exists and not insert dupe
                duplicate_event = True
            else:
                db.execute_query(queries['seanceattendees'][action], (
                    int(content['attendee_id']),
                    int(content['seance_id']),
                ), quantity="zero")

        if content['action'] == 'delete':
            db.execute_query(queries['seanceattendees'][action], (
                int(content['seanceattendees_id']),
            ), quantity="zero")

        if content['action'] == 'tagupdate':
            seanceattendees_id_to_edit = int(content['seanceattendees_id_to_edit'])
            seanceattendees_to_edit = db.execute_query(queries['seanceattendees']['inline_tag']
                                                       , (seanceattendees_id_to_edit,), quantity="one")

        if content['action'] == 'update':

            attendee_data = db.execute_query(query=attendee_query)
            attendee_records = [(record['attendee_id'], record['seance_id']) for record in attendee_data]

            # see if requested insert already exists
            if (int(content['attendee_id']),int(content['seance_id'])) in attendee_records:
                # if so this variable will alert user that the record exists and not insert dupe
                duplicate_event = True
            else:

                db.execute_query(queries['seanceattendees']['inline_update'], (
                    int(content['seance_id']),
                    int(content['attendee_id']),
                    int(content['seanceattendees_id']),
                ), quantity="zero")

    args = request.args
    # chosen attendee defaults to None unless we have id passed in in GET args
    chosen_attendee_id = args.get('attendee_id_input')
    chosen_attendee = None
    # we are not supporting autofilling when attendee_id is NULL
    # there are potentially many entries where attendee_id is NULL, and it is hard to tell them apart
    if chosen_attendee_id is not None:
        chosen_attendee = db.execute_query(queries['attendees']['select_specific'], (int(chosen_attendee_id),),
                                           quantity="one")

    # chosen seance defaults to None unless we have id passed in in GET args
    chosen_seance_id = args.get('seance_id_input')
    chosen_seance = None
    # if a seance_id has been passed in, get info about it
    if chosen_seance_id:
        chosen_seance = db.execute_query(queries['seances']['select_specific'], (int(chosen_seance_id),),
                                         quantity="one")

    # query for populating dropdown menu to choose a seance
    seance_data = db.execute_query(queries['seances']['select'])

    # query for getting info about all attendees in our database
    all_attendees_query = queries['attendees']['select']
    all_attendees = db.execute_query(all_attendees_query)



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
                           seanceattendees_to_edit=seanceattendees_to_edit, duplicate_event=duplicate_event)
