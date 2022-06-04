# Author: Ed Wise and Greg Melsby
# Date:  6\4\2022

from flask import Blueprint, render_template, request
import database.db_connector as db
import toml
# our queries are read from here
queries = toml.load("models/queries.toml")
methods = Blueprint("methods", __name__, static_folder="static", template_folder="templates")

@methods.route('/methods', methods=['GET', 'POST'])
def methods_func():
    # method will be post or get, get will pass to line 40
    # initialize variable to tag record on row being updated
    method_to_edit = -1
    if request.method == 'POST':

        # we had a post so we are going to look at a parameter passed from a hidden form value
        # get form values as dict
        content = request.form.to_dict()
        # this hidden form value will tell us what to do
        action = content['action']
        # hidden value says tagupddate
        if action == 'tagupdate':
            method_to_edit = int(content['method_id'])

        if action == 'update' and content.get('name').strip():
            # get update query from toml and send it with parameters (see models/queries.toml)
            db.execute_query(queries['methods'][action]
                             , (content['name'].strip(), content['description'].strip() ,int(content['method_id'])), quantity="zero")
        # get insert query from toml and send it with parameter (see models/queries.toml)
        if action == 'insert' and content.get('name').strip():
            db.execute_query(queries['methods'][action], (content['name'].strip(), content['description'].strip(),), quantity="zero")

        # use delete query from toml to delete method of passed-in id
        if action == 'delete':
            db.execute_query(queries['methods'][action], (content['method_id'],), quantity="zero")

    method_data = db.execute_query(queries['methods']['select_detailed'])


    return render_template('methods.j2', method_data=method_data, method_to_edit=method_to_edit)
