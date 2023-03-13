from flask import Flask, request, jsonify, render_template
from jinja2 import Environment, PackageLoader, select_autoescape
import psycopg2
from datetime import datetime
import json

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

@app.route("/", methods=['GET', 'POST'])
def log_request():
        # Connect to the database 
    conn = psycopg2.connect(
        host='localhost',
        port='5432',
        dbname='paulschofield-personal',
        user='paulschofield-personal',
        password='root'
    )
    cur = conn.cursor()

        # Insert the request data into the database
    headers = json.dumps(dict(request.headers))
    cur.execute("INSERT INTO requests (method, path, headers, body, created_at) VALUES (%s, %s, %s, %s, %s)", (
        request.method,
        request.path,
        headers,
        request.data,
        datetime.now()
    ))
    conn.commit()

    # Close the connection
    cur.close()
    conn.close()

    return render_template('sent.html')