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
   license_number = db.Column(db.String(100), primary_key=True)
   advocate_name = db.Column(db.String(100))
   email = db.Column(db.String(100))
   password = db.Column(db.String(100))


   def __init__(self, license_number, advocate_name, email, password):
      self.license_number = license_number
      self.advocate_name = advocate_name
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
      
class Case(db.Model):
   case_number = db.Column(db.Integer, primary_key=True)
   case_name = db.Column(db.String(300))
   client_name = db.Column(db.String(100), db.ForeignKey(Client.client_name))
   opponent = db.Column(db.String(300))
   court = db.Column(db.String(100))
   case_type = db.Column(db.String(100))
   description = db.Column(db.String(1000))
   opponent_advocate = db.Column(db.String(100))
   judge = db.Column(db.String(100))
   filing_date = db.Column(db.Date)
   assigned_advocates = db.db.Column(db.String(1000))

   def __init__(self, case_number, case_name,client_name, opponent, court, case_type, description, opponent_advocate, judge, filing_date, assigned_advocates):
      self.case_number = case_number
      self.case_name = case_name
      self.client_name = client_name
      self.opponent = opponent
      self.court = court
      self.case_type = case_type
      self.description = description
      self.opponent_advocate = opponent_advocate
      self.judge = judge
      self.filing_date = filing_date
      self.assigned_advocates = assigned_advocates
   
class Hearings(db.Model):
   id = db.Column(db.Integer, primary_key=True, auto_increment=True)
   case_number = db.Column(db.String(300))
   license_number = db.Column(db.String(100), db.ForeignKey(Advocate.license_number))
   description = db.Column(db.String(1000))
   hearing_date = db.Column(db.Date)
   next_hearing_date = db.Column(db.Date)

   def __init__(self, case_number, id,license_number, hearing_date, next_hearing_date, case_type, description, hearing_date_advocate, judge, filing_date, assigned_advocates):
      self.case_number = case_number
      self.id = id
      self.license_number = license_number
      self.hearing_date = hearing_date
      self.next_hearing_date = next_hearing_date
      self.description = description


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