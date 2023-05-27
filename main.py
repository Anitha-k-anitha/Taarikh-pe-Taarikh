from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.app_context()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tarikh.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

class Admin(db.Model):
   id = db.Column(db.Integer, primary_key=True)

   email = db.Column(db.String(120), unique=True, nullable=False)
   password_hash = db.Column(db.String(128), nullable=False)

   def set_password(self, password):
      self.password_hash = generate_password_hash(password)

   
   def __init__(self, id, email, password):
      self.id = id
      self.email = email
      self.password = password

# class students(db.Model):
#    id = db.Column('student_id', db.Integer, primary_key = True)
#    name = db.Column(db.String(100))
#    city = db.Column(db.String(50))
#    addr = db.Column(db.String(200)) 
#    pin = db.Column(db.String(10))

# def __init__(self, name, city, addr,pin):
#    self.name = name
#    self.city = city
#    self.addr = addr
#    self.pin = pin

# @app.route('/')
# def show_all():
#    return render_template('show_all.html', students = students.query.all() )
def add_admin():
   admin = Admin(1,'mihika831@gmail.com', '1234')
         
   db.session.add(admin)
   db.session.commit()

@app.route('/new', methods = ['GET', 'POST'])
def new():
   admin = Admin.query.all()
#    if request.method == 'POST':
#       if not request.form['name'] or not request.form['city'] or not request.form['addr']:
#          flash('Please enter all the fields', 'error')
#       else:
#          student = students(request.form['name'], request.form['city'],
#             request.form['addr'], request.form['pin'])
         
#          db.session.add(student)
#          db.session.commit()
#          flash('Record was successfully added')
#          return redirect(url_for('show_all'))
   return render_template('index.html', admin=admin)

if __name__ == '__main__':
   with app.app_context():
      db.create_all()
   with app.app_context():
      add_admin()

      app.run(debug = True)


      # admin = Admin('mihika831@gmail.com', '1234')
         
      # db.session.add(admin)
      # db.session.commit()