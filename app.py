import os
from flask import Flask, render_template, request, session , redirect, flash
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)


s = os.environ.get("DATABASE_URL")
s = 'postgresql+psycopg2:/' + s[s.find('/')+1:]
app.config['SQLALCHEMY_DATABASE_URI'] = s
db = SQLAlchemy(app)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SECRET_KEY'] = "secret key"
Session(app)

from models import User

@app.route('/',methods=['POST','GET'])
def home():
   user = session.get('current_user',None)
   return render_template('/index.html',user=user)

@app.route('/login',methods=['POST','GET'])
def login():
   if request.method == 'POST':
      uname = request.form['username']
      passw = request.form['password']
      session['current_user'] = User.login_user(uname,passw)
      user = session.get('current_user',None)
      if user == None:
         flash('Incorrect password or username')
      else:
         return redirect('/user_home')
   user = session.get('current_user',None)
   return render_template('/login.html',user=user)

@app.route('/register',methods=['POST','GET'])
def register():
   if request.method == 'POST':
      frm = request.form
      try:
         db.session.add(User(frm['username'],frm['password'],frm['name'],frm['email'],frm['mobile'],frm['date'],frm['panno'],frm['aadhar']))
         db.session.commit()
         session['current_user'] = User.query.filter_by(username=frm['username']).first()
      except(Exception):
         flash("Improper details")
         return render_template('/register.html')
      return redirect('/user_home')
   user = session.get('current_user',None)
   return render_template('/register.html',user=user)

@app.route('/user_home',methods=['POST','GET'])
def user_home():
   user = session.get('current_user',None)
   if user == None:
      flash('Incorrect password or username')
      return redirect('/login')
   return render_template('/user_home.html',user=user)

@app.route('/personal_details',methods=['POST','GET'])
def personal_details():
   user = session.get('current_user',None)
   if user == None:
      flash('Incorrect password or username')
      return redirect('/login')
   return render_template('/personal_details.html',user=user)

@app.route('/company_details',methods=['POST','GET'])
def company_details():
   user = session.get('current_user',None)
   return render_template('/company_details.html',user=user)

@app.route('/logout',methods=['POST','GET'])
def logout():
   session['current_user']=None
   return redirect('/')