from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'User'

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(120),unique=True)
    password = db.Column(db.String(120))
    name = db.Column(db.String(200))
    email = db.Column(db.String(80),unique=True)
    mobile = db.Column(db.String(14))
    dob = db.Column(db.Date)
    pan_no = db.Column(db.String(10),unique=True)
    aadhar_no = db.Column(db.String(12),unique=True)

    def __init__(self,username,raw_pass,name,email,mobile,dob,pan_no,aadhar_no):
        self.username = username
        self.set_password(raw_pass)
        self.name = name
        self.email = email
        self.mobile = mobile
        self.dob = dob
        self.pan_no = pan_no
        self.aadhar_no = aadhar_no

    def __repr__(self):
        return '<User %r>' % self.username

    def set_password(self,raw_pass):
        self.password = generate_password_hash(raw_pass)

    def check_password(self,password):
        return check_password_hash(self.password,password)
    
    @classmethod
    def login_user(cls,username,password):
        user = cls.query.filter_by(username=username).first()
        if user == None:
            return None
        if user.check_password(password):
            return user


class Bank_Details(db.Model):
    __tablename__ = 'Bank_Details'

    account_no = db.Column(db.BigInteger,primary_key=True,autoincrement=False)
    User_id = db.Column(db.Integer,db.ForeignKey('User.id',ondelete='CASCADE'))
    user = db.relationship('User',backref=db.backref('User_bank',passive_deletes=True))
    bank_name = db.Column(db.String(120))
    bank_branch = db.Column(db.String(120))
    bank_IFSC = db.Column(db.String(20))

    def __init__(self,bank_ac_no,User_id,bank_name,bank_branch,bank_IFSC):
        self.account_no = bank_ac_no
        self.User_id = User_id
        self.bank_name = bank_name
        self.bank_branch = bank_branch
        self.bank_IFSC = bank_IFSC

    def __repr__(self):
        return '<Bank_ac %r>' % self.account_no


class demat(db.Model):
    __tablename__ = 'demat'

    account_no = db.Column(db.BigInteger,primary_key=True,autoincrement=False)
    User_id = db.Column(db.Integer,db.ForeignKey('User.id',ondelete='CASCADE'))
    user = db.relationship('User',backref=db.backref('User_demat',passive_deletes=True))
    Broker_id = db.Column(db.Integer)
    Broker_name = db.Column(db.String(200))
    Funds_Avail = db.Column(db.Numeric)
    Funds_Blocked = db.Column(db.Numeric)
    Funds_Invested = db.Column(db.Numeric)

    def __init__(self,account_no,User_id,Broker_id,Broker_name):
        self.account_no = account_no
        self.User_id = User_id
        self.Broker_id = Broker_id
        self.Broker_name = Broker_name
        self.Funds_Avail = 0
        self.Funds_Blocked = 0
        self.Funds_Invested = 0
    
    def __repr__(self):
        return '<demat_ac %r>' % self.account_no

