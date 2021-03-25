from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'User'

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.Text,unique=True)
    password = db.Column(db.Text)
    name = db.Column(db.Text)
    email = db.Column(db.Text)
    mobile = db.Column(db.String(14))
    dob = db.Column(db.Date)
    pan_no = db.Column(db.String(10))
    aadhar_no = db.Column(db.String(12))