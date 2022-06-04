# Author: Ed Wise
# Date: 
# Description:
from flask import Blueprint, render_template

index = Blueprint("index", __name__, static_folder="static", template_folder="templates")


@index.route('/index')
@index.route('/')
def home():
    return render_template('index.j2')