import os
from flask import Flask, render_template, request, session , redirect, flash
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
import numpy as np
import pandas as pd
import yfinance as yf
import time
import plotly.graph_objs as go
app = Flask(__name__)


s = os.environ.get("DATABASE_URL")
s = 'postgresql+psycopg2:/' + s[s.find('/')+1:]
app.config['SQLALCHEMY_DATABASE_URI'] = s
db = SQLAlchemy(app)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SECRET_KEY'] = "secret key"
Session(app)

s_time = time.time()-60
shrs_data = None
year_shr_data = None
share_info = {'previousClose': 0, 'regularMarketOpen': 0, 'regularMarketDayHigh': 0,'regularMarketPreviousClose': 253.20,'regularMarketDayLow': 0,'marketCap': 0,'dayLow': 0,'volume': 0,'fiftyTwoWeekHigh': 0,
'fiftyTwoWeekLow': 0,'shortName': '','regularMarketPrice': 0
}
def get_shrs_yf(cmp,period='1d',interval='1m'):
   #comp = str(cmp).translate([None,'[],\''])
   global shrs_data ,share_info,year_shr_data
   global s_time
   shrs_data = yf.download(tickers=cmp,period='1d',interval='1m')
   share_info=yf.Ticker(cmp).info
   s_time = time.time()

def port_shrs_yf(cmp,period='1d',interval='1m',change_gl=True):
   comp = str(cmp).translate([None,'[],\''])
   global shrs_data ,share_info,year_shr_data
   global s_time
   if s_time==None or time.time() - s_time > 60:
      shar_data = yf.download(tickers=cmp,period='1d',interval='1m')
      s_time = time.time()
   if change_gl:
      shrs_data = shar_data
   return shar_data

def get_company_info(cmp,change_gl):
   if change_gl:
      global share_info
      if share_info:
         return
   else:
      share_info = {}
   for c in cmp:
      share_info[c] = yf.Ticker(c).info
   return share_info

from models import User, Bank_Details, demat, company, shares, portfolio, transactions
comp = None
cmp=None
def updt_cmp():
   global comp, cmp
   comp = company.query.all()
   cmp = {}
   for i in comp:
      cmp[i.id] = i
updt_cmp()

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
         session['current_trans'] = transactions.get_trs(session['current_demat'].account_no)
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
   if trans==None:
      trans=[]
   if request.args.get('trade')=='1':
      print("yes")
      #location.href="/user_home?trade=1&company_id"+"{{share_info['symbol']}}"+
      #      "&company="+"{{share_info['shortName']}}"+
      #      "&buy=1"+
      #      "&price="+"{{share_info['regularMarketPrice']}}"+
      #      "&quantity="+document.getElementById("quantity").value;+
      #      "&status=1"
      form=request.args
      print(form)
      try:
         #db.session.add(transactions(time.time(),form.get('company_id'),dmt,bool(form.get('buy')),float(form.get('price')),int(form.get('quantity')),form.get('status')))
         #db.session.add(portfolio(form.get('company_id'),int(form.get('quantity')),float(form.get('price')),dmt))
         #db.session.commit()
      except Exception as exp:
         #print(exp)
         #flash("Improper details")
         return render_template('/user_home.html')
      return render_template('/user_home.html',user=user,dmt=dmt,trans=trans)
   else:
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
   comp=request.args.get('comp')
   if comp== None :
      return render_template('/company_details.html',user=user,cmp_list=list(cmp.keys()),shrs=share_info,shrs_curr=shrs_data,flag=0)
   else:
      get_shrs_yf(comp)
      return render_template('/company_details.html',user=user,cmp_list=list(cmp.keys()),shrs=share_info,shrs_curr=shrs_data,flag=1)

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
   if user == None:
      flash('Login to Accesss Potfolio')
      return redirect('/login')
   pft = portfolio.get_shares(dmt.account_no)
   port_shrs_yf(list(cmp.keys()))
   return render_template('/portfolio.html',user=user,dmt=dmt,trans=trans,pft=pft,cmp=cmp,shrs=shrs_data)

@app.route('/trade',methods=['POST','GET'])
def trade():
   user = session.get('current_user',None)
   dmt = session.get('current_demat',None)
   pft = portfolio.get_shares(dmt.account_no)
   if user == None:
      flash('Login to Access Trade Page')
      return redirect('/login')
   if request.method == 'GET' :
      # tp -> 0 -> sell , tp -> 1 -> buy
      company_to_trade = request.args.get('cmp')
      max_lim = 0
      if company_to_trade:
         if cmp.get(company_to_trade,None):
            global s_time
            if time.time() - s_time > 60 :
               get_shrs_yf(company_to_trade)
            if request.args.get('tp') == '1':
               return render_template('/trade_page.html',user=user,dmt=dmt,shrs=shrs_data,share_info=share_info,sell=0)
            else:
               for shr in pft:
                  if shr.company_id == company_to_trade:
                     max_lim = shr.quantity
                     break
               return render_template('/trade_page.html',user=user,dmt=dmt,shrs=shrs_data,share_info=share_info,max_lim=max_lim,sell=1)
         else:
            try:
               dat = get_shrs_yf([company_to_trade,],period='1y',interval='1d',change_gl=False)
               if dat.empty:
                  print('Company not Found')
               else:
                  shr_info = get_company_info(company_to_trade,False)
                  print("check2"+shr_info)
                  db.session.add(company(company_to_trade,company_to_trade,'-',dat['High'].max(skipna=True),dat['Low'].min(skipna=True)))
                  db.session.commit()
                  updt_cmp()
                  return render_template('/trade_page.html',user=user,dmt=dmt,shrs=shrs_data,share_info=shr_info)
            except Exception as exp:
               print(exp)
   if share_info == None:
      get_shrs_yf(list(cmp.keys()))
   return render_template('/trade_page.html',user=user,dmt=dmt,shrs=shrs_data,share_info=share_info['AAPL'])
