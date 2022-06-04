# Author: Ed Wise
# Date: 
# Description:
from flask import Blueprint, render_template, request
import database.db_connector as db
import toml

queries = toml.load("models/queries.toml")
mediums = Blueprint("mediums", __name__, static_folder="static", template_folder="templates")


@mediums.route('/mediums', methods=['GET', 'POST'])
def mediums_func():
    # method will be post or get, get will pass to line 468
    medium_to_edit = -1
    if request.method == 'POST':

        # we had a post so we are going to look at a parameter passed from a hidden form value
        # get form values as dict
        content = request.form.to_dict()
        # this hidden form value will tell us what to do
        action = content['action']
        # hidden value says upddate
        if action == 'tagupdate':
            medium_to_edit = int(content['medium_id'])

        # only update if replacement name is nonempty
        if action == 'update' and content.get('full_name').strip():
            # get update query from toml and send it with parameters (see /home/ed/DataSeyance/models/queries.toml)
            db.execute_query(queries['mediums'][action]
                             , (content['full_name'].strip(), int(content['medium_id'])), quantity="zero")
        # get insert query from toml and send it with parameter (see /home/ed/DataSeyance/models/queries.toml)
        # only allow insertion if string is nonempty
        if action == 'insert' and content.get('full_name').strip():
            db.execute_query(queries['mediums'][action], (content['full_name'].strip(),), quantity="zero")

        if action == 'delete':
            db.execute_query(queries['mediums'][action], (content['medium_id'],), quantity="zero")

    medium_data = db.execute_query(queries['mediums']['select'])

    return render_template('mediums.j2', medium_data=medium_data, medium_to_edit=medium_to_edit)
