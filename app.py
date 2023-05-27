from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taarikh.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)
bcrypt=Bcrypt(app)

class Admin(db.Model):
   email = db.Column(db.String(100), primary_key=True)
   password = db.Column(db.String(100))


   def __init__(self, email, password):
      self.email = email
      self.password = bcrypt.generate_password_hash(password).decode('utf-8')
      
class Advocate(db.Model):
   email = db.Column(db.String(100), primary_key=True)
   password = db.Column(db.String(100))


   def __init__(self, email, password):
      self.email = email
      self.password = bcrypt.generate_password_hash(password).decode('utf-8')
      
   
class Client(db.Model):
   id = db.Column(db.Integer,primary_key=True)
   name = db.Column(db.String(100),nullable=False)
   email = db.Column(db.String(100), primary_key=True)
   password = db.Column(db.String(100))


   def __init__(self, id, name,email, mobile):
      self.id = id
      self.name = name
      self.email = email
      self.mobile = mobile
      


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
   
   user = Advocate.query.filter_by(email=email).first()
   if user and bcrypt.check_password_hash(user.password, password):
      flash('Logged in successfully!', 'success')
      return render_template('indiv.html')
   else:
      flash('Invalid email or password', 'error')
      return render_template('home.html')



#create new client
@app.route('/add_client',methods=["POST"])
def addclient():
   id = request.form['id']
   name = request.form['name']
   email = request.form['email']
   mobile = request.form['mobile']

   new_client = Client(id=id, name=name, email=email, mobile=mobile)
   db.session.add(new_client)
   db.session.commit()
   
   flash('Client added successfully!', 'success')
   return render_template('same.html')
if __name__ == '__main__':
   with app.app_context():
      db.create_all()
      
      app.run(debug = True)