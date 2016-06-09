from flask import Flask, render_template, request, redirect, session, flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[a-zA-Z]')
app = Flask(__name__)
app.secret_key = 'ThisIsSecret'

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
	elif not EMAIL_REGEX.match(request.form['email']):
		flash("Invalid Email Address!")
		error = True
	if len(request.form['first_name']) < 1:
		flash('First name cannot be empty')
		error = True
	elif not NAME_REGEX.match(request.form['first_name']):
		flash("First Name cannot have numbers!")
		error = True
	if len(request.form['last_name']) < 1:
		flash('Last Name cannot be empty')
		error = True
	elif not NAME_REGEX.match(request.form['last_name']):
		flash("Last Name cannot have numbers!")
		error = True
	if len(request.form['password']) < 8:
		flash('Password is too short')
		error = True
	if request.form['confirm_pass'] != request.form['password']:
		flash('Your passwords do not match')
		error = True
	if error:
		return redirect('/')
	return render_template('result.html', email = email, first_name = first_name, last_name = last_name)

@app.route('/goback', methods=['POST'])
def goback():
	return redirect('/')

app.run(debug=True)