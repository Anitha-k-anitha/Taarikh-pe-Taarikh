from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)
bcrypt=Bcrypt(app)

class Admin(db.Model):
   email = db.Column(db.String(100), primary_key=True)
   password = db.Column(db.String(100))


   def __init__(self, email, password):
      self.email = email
      self.password = bcrypt.generate_password_hash(password).decode('utf-8')
      
class Indiv(db.Model):
   email = db.Column(db.String(100), primary_key=True)
   password = db.Column(db.String(100))


   def __init__(self, email, password):
      self.email = email
      self.password = bcrypt.generate_password_hash(password).decode('utf-8')
      
   


@app.route('/')
def home():
   return render_template('home.html')


@app.route('/login-firm', methods=["POST"])
def loginfirm():
   email = request.form['email']
   password = request.form['password']
   
   user = Admin.query.filter_by(email=email).first()
   if user and bcrypt.check_password_hash(user.password, password):
      flash('Logged in successfully!', 'success')
      return render_template('firm.html')
   else:
      flash('Invalid email or password', 'error')
      return render_template('home.html')
   
   
@app.route('/login-ind', methods=["POST"])
def loginInd():
   email = request.form['email']
   password = request.form['password']
   
   user = Indiv.query.filter_by(email=email).first()
   if user and bcrypt.check_password_hash(user.password, password):
      flash('Logged in successfully!', 'success')
      return render_template('indiv.html')
   else:
      flash('Invalid email or password', 'error')
      return render_template('home.html')


if __name__ == '__main__':
   app.run(debug = True)