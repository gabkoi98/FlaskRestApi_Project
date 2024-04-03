from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import CategorySchema
from db import db
from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("category", __name__, description="Operations on Catetory")

from models import CategoryModel


@blp.route("/category")
class Category(MethodView):
    @blp.arguments(CategorySchema)
    @blp.response(200, CategorySchema)
    def post(self , category_data):
        category = CategoryModel(**category_data)
        
        try:
            db.session.add(category)
            db.session.commit()
            
        except SQLAlchemyError:
              abort(500, message="An error occurred while inserting the category")
        return jsonify({"Message": "category has been created successfully"}) , 201 
    
    
    @blp.response(200, CategorySchema)
    def delete(self, category_data):
        category = CategoryModel.query.get_or_404(category_data)
        
        db.session.delete(category)
        db.session.commit()
        
        return{"Message": "Category has be delete succcesfuly"}
    
    
    @blp.response(200, CategorySchema(many=True))
    def get(self):
        category = CategoryModel.query.all(category)
        
        return category
        
        
        
        
    
    
    
        
        
        

