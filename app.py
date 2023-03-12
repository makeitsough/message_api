from flask import Flask, request, jsonify, render_template
from jinja2 import Environment, PackageLoader, select_autoescape
import psycopg2
from datetime import datetime
import json

app = Flask(__name__)

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


@app.route('/message/', methods=['GET', 'POST'])
def new_message():
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
    body = json.dumps(dict(request.form))
    cur.execute("INSERT INTO requests (method, path, headers, body, created_at) VALUES (%s, %s, %s, %s, %s)", (
        request.method,
        request.path,
        headers,
        body,
        datetime.now()
    ))
    conn.commit()

    # Close the connection
    cur.close()
    conn.close()

    ##input_message = input('Enter message')
    return render_template('sent.html')

@app.route('/retrieve/', methods=['GET'])
def get_message():
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
    body = json.dumps(dict(request.form))
    cur.execute("INSERT INTO requests (method, path, headers, body, created_at) VALUES (%s, %s, %s, %s, %s)", (
        request.method,
        request.path,
        headers,
        body,
        datetime.now()
    ))
    conn.commit()

        #Query recent messages; option to specify number of messages
    #Substituting for user input == number of messages to retriev
    user_input = 3
    cur.execute("SELECT body FROM requests WHERE method='POST' ORDER BY created_at DESC LIMIT {:d}".format(user_input))
    for record in cur:
        print(record)


    cur.close()
    conn.close()

    return render_template('send.html')