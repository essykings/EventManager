from datetime import datetime
from flask import Flask
from app import db
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
from sqlalchemy import Integer, ForeignKey, String, Column

class Google(db.Model):
    __tablename__ = "gmail"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=True)
    avatar = db.Column(db.String(200))
    active = db.Column(db.Boolean, default=False)
    tokens = db.Column(db.Text)
    created_at = db.Column(db.DateTime)

class User(db.Model):

  __table__name = "users"
  id = db.Column(db.Integer, primary_key = True)
  firstname = db.Column(db.String(100))
  lastname = db.Column(db.String(100))
  email = db.Column(db.String(120))
  pwdhash = db.Column(db.String(54))
  events = db.relationship('Event', backref='owner', lazy='dynamic')
   
  def __init__(self, firstname, lastname, email, password):
    self.firstname = firstname.title()
    self.lastname = lastname.title()
    self.email = email.lower()
    self.set_password(password)
     
  def set_password(self, password):
    self.pwdhash = generate_password_hash(password)
   
  def check_password(self, password):
    return check_password_hash(self.pwdhash, password)
class Event(db.Model):
  __table__name = "events"
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50))
  location = db.Column(db.String(50))
  date = db.Column(db.DateTime)
  description = db.Column(db.String)
  timestamp = db.Column(db.DateTime, index=True)
  owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  
  def __init__ (self, name, location, date, description):
    self.name = name
    self.location = location
    self.date = date
    self.description =description
    

  