from app import db
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'User'

    username = db.Column(db.String(120),primary_key=True)
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
    User_id = db.Column(db.String(120),db.ForeignKey('User.username',ondelete='CASCADE'))
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

    account_no = db.Column(db.BigInteger,primary_key=True)
    User_id = db.Column(db.String(120),db.ForeignKey('User.username',ondelete='CASCADE'))
    user = db.relationship('User',backref=db.backref('User_demat',passive_deletes=True))
    Funds_Avail = db.Column(db.Numeric)
    Funds_Blocked = db.Column(db.Numeric)
    Funds_Invested = db.Column(db.Numeric)

    def __init__(self,account_no,User_id):
        self.account_no = account_no
        self.User_id = User_id
        self.Funds_Avail = 0
        self.Funds_Blocked = 0
        self.Funds_Invested = 0
    
    def __repr__(self):
        return '<demat_ac %r>' % self.account_no


class company(db.Model):
    __tablename__ = 'company'

    id = db.Column(db.String(10),primary_key=True)
    name = db.Column(db.String(200),unique=True)
    sector = db.Column(db.String(100))
    year_low = db.Column(db.Numeric)
    year_high = db.Column(db.Numeric)

    def __init__(self,id,name,sector,year_low,year_high):
        self.id = id
        self.name = name
        self.sector = sector
        self.year_low = year_low
        self.year_high = year_high
    
    def __repr__(self):
        return '<comapny %r>' % self.id


class shares(db.Model):
    __tablename__ = 'shares'

    share_id = db.Column(db.Integer,primary_key=True)
    company_id = db.Column(db.String(10),db.ForeignKey('company.id',ondelete='CASCADE'))
    company = db.relationship('company',backref=db.backref('share_company',passive_deletes=True))
    prev_close = db.Column(db.Numeric)
    open_price = db.Column(db.Numeric)
    volume = db.Column(db.Integer)
    date = db.Column(db.DateTime,default=datetime.datetime.now)
    day_low = db.Column(db.Numeric)
    day_high = db.Column(db.Numeric)


    def __init__(self,company_id,prev_close,open_price,volume,date,day_low,day_high):
        self.company_id = company_id
        self.prev_close = prev_close
        self.open_price = open_price
        self.volume = volume
        self.date = date
        self.day_low = day_low
        self.day_high = day_high
    
    def __repr__(self):
        return '<shares %r %r>' % self.company_id , self.date


class portfolio(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    company_id = db.Column(db.String(10),db.ForeignKey('company.id',ondelete='CASCADE'))
    company = db.relationship('company',backref=db.backref('portfolio_company',passive_deletes=True))
    quantity = db.Column(db.Integer)
    bid_price = db.Column(db.Numeric)
    demat_ac = db.Column(db.BigInteger,db.ForeignKey('demat.account_no',ondelete='CASCADE'))
    demat = db.relationship('demat',backref=db.backref('portfolio_demat',passive_deletes=True))

    def  __init__(self,company_id,quantity,bid_price,demat_ac):
        self.company_id = company_id
        self.quantity = quantity
        self.bid_price = bid_price
        self.demat_ac = demat_ac

    def __repr__(self):
        return '<owned %r>' % self.id


class transactions(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    timestamp = db.Column(db.DateTime,default=datetime.datetime.now)
    company_id = db.Column(db.String(10),db.ForeignKey('company.id',ondelete='CASCADE'))
    company = db.relationship('company',backref=db.backref('trans_company',passive_deletes=True))
    demat_ac = db.Column(db.BigInteger,db.ForeignKey('demat.account_no',ondelete='CASCADE'))
    demat = db.relationship('demat',backref=db.backref('portfolio_demat',passive_deletes=True))
    buy = db.Column(db.Boolean)
    price = db.Column(db.Numeric)
    quantity = db.Column(db.Integer)
    status = db.Column(db.Integer)

    def __init__(self,timestamp,company_id,demat_ac,buy,price,quantity,status = 0):
        self.timestamp = timestamp
        self.company_id = company_id
        self.demat_ac = demat_ac
        self.buy = buy
        self.price = price
        self.quantity = quantity
        self.status = status

    def __repr__(self):
        return '<trans %r>' % self.id