from flask_app import app, render_template, request, redirect, session, jsonify
from flask_app.models.event import Event
from flask_app.models.dance import Dance
from flask_app.models.user import User

@app.route('/new/dance')
def new_dance():

    return render_template('new_dance.html')


# ! CREATE 
@app.route('/create/dance', methods = ['post'])
def create_dance():
    print(request.form )
    if not Dance.validate_dance(request.form):
        return redirect('/new/dance')
    dance = Dance.save(request.form)
    return redirect('/dances')

# ! READ ALL
@app.route('/dashboard')
@app.route('/dances')
def dances():
    # ! code to keep non-logged-in users from visiting route
    if 'user_id' not in session:
        return redirect('/logout')

    return render_template('dashboard.html')

# ! READ ONE
@app.route('/show/dance/<int:id>')
def show_dance(id):
    data = {'id': id}
    dance = Dance.get_one(data)
    return render_template('show_dance.html', dance = dance)

# ! UPDATE
@app.route('/edit/<int:id>')
def edit_dance(id):
    data = {'id':id}
    return render_template('edit_dance.html', dance = Dance.get_one(data))

@app.route('/update/dance', methods = ['post'])
def update_dance():
    print(request.form)
    if not Dance.validate_dance(request.form):
        return redirect(f"/edit/{request.form['id']}")
    Dance.update(request.form)
    return redirect(f"/dashboard")

# ! DELETE 
@app.route('/delete/<int:id>')
def delete_dance(id):
    Dance.destroy({'id': id})
    return redirect(f"/dashboard")

@app.route('/events_data')
def event_data():
    events = [
        {
            'todo' : 'Alberto Birthday',
            'date' : '2022-08-25',
        },
        {
            'todo' : 'Comer tacos de carne asada',
            'date' : '2022-08-26',
        }
    ]
    return jsonify(events)


@app.route('/event')
def home():
    
    return render_template('calendar_events.html', events = Event.get_all())


@app.route('/create/event', methods = ['post'])
def create_event():
    print(request.form )
    event = Event.save(request.form)
    return redirect('/event')




