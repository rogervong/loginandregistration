from flask import Flask, render_template, request, redirect, session, flash
import re
from mysqlconnection import MySQLConnector
from flask.ext.bcrypt import Bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[a-zA-Z]*$')
app = Flask(__name__)
app.secret_key = 'ThisIsSecret'
bcrypt = Bcrypt(app)
mysql = MySQLConnector(app, 'loginregistration')
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
	email = request.form['email']
	first_name = request.form['first_name']
	last_name = request.form['last_name']
	password = request.form['password']
	confirm_pass = request.form['confirm_pass']
	error = False
	if len(request.form['email']) < 1:
		flash('Email cannot be empty')
		error = True
	elif not EMAIL_REGEX.match(request.form['email']):
		flash("Invalid Email Address!", 'register')
		error = True
	if len(request.form['first_name']) < 2:
		flash('First name cannot be empty', 'register')
		error = True
	elif not NAME_REGEX.match(request.form['first_name']):
		flash("First Name cannot have numbers!", 'register')
		error = True
	if len(request.form['last_name']) < 2:
		flash('Last Name cannot be empty', 'register')
		error = True
	elif not NAME_REGEX.match(request.form['last_name']):
		flash("Last Name cannot have numbers!", 'register')
		error = True
	if len(request.form['password']) < 8:
		flash('Password is too short', 'register')
		error = True
	if request.form['confirm_pass'] != request.form['password']:
		flash('Your passwords do not match', 'register')
		error = True
	if error:
		return redirect('/')
	query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (:first_name, :last_name, :email, :password, NOW(), NOW())"
	data = { 'first_name': first_name, 'last_name': last_name, 'email': email, 'password': bcrypt.generate_password_hash(password)}
	mysql.query_db(query, data)
	session['users'] = mysql.query_db("SELECT * FROM users")
	return render_template('result.html', all_users = session['users'])

@app.route('/login', methods =['post'])
def login():
	email = request.form['email']
	password = request.form['password']
	error = False
	if len(email) < 1:
		flash('Please Enter Email', 'login')
		error = True
	elif not EMAIL_REGEX.match(request.form['email']):
		flash("Invalid Email Address!", 'login')
		error = True
	if len(password) < 1:
		flash ('Please Enter Password', 'login')
	if error:
		return redirect('/')
	query = "SELECT * FROM users WHERE email = :email"
	data = { 'email': email }
	login = mysql.query_db(query, data)
	users = session['users']
	try:
		bcrypt.check_password_hash(login[0]['password'], password)
		return render_template('result.html', all_login = login)
	except:
		flash('password does not match', 'login')
		return redirect('/')
	return render_template('result.html', all_login = login)

@app.route('/goback', methods=['POST'])
def goback():
	return redirect('/')

app.run(debug=True)