# Author: Ed Wise and Greg Melsby
# Date:  6\4\2022

from flask import Blueprint, render_template, request
import database.db_connector as db
import toml
# our queries are read from here
queries = toml.load("models/queries.toml")
channelings = Blueprint("channelings", __name__, static_folder="static", template_folder="templates")


@channelings.route('/channelings', methods=['GET', 'POST'])
def channelings_func():
    channeling_query = queries['channelings']['select']
    channeling_params = ()
    # used to tag record on line to be edited
    channeling_id_to_edit = -1
    chosen_seance = None

    # we had a post so we are going to look at a parameter passed from a hidden form value
    # get form values as dict

    if request.method == 'POST':
        content = request.form.to_dict()

        # this hidden form value will tell us what to do

        # we do not get an action tag if we nav from seance button to channelings here so we handle that here.
        if 'action' in content.keys():
            action = content['action']
        else:
            action = None

        for key, value in content.items():
            if key == 'action':
                continue
            if not value:
                content[key] = None
            else:
                content[key] = int(value)
        # read and execute action
        if action == 'insert':
            db.execute_query(queries['channelings'][action], (
                content['medium_id'],
                content['spirit_id'],
                content['method_id'],
                content['seance_date'],
                content['is_successful'],
                content['length_in_minutes']
            ), quantity="zero")
        # read and execute action
        if action == 'delete':
            db.execute_query(queries['channelings'][action],
                             (int(content['channeling_id']),), quantity="zero")
        # read and execute action
        if action == 'tagupdate':
            channeling_id_to_edit = int(content['channeling_id'])
        # read and execute action
        if action == 'update':
            db.execute_query(queries['channelings'][action], (
                content['medium_id'],
                content['spirit_id'],
                content['method_id'],
                content['seance_id'],
                content['is_successful'],
                content['length_in_minutes'],
                content['id_input']
            ), quantity="zero")

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

    return render_template('channelings.j2', channeling_id_to_edit=channeling_id_to_edit, chosen_seance=chosen_seance,
                           channeling_data=channeling_data,
                           seance_data=seance_data, medium_data=medium_data, spirit_data=spirit_data,
                           method_data=method_data, location_data=location_data)
