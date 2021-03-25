import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)


s = os.environ.get("DATABASE_URL")
s = 'postgresql+psycopg2:/' + s[s.find('/')+1:]
app.config['SQLALCHEMY_DATABASE_URI'] = s
db = SQLAlchemy(app)


from models import User

@app.route('/',methods=['POST','GET'])
def home():
   return render_template('/index.html')