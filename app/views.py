from app import app
from flask import Flask, render_template, request,session, redirect, url_for,flash,session
from forms import SignupForm, SigninForm,EventForm
from models import db,User,Event

@app.route('/')
@app.route('/index')
def index():
  #return "hello"
	return render_template('index.html')


  
@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form = SignupForm()
   
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('signup.html', form=form)
    else:
      newuser = User(form.firstname.data, 
                    form.lastname.data, 
                      form.email.data, 
                      form.password.data)
      db.session.add(newuser)
      db.session.commit()
      session['email'] = newuser.email
       
      return redirect(url_for('index'))
   
  elif request.method == 'GET':
    return render_template('signup.html', form=form)

@app.route('/profile')
def profile():
 if 'email' not in session:
    return redirect(url_for('index'))
 
    user = User.query.filter_by(email = session['email']).first()
 
    if user is None:
      return redirect(url_for('signin'))
    else:
      return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def signin():
  form = SigninForm()
   
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('login.html', form=form)
    else:
      session['email'] = form.email.data
      return redirect(url_for('index'))
                 
  elif request.method == 'GET':
    return render_template('login.html', form=form)

@app.route('/post_event', methods=['GET', 'POST'])
def post_event():
  form = EventForm(request.form)
  if request.method == 'POST':
    #if form.validate():
    newevent = Event(form.name.data, 
                      form.location.data, 
                      form.date.data, 
                      form.description.data)
    db.session.add(newevent)
    db.session.commit()
    return render_template('events.html', form=form)
    

  elif request.method == 'GET':
    return render_template('post_events.html', form =form)

@app.route('/events')
def events():
  return render_template('events.html')

@app.route('/logout')
def gallery():
  pass