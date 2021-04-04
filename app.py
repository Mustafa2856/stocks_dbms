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


from models import User, Bank_Details, demat, company, shares, portfolio, transactions
comp = company.query.all()
shars = shares.query.all()
cmp = {}
shrs = {}
for i in comp:
   cmp[i.id] = i
for i in shars:
   shrs[i.company_id] = i
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
         try:
            session['current_demat'] = demat.get_ac(uname)
            session['current_trans'] = transactions.get_trs(session['current_demat'].account_no)
         except Exception as exp:
            print(exp)
            flash("Some error occured with your account")
            return render_template('/login.html',user=user)
         return redirect('/user_home')
   user = session.get('current_user',None)
   return render_template('/login.html',user=user)

@app.route('/register',methods=['POST','GET'])
def register():
   if request.method == 'POST':
      frm = request.form
      try:
         db.session.add(User(frm['username'],frm['password'],frm['name'],frm['email'],frm['mobile'],frm['date'],frm['panno'],frm['aadhar']))
         db.session.add(Bank_Details(frm['bank_ac'],frm['username'],frm['bank_name'],frm['bank_branch'],frm['bank_ifsc']))
         db.session.add(demat(frm['username']))
         db.session.commit()
         session['current_user'] = User.query.filter_by(username=frm['username']).first()
         session['current_demat'] = demat.query.filter_by(User_id=frm['username']).first()
         session['current_trans'] = transactions.query.filter_by(demat_ac=session.get('current_demat',None))
      except Exception as exp:
         print(exp)
         flash("Improper details")
         return render_template('/register.html')
      return redirect('/user_home')
   user = session.get('current_user',None)
   return render_template('/register.html',user=user)

@app.route('/user_home',methods=['POST','GET'])
def user_home():
   user = session.get('current_user',None)
   dmt = session.get('current_demat',None)
   trans = session.get('current_trans',None)
   if user == None:
      flash('Login to Access Account Details')
      return redirect('/login')
   return render_template('/user_home.html',user=user,dmt=dmt,trans=trans)

@app.route('/personal_details',methods=['POST','GET'])
def personal_details():
   user = session.get('current_user',None)
   if user == None:
      flash('Login to Access Personal Details Page')
      return redirect('/login')
   return render_template('/personal_details.html',user=user)

@app.route('/company_details',methods=['POST','GET'])
def company_details():
   user = session.get('current_user',None)
   return render_template('/company_details.html',user=user)

@app.route('/logout',methods=['POST','GET'])
def logout():
   session['current_user']=None
   session['current_demat']=None
   session['current_trans']=None
   return redirect('/')



@app.route('/portfolio',methods=['POST','GET'])
def porfolio():
   user = session.get('current_user',None)
   dmt = session.get('current_demat',None)
   trans = session.get('current_trans',None)
   pft = portfolio.get_shares(dmt.account_no)
   if user == None:
      flash('Login to Accesss Potfolio')
      return redirect('/login')
   return render_template('/portfolio.html',user=user,dmt=dmt,trans=trans,pft=pft,cmp=cmp,shrs=shrs)


@app.route('/trade',methods=['POST','GET'])
def trade():
   user = session.get('current_user',None)
   if user == None:
      flash('Login to Access Trade Page')
      return redirect('/login')
   return render_template('/trade_page.html',user=user)
