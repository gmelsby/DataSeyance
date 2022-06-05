from flask import Flask
from flask_mysqldb import MySQL
import os

# all of our routes are in here
from blueprints.index import index
from blueprints.seances import seances
from blueprints.locations import locations
from blueprints.channelings import channelings
from blueprints.spirits import spirits
from blueprints.attendees import attendees
from blueprints.mediums import mediums
from blueprints.methods import methods
from blueprints.seanceattendees import seanceattendees

app = Flask(__name__)
mysql = MySQL(app)
# all of our routes are blueprints in the blueprints directory.
app.register_blueprint(index)
app.register_blueprint(seances)
app.register_blueprint(locations)
app.register_blueprint(channelings)
app.register_blueprint(spirits)
app.register_blueprint(attendees)
app.register_blueprint(mediums)
app.register_blueprint(methods)
app.register_blueprint(seanceattendees)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3023))
    app.run(port=port, debug=True)
