import os
from flask import Flask, render_template, request, session , redirect
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
app.config['SECRET_KEY'] = 'super secret key'
Session(app)

from models import User

@app.route('/',methods=['POST','GET'])
def home():
   return render_template('/index.html')

@app.route('/login',methods=['POST','GET'])
def login():
   return render_template('/login.html')

@app.route('/login_',methods=['POST'])
def check_login():
   uname = request.form['username']
   passw = request.form['password']
   session['current_user'] = User.login_user(uname,passw)
   return redirect('/user_home')

@app.route('/register',methods=['POST','GET'])
def register():
   return render_template('/register.html')

@app.route('/register_',methods=['POST'])
def reg():
   frm = request.form
   db.session.add(User(frm['username'],frm['password'],frm['name'],frm['email'],frm['mobile'],frm['date'],frm['panno'],frm['aadhar']))
   db.session.commit()
   session['current_user'] = User.query.filter_by(username=frm['username']).first()
   return redirect('/user_home')

@app.route('/user_home',methods=['POST','GET'])
def user_home():
   user = session.get('current_user',None)
   if user == None:
      return redirect('/')
   return render_template('/user_home.html',user=user)

