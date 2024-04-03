from db import db 
from datetime import datetime, date, timedelta

class UserModel(db.Model):
    __tablename__ = "users" 
    id = db.Column(db.Integer, primary_key=True, index=True)
    fullname = db.Column(db.String(55))
    username = db.Column(db.String(50), )
    email = db.Column(db.String(50),)
    address = db.Column(db.String(250),)
    phone = db.Column(db.String(50), )
    password = db.Column(db.String(150),)
    timestamp = db.Column(db.DateTime, default=datetime.now())
    
    
    
    
    
