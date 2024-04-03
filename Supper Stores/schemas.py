from marshmallow import Schema, fields

# This is the schema we are going to used to be pass in the
# schema model in to set the relationships among other tables 
# for example if you want the productTable and the UserTable  to have a Relationship

class PlainProductSchema(Schema):
    id = fields.Str(dump_only=True)
    productname = fields.Str(required=True)
    description = fields.Str(required=True)
    image = fields.Str(required=True)
    
    
    
class PlainCartSchema(Schema):
    id = fields.Str(dump_only=True)
    quantity = fields.Int(required=True)




# These are the Schema for all the table in the Model folders
    
class UserSchema(Schema):
    id = fields.Str(dump_only=True)
    password = fields.Str(required=True, load_only=True)
    fullname = fields.Str()
    email = fields.Email()
    username = fields.Str()
    address = fields.Str()
    phone = fields.Str()
    timestamp = fields.DateTime()



class CategorySchema(Schema):
    id = fields.Str(dump_only=True)
    title = fields.Str(required=True)
    image = fields.Str(required=True)
    timestamp = fields.DateTime()
    

class ProductUpdateSchema(Schema):
    productname = fields.Str()
    description = fields.Str()
    image = fields.Str()


class CartUpdateSchema(Schema):
    quantity = fields.Int(required=True)
    

    
# These are the schema use to conncect the relationship
class Productschema(PlainProductSchema):
    user_id = fields.Int(required=True, load_only=True)
    category_id = fields.Int(requires=True, load_only=True)
    price = fields.Int(required=True)
    carts = fields.List(fields.Nested(PlainCartSchema()), dump_only=True)


class CartSchema(Schema):
    user_id = fields.Int(required=True, load_only=True)
    product_id = fields.Int(required=True, load_only=True)
    quantity = fields.Int(required=True)
    product = fields.Nested(PlainProductSchema(), dump_only=True)

