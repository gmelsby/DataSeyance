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

@app.route('/mediums', methods=['GET', 'POST'])
def mediums():
    if request.method == 'POST':
        if request.form.get('id_input') and request.form.get('name'):
            full_name_input = request.form['name']
            id_input = request.form['id_input']

            query = ('UPDATE Mediums ' 
                     f'SET full_name = "{full_name_input}" '
                     f'WHERE medium_id = {id_input};')

            cursor = db.execute_query(db_connection=db_connection, query=query)
            mysql.connection.commit();
            
            return redirect('/mediums')

        if request.form.get('name') and request.form.get('id_input') != '':
            full_name_input = request.form['name']
            query = f'INSERT INTO Mediums (full_name) VALUES ("{full_name_input}");'
            cursor = db.execute_query(db_connection=db_connection, query=query)
            mysql.connection.commit();
            
        return redirect('/mediums')

    if request.method == 'GET':
        args = request.args
        medium_to_edit = None
        if args.get('id'):
            preselect_query = f"SELECT medium_id, full_name FROM Mediums WHERE medium_id = {args.get('id')};"
            cursor = db.execute_query(db_connection=db_connection, query=preselect_query)
            medium_to_edit = cursor.fetchall()[0]
            
        query = 'SELECT medium_id, full_name FROM Mediums;'
        cursor = db.execute_query(db_connection=db_connection, query=query)
        medium_data = cursor.fetchall()

        return render_template('mediums.j2', medium_data=medium_data, medium_to_edit=medium_to_edit)
    
@app.route('/delete_medium/<int:id>')
def delete_medium(id):
    query = f'DELETE FROM Mediums WHERE medium_id = {id};'
    cursor = db.execute_query(db_connection=db_connection, query=query)
    mysql.connection.commit()
    
    return redirect('/mediums')




@app.route('/methods', methods=['GET', 'POST'])
def methods():
    if request.method == 'POST':
        if request.form.get('id_input') and request.form.get('name'):
            name_input = request.form['name']
            id_input = request.form['id_input']
            description_input = 'NULL'
            if request.form.get('description'):
                description_input = f'"{request.form["description"]}"'


            query = ('UPDATE Methods ' 
                     f'SET name = "{name_input}", '
                     f'description = {description_input} '
                     f'WHERE method_id = {id_input};')

            cursor = db.execute_query(db_connection=db_connection, query=query)
            mysql.connection.commit();
            
            return redirect('/methods')

        if request.form.get('name') and request.form.get('id_input') != '':
            name_input = request.form['name']
            description_input = 'NULL'
            if request.form.get('description'):
                description_input = f'"{request.form["description"]}"'
            query = f'INSERT INTO Methods (name, description) VALUES ("{name_input}", {description_input});'
            cursor = db.execute_query(db_connection=db_connection, query=query)
            mysql.connection.commit();
            
        return redirect('/methods')

    if request.method == 'GET':
        args = request.args
        method_to_edit = None
        if args.get('id'):
            preselect_query = f"SELECT method_id, name, description FROM Methods WHERE method_id = {args.get('id')};"
            cursor = db.execute_query(db_connection=db_connection, query=preselect_query)
            method_to_edit = cursor.fetchall()[0]
            
        query = 'SELECT method_id, name, description FROM Methods;'
        cursor = db.execute_query(db_connection=db_connection, query=query)
        method_data = cursor.fetchall()

        return render_template('methods.j2', method_data=method_data, method_to_edit=method_to_edit)
    

@app.route('/delete_method/<int:id>')
def delete_method(id):
    query = f'DELETE FROM Methods WHERE method_id = {id};'
    cursor = db.execute_query(db_connection=db_connection, query=query)
    mysql.connection.commit()
    
    return redirect('/methods')


@app.route('/seanceattendees')
def seanceattendees():
    return render_template('seanceattendees.j2')

@app.route('/seances')
def seances():
    return render_template('seances.j2')

@app.route('/spirits', methods=['GET', 'POST'])
def spirits():
    if request.method == 'POST':
        if request.form.get('id_input') and request.form.get('name'):
            full_name_input = request.form['name']
            id_input = request.form['id_input']

            query = ('UPDATE Spirits ' 
                     f'SET full_name = "{full_name_input}" '
                     f'WHERE spirit_id = {id_input};')

            cursor = db.execute_query(db_connection=db_connection, query=query)
            mysql.connection.commit();
            
            return redirect('/spirits')

        if request.form.get('name') and request.form.get('id_input') != '':
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
    port = int(os.environ.get('PORT', 5005))
    app.run(port=port, debug=True)