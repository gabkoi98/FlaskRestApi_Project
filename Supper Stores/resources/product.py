from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import Productschema, ProductUpdateSchema
from db import db
from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("products", __name__, description="Operations on items")

from models import ProductModel

        

@blp.route("/product")
class GetAllProduct(MethodView):
    @blp.arguments(Productschema)
    @blp.response(201, Productschema)
    def post(self, product_data):
        category_id = product_data.get("category_id")
        if not category_id:
            abort(409, message="Category is required")

        try:
            product = ProductModel(**product_data)
            product.category_id = category_id

            db.session.add(product)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message="An error occurred while inserting the product")

        return jsonify({"Message": "Product has been created successfully"}), 201

    
    
    @blp.response(200, Productschema(many=True))
    def get(self):
        products = ProductModel.query.all()
        
        return products

    @blp.response(204)
    def delete(self):
        products = ProductModel.query.all()
        for product in products:
            db.session.delete(product)
        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="An error occurred while deleting the products")
        return jsonify({"Message": "Products are deleted successfully"}), 204


#  This is to find all the product by id

@blp.route("/product/<int:product_id>")
class Product(MethodView):
    @blp.response(201, Productschema)
    def get(self, product_id):
        Product = ProductModel.query.get_or_404(product_id)
        
        return Product
    
    def delete(self, product_id):
        product = ProductModel.query.get_or_404(product_id)
        
        db.session.delete(product)
        db.session.commmit()
        return {"messsage": "product deleted sucdaafully"}
    
      
      
    @blp.arguments(ProductUpdateSchema)
    @blp.response(200, Productschema)
    def put(self, product_data, product_id):
        product = ProductModel.query.get(product_id)
        
        if product:
            product.productname = product_data["productname"]
            product.description = product_data["description"]
            product.image = product_data["image"]
            
        else:
            product = ProductModel(id=product_id, **product_data)
        
        db.session.add(product)
        db.session.commit()
        
        return product


@blp.route("/product/user/<int:user_id>")
class Productupdate(MethodView):
    @blp.response(201, Productschema)
    def get(self, user_id):
        product = ProductModel.query.get_or_404(user_id)
        
        if not product:
            abort(409, message="This product does not exist")
            
        return product
    
    @blp.response(201, Productschema)
    def delete(self, user_id):
        product = ProductModel.query.get_or_404(user_id)
        
        db.session.delete(product)
        db.session.commit()
        
        return {"Message": "Your product has been deleted successfully. Thank you!"}
