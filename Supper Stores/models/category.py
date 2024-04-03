from db import db 
from datetime import datetime, date, timedelta


class CategoryModel(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True )
    title = db.Column(db.String(50), nullable=False)
    image  = db.Column(db.String(1000000))
    timestamp = db.Column(db.DateTime, default=datetime.now)
    
    
    