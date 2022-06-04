# Author: Ed Wise
# Date: 
# Description:
from flask import Blueprint, render_template, request
import database.db_connector as db
import toml

queries = toml.load("models/queries.toml")
locations = Blueprint("locations", __name__, static_folder="static", template_folder="templates")


@locations.route('/locations', methods=['GET', 'POST'])
def locations_func():
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
            ), quantity="zero")

        if action == 'delete':
            db.execute_query(queries['locations'][action], (
                int(content['location_id']),), quantity="zero")

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
            ), quantity="zero")

        # query for displaying all info about Locations in table
    location_data = db.execute_query(queries['locations']['select'])


    return render_template('locations.j2', location_data=location_data, location_to_edit=location_to_edit)
