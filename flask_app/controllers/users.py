from flask_app import app, render_template, request, redirect, session, bcrypt, flash
from flask_app.models.user import User
from flask import Flask

# TODO ROOT ROUTE
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/login')
def show_login():
    return render_template('login.html')
    
@app.route('/calender_event')
def calender_event():
    return render_template('calender_events.html')

# TODO REGISTER
@app.route('/register', methods = ['post'])
def register():
    ## validate them
    print(request.form)
    data = {'email': request.form['email']}
    user_in_db = User.get_one_with_email(data)
    if user_in_db:
        flash("email already in use", 'email')
        return redirect('/login')
    if not User.validate_user(request.form):
        return redirect('/login')
    hashed_pw = bcrypt.generate_password_hash(request.form['password'])
    print(hashed_pw)
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': hashed_pw
    }
    print(data)
    ## add user to database
    user_id = User.save(data)
    ## log in the user by adding them to session
    session['user_id'] = user_id
    session['first_name'] = request.form['first_name']

    return redirect('/')

# TODO LOGIN
@app.route('/login', methods = ['post'])
def login():
    ## check the database for the email they enter
    data = {'email': request.form['log_email']}
    user_in_db = User.get_one_with_email(data)
    if not user_in_db:
        flash("invalid credentials")
        return redirect('/login')
    ## check the password the supply matches the hash in the database
    if not bcrypt.check_password_hash(user_in_db.password, request.form['log_password']):
        flash("invalid credentials")
        return redirect('/login')
    ## log in the use by adding to session
    session['user_id'] = user_in_db.id
    session['first_name'] = user_in_db.first_name
    return redirect('/')


# TODO LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
    pass

# app = Flask('FullCalendar Demo')


@app.route('/')
def homeie():
        return render_template('index.html')

@app.route('/calendar')
def events():
    # events = [
    #     {
    #         'todo' : 'Alberto Birthday',
    #         'date' : '2022-08-25',
    #     },
    #     {
    #         'todo' : 'Comer tacos de carne asada',
    #         'date' : '2022-08-26',
    #     }
    # ]

    return render_template('calendar_events.html')

