from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import jsonify
from schemas import CartSchema, CartUpdateSchema
from db import db
from sqlalchemy.exc import SQLAlchemyError
from models import CartModel

blp = Blueprint("carts", __name__, description="Operations on items")

@blp.route("/cart")
class CreateCart(MethodView):
    @blp.arguments(CartSchema)
    @blp.response(201, CartSchema)
    def post(self, cart_data):
        user_id = cart_data.get("user_id")
    
        if not user_id:
            abort(400, message="user_id is required")

        try:
            cart = CartModel(**cart_data)
            cart.user_id = user_id

            db.session.add(cart)
            db.session.commit()

    
            return jsonify({"Message": "Cart has been created successfully"}), 201
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(400, message=f"An error occurred while creating this cart: {str(e)}")
            
            
    @blp.response(200, CartSchema(many=True))
    def get(self):
        carts = CartModel.query.all()
        
        return carts

    
@blp.route("/cart/user/<int:user_id>")
class CartInfo(MethodView):
    def delete(self, user_id):
     
        carts = CartModel.query.filter_by(user_id=user_id).all()
      
        if not carts:
            abort(404, message="No carts found for the user.")
        

        for cart in carts:
            db.session.delete(cart)
        
        db.session.commit()
        
        return jsonify({"message": f"Carts for user {user_id} have been deleted successfully."}), 200
    
    
@blp.route("/cart/<string:cart_id>")
class UpdateCart(MethodView):
    @blp.arguments(CartUpdateSchema)
    @blp.response(201, CartSchema)
    def put(self, cart_data, cart_id):
        cart = CartModel.query.get(cart_id)

        if cart:
            cart.quantity = cart_data.get("quantity")
        else:
            cart = CartModel(id=cart_id, **cart_data)
            db.session.add(cart)
        
        db.session.commit()
        
        return cart








