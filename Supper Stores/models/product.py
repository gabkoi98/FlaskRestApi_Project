from db import db
from datetime import datetime, date, timedelta

class ProductModel(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    productname = db.Column(db.String(80), nullable=False)  
    description = db.Column(db.String(1000), nullable=False)
    image = db.Column(db.String(1000000))
    price = db.Column(db.Integer,)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False) 
    timestamp = db.Column(db.DateTime, default=datetime.now())
