from flask import Flask, render_template, redirect, json, request
from flask_mysqldb import MySQL
import os
import database.db_connector as db

db_connection = db.connect_to_database()

app = Flask(__name__)
mysql = MySQL(app)

@app.route('/')
def root():
    return redirect("/index", code=302)


@app.route('/index')
def index():
    return render_template('index.j2')

@app.route('/attendees')
def attendees():
    return render_template('attendees.j2')

@app.route('/channelings')
def channelings():
    return render_template('channelings.j2')

@app.route('/locations')
def locations():
    return render_template('locations.j2')

@app.route('/mediums')
def mediums():
    return render_template('mediums.j2')

@app.route('/methods')
def methods():
    return render_template('methods.j2')

@app.route('/seanceattendees')
def seanceattendees():
    return render_template('seanceattendees.j2')

@app.route('/seances')
def seances():
    return render_template('seances.j2')

@app.route('/spirits', methods=['GET', 'POST'])
def spirits():
    if request.method == 'POST':
        if request.form.get('id_input'):
            full_name_input = request.form['name']
            id_input = request.form['id_input']

            query = ('UPDATE Spirits ' 
                     f'SET full_name = "{full_name_input}" '
                     f'WHERE spirit_id = {id_input};')

            cursor = db.execute_query(db_connection=db_connection, query=query)
            mysql.connection.commit();
            
            return redirect('/spirits')

        if request.form.get('name'):
            full_name_input = request.form['name']
            query = f'INSERT INTO Spirits (full_name) VALUES ("{full_name_input}");'
            cursor = db.execute_query(db_connection=db_connection, query=query)
            mysql.connection.commit();
            
        return redirect('/spirits')

    if request.method == 'GET':
        args = request.args
        spirit_to_edit = None
        if args.get('id'):
            preselect_query = f"SELECT spirit_id, full_name FROM Spirits WHERE spirit_id = {args.get('id')};"
            cursor = db.execute_query(db_connection=db_connection, query=preselect_query)
            spirit_to_edit = cursor.fetchall()[0]

        query = 'SELECT spirit_id, full_name FROM Spirits;'
        cursor = db.execute_query(db_connection=db_connection, query=query)
        spirit_data = cursor.fetchall()

        return render_template('spirits.j2', spirit_data=spirit_data, spirit_to_edit=spirit_to_edit)
    
@app.route('/delete_spirit/<int:id>')
def delete_spirit(id):
    query = f'DELETE FROM Spirits WHERE spirit_id = {id};'
    cursor = db.execute_query(db_connection=db_connection, query=query)
    mysql.connection.commit()
    
    return redirect('/spirits')



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port, debug=True)