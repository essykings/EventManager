import time
from datetime import datetime
from flask.ext.wtf import Form
from flask_wtf.file import FileField

from wtforms import  TextField,fields, widgets,DateTimeField, DateField,TextAreaField, SubmitField,PasswordField,FileField
from wtforms import validators 
from models import db, User


class SignupForm(Form):
  firstname = TextField("First name",  [validators.Required("Please enter your first name.")])
  lastname = TextField("Last name",  [validators.Required("Please enter your last name.")])
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  password = PasswordField('Password', [validators.Required("Please enter a password.")])
  submit = SubmitField("Create account")
 
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not Form.validate(self):
      return False
     
    # user = User.query.filter_by(email = self.email.data.lower()).first()
    # if user:
    #   self.email.errors.append("That email is already taken")
    #   return False
    # else:
    #   return True

class SigninForm(Form):
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  password = PasswordField('Password', [validators.Required("Please enter a password.")])
  submit = SubmitField("Sign In")
   
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not Form.validate(self):
      return False
     
    user = User.query.filter_by(email = self.email.data.lower()).first()
    if user and user.check_password(self.password.data):
      return True
    else:
      self.email.errors.append("Invalid e-mail or password")
      return False


class EventForm(Form):
  date = DateTimeField('Date',format= '%m/%d/%Y')
  name = TextField("Event title",[validators.DataRequired()])
  location = TextField("Location",[validators.DataRequired()])
  
  description = TextField("Description",[validators.DataRequired()])
  submit = SubmitField("Submit Event")

  