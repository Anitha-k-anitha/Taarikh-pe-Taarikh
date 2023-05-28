from flask import Flask, request, flash, render_template, jsonify, request, session, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taarikh.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    # Code to load and return the user object based on the user_id
    pass

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
   id = db.Column(db.Integer,primary_key=True, autoincrement=True)
   name = db.Column(db.String(100),nullable=False)
   email = db.Column(db.String(100))
   mobile = db.Column(db.String(10),nullable=False)



   def __init__(self, id, name,email, mobile):
      self.id = id
      self.name = name
      self.email = email
      self.mobile = mobile
      
class Case(db.Model):
   case_number = db.Column(db.Integer, primary_key=True)
   case_name = db.Column(db.String(300))
   client_name = db.Column(db.String(100), db.ForeignKey(Client.name))
   opponent = db.Column(db.String(300))
   court = db.Column(db.String(100))
   case_type = db.Column(db.String(100))
   description = db.Column(db.String(1000))
   opponent_advocate = db.Column(db.String(100))
   judge = db.Column(db.String(100))
   filing_date = db.Column(db.Date)
   assigned_advocates = db.Column(db.String(1000))

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
   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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
def index():
   return render_template('index.html')

@app.route('/login-firm', methods=["POST", "GET"])
def loginfirm():
   if request.method == 'POST':
      email = request.form['email']
      password = request.form['password']
   
      user = Admin.query.filter_by(email=email).first()
      if user and bcrypt.check_password_hash(user.password, password):
         flash('Logged in successfully!', 'success')
         print(session)
         session['admin_email'] = email
         advocates = Advocate.query.all()
         return render_template('admin_home.html')
      else:
         flash('Invalid email or password', 'error')
   return render_template('loginfirm.html')



#login for advocate
@app.route('/login-ind', methods=["POST", "GET"])
def loginInd():
   if request.method == 'POST':
      email = request.form['email']
      password = request.form['password']
   
      user = Advocate.query.filter_by(email=email).first()
      if user and bcrypt.check_password_hash(user.password, password):
         flash('Logged in successfully!', 'success')
         print(session)
         session['advocate_name'] = user.advocate_name 
         return render_template('advocate_dashboard.html')
      else:
         flash('Invalid email or password', 'error')
   return render_template('loginindiv.html')



#create new client
@app.route('/add_client',methods=["POST", "GET"])
def addclient():
   if request.method == 'POST':
      id = request.form['client_id']
      name = request.form['name']
      email = request.form['email']
      mobile = request.form['mobile']

      new_client = Client(id=id, name=name, email=email, mobile=mobile)
      db.session.add(new_client)
      db.session.commit()
      
      flash('Client added successfully!', 'success')
   return render_template('addClient.html')

#get all cases
@app.route('/cases', methods=["GET"])
def cases():
   if not session['advocate_name']:
      return redirect(url_for('loginInd')) 
   assigned_advocates = session['advocate_name']
   cases = Case.query.filter_by(assigned_advocates=assigned_advocates).order_by(Case.case_number).all()
   case_list = []
    
   for case in cases:
      case_data = {
         
         'Case_number': case.case_number,
         'name': case.case_name,
         'hearing_date': case.hearing_date.strftime('%Y-%m-%d'),
         'court': case.court
      }
      case_list.append(case_data)
    
   return render_template('cases.html', cases=case_list)

   
   
#get dated cases
@app.route('/datedcases',methods=["GET"])
def datedcases():
   if not session['advocate_name']:
      return redirect(url_for('loginInd'))
   date= request.args.get('date')
   assigned_advocates = session['advocate_name']
   cases = Case.query.filter_by(assigned_advocates=assigned_advocates, filing_date=date).order_by(Case.case_number).all()
   case_list = []
   for case in cases:
      case_data = {
         'Case_number': case.case_number,
         'name': case.case_name,
         'hearing_date': case.hearing_date.strftime('%Y-%m-%d'),
         'court':case.court
        }
      case_list.append(case_data)
   return render_template('cases.html', cases=case_list)



#add advocate
@app.route('/add-advocate',methods=["POST", "GET"])   
def addadvocate():
   if request.method == 'POST':
      license_number = request.form['license_number']
      advocate_name = request.form['advocate_name']
      email = request.form['email']
      password = request.form['password']
   
      new_advocate = Advocate(license_number=license_number, advocate_name=advocate_name, email=email, password=password)
      db.session.add(new_advocate)
      db.session.commit()
   
      flash("Advocate added succesfully", "success")
   return render_template("add_advocate.html")


#add cases

@app.route('/add-case',methods=["post", "GET"])
def addcase():
   if request.method=="POST":
      case_number = request.form['case_number']
      case_name = request.form['case_name']
      client_name = request.form['client_name']
      opponent = request.form['opponent']
      court =request.form['court']
      case_type = request.form['case_type']
      description = request.form['description']
      opponent_advocate = request.form['opponent_advocate']
      judge = request.form['judge']
      filing_date_list = request.form['filing_date'].split('-')
      print(filing_date_list)
      filing_date = datetime.date(int(filing_date_list[0]), int(filing_date_list[1]), int(filing_date_list[2]))
      print(filing_date)
      assigned_advocates = request.form['assigned_advocates']
   
   
      new_case = Case(case_number = case_number, case_name=case_name, client_name=client_name, opponent=opponent, court=court, case_type = case_type, description=description, opponent_advocate=opponent_advocate, judge=judge,filing_date=filing_date, assigned_advocates=assigned_advocates)
      db.session.add(new_case)
      db.session.commit()
      flash("Case added succefully","success")
   return render_template('addCases.html')

#add hearing
@app.route('/add-hearing',methods=["POST"])
def addhearing():
   case_number = request.form['case_number']
   id = request.form['id']
   license_number = request.form['license_number']
   hearing_date = request.form['hearing_date']
   next_hearing_date = request.form['next_hearing_date']
   description = request.form['description']
   
   new_hearing = Hearings(case_number = case_number, id=id, license_number=license_number, hearing_date=hearing_date, next_hearing_date=next_hearing_date,description=description)
   db.session.add(new_hearing)
   db.session.commit()
   
   
   flash("Hearing details added", "success")
   return render_template("firm.html")
   

def get_contact_info(Advocate):
    contact_info = {
        'phone': Advocate.phone,
        'email': Advocate.email,
    }
    return contact_info

#display all the advocates name and details in admin dashboard
@app.route('/admindashboard')
def admindashboard():
    print(session)
   #  print("email"+session["email"])
    advocates = Advocate.query.all()
    advocate_list = []
    
    for advocate in advocates:
        advocate_data = {
            'advocate_name': advocate.advocate_name,
            'email': advocate.email,
        }
        advocate_list.append(advocate_data)
    
    return render_template('admin_dashboard.html', advocates=advocate_list)


if __name__ == '__main__':
   with app.app_context():
      db.create_all()
    
      app.run(debug = True)