from flask import Flask, render_template, redirect, request, session, flash
from mysqlconnection import MySQLConnector
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

app = Flask(__name__)

mysql = MySQLConnector(app,'email')

app.secret_key = "ThisIsSecret!"

@app.route('/', methods=['GET'])
def index():
	if not session.has_key('display'):
		session['display'] = False


	query = "SELECT * FROM emails"
	emails = mysql.query_db("SELECT * FROM emails")
	print session['display']
	return render_template("index.html", emails=emails, display=session['display'])

@app.route('/process', methods=['POST'])
def submit():
    if not EMAIL_REGEX.match(request.form['email']):
        flash('<div class="error">Email is not valid!</div>')
    else:
		flash('<div class="success">The email you entered ' +request.form["email"]+ ' is a VALID email address! Thank you!</div>')
		query = "INSERT INTO emails (email, created_at, updated_at) VALUES (:email, NOW(), NOW())"
		data = {
		'email': request.form['email']
		}
		mysql.query_db(query, data)
		session['display'] = True
    return redirect('/')
@app.route('/clear')
def clear():
	session.clear()
	return redirect('/')
app.run(debug=True)