# Author: Ed Wise and Greg Melsby
# Date:  6\4\2022

from flask import Blueprint, render_template, request
import database.db_connector as db
import toml
# our queries are read from here
queries = toml.load("models/queries.toml")
spirits = Blueprint("spirits", __name__, static_folder="static", template_folder="templates")

@spirits.route('/spirits', methods=['GET', 'POST'])
def spirits_func():
    # method will be post or get, get will pass to line 40
    # initialize variable to tag record on row being updated
    edit_form = -1
    if request.method == 'POST':

        # we had a post so we are going to look at a parameter passed from a hidden form value
        # get form values as dict
        content = request.form.to_dict()
        # this hidden form value will tell us what to do
        action = content['action']
        #hidden value says tagupdate
        if action == 'tagupdate':
           edit_form = int(content['id_input'])

        if action == 'update' and content.get('new_name').strip():
            #get update query from toml and send it with parameters (see models/queries.toml)
            print(int(content['id_input']))
            db.execute_query(queries['spirits'][action]
                             , (content['new_name'].strip(), int(content['id_input'])), quantity="zero")
        # get insert query from toml and send it with parameter (see models/queries.toml)
        # only allow insertion if name is nonempty
        if action == 'insert' and content.get('insert_full_name').strip():
            db.execute_query(queries['spirits'][action], (content['insert_full_name'].strip(),), quantity="zero")

        if action == 'delete':
            db.execute_query(queries['spirits'][action], (content['spirit_id'],), quantity="zero")

    spirit_data = db.execute_query(queries['spirits']['select'])

    return render_template('spirits.j2', spirit_data=spirit_data,  edit_form=edit_form)

