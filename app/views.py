from app import app
from flask import Flask, render_template, request,session, redirect, url_for,flash,session
from forms import SignupForm, SigninForm,EventForm
from models import db,User,Event
from werkzeug import secure_filename
import random,string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

@app.route('/')
@app.route('/index')
def index():
  name = Event.name
  #event =Event.event
  #q = session.query(User).filter(User.name == 'fred')
  new_events = Event.query.filter_by(id = Event.id)
  return render_template('index.html',new_events=new_events,name = name)

	#return render_template('index.html')
@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form = SignupForm()
  if 'email' in session:
    return redirect(url_for('post_event'))
   
  if request.method == 'POST':
    if form.validate() == False:
      flash('All fields are required')
      return render_template('signup.html', form=form)
    else:
      newuser = User(form.firstname.data, 
                    form.lastname.data, 
                      form.email.data, 
                      form.password.data)
      db.session.add(newuser)
      flash("Registration successful")
      db.session.commit()
      session['email'] = newuser.email
      
      return redirect(url_for('signin'))
   
  elif request.method == 'GET':
      return render_template('signup.html', form=form)

@app.route('/profile')
def profile():
 if 'email' not in session:
    return redirect(url_for('login'))
 
    user = User.query.filter_by(email = session['email']).first()
 
    if user is None:
      return redirect(url_for('signin'))
    else:
      return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def signin():
  form = SigninForm()
  if 'email' in session:
    return redirect(url_for('post_event'))
   
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('login.html', form=form)
    else:
      session['email'] = form.email.data
      return redirect(url_for('post_event'))
                 
  elif request.method == 'GET':
    return render_template('login.html', form=form)

@app.route('/signout')
def signout():
 
  if 'email' not in session:
    return redirect(url_for('signin'))
     
  session.pop('email', None)
  return redirect(url_for('index'))

@app.route('/post_events', methods=['GET', 'POST'])
def post_event():
  form = EventForm()
  if 'email' not in session:
    flash("You need to login to post Events")
    return redirect(url_for('signin'))
  user = User.query.filter_by(email = session['email']).first()
  
  if user is None:
    return redirect(url_for())

  if request.method == 'POST':
    if form.validate() == False:
      flash("Fill all the fields")
      return render_template('post_events.html',form=form)
    else:
      
      newevent = Event(form.name.data, 
                      form.location.data, 
                      form.date.data, 
                      form.description.data)
      db.session.add(newevent)
      flash("Event successfully posted")
      db.session.commit()
      
      return redirect(url_for('index'))
  elif request.method == 'GET':
      return render_template('post_events.html',form=form)
      
@app.route('/events')
def events():
  name = Event.name
  #event =Event.event
  #q = session.query(User).filter(User.name == 'fred')
  new_events = Event.query.filter_by(id = Event.id)
  return render_template('events.html',new_events=new_events,name = name)
@app.route('/google')
def showLogin():
  state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
  session['state'] = state
  #return "The current session state is %s" % session['state']
  return render_template('google.html', STATE=state)
  
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    session['access_token'] = credentials.access_token
    session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    session['username'] = data['name']
    session['picture'] = data['picture']
    session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += session['username']
    output += '!</h1>'
    output += '<img src="'
    output += session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % session['username'])
    print "done!"
    return output

