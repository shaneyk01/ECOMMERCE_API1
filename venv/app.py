from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey, Table, Column, String, Integer, Float, select
from marshmallow import ValidationError
from typing import List, Optional

# Initialize Flask app and configure database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Sageyk01!2024@localhost/ecommerce_api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class Base(DeclarativeBase):
    pass

# Initialize SQLAlchemy and Marshmallow
db = SQLAlchemy(model_class=Base)
db.init_app(app)
ma = Marshmallow(app)


# Define the many-to-many relationship table between Order and Product
order_products = Table(
    "order_products",
    Base.metadata,
    Column("order_id", ForeignKey("orders.id"), primary_key=True),
    Column("product_id", ForeignKey("products.id"), primary_key=True)
)


# Define the User model
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(200))
    street_number: Mapped[int] = mapped_column(Integer)
    street_name: Mapped[str] = mapped_column(String(100))
    city: Mapped[str] = mapped_column(String(100))
    state: Mapped[str] = mapped_column(String(100))
    zip_code: Mapped[str] = mapped_column(String(20))

# Define the one-to-many relationship with Order
    orders: Mapped[List["Order"]] = relationship("Order", back_populates="user")


# Define the Order model
class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    order_date: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

# Define the one-to-one relationship with User
    user: Mapped["User"] = relationship("User", back_populates="orders")

 # Define the many-to-many relationship between Product and Order
    products: Mapped[List["Product"]] = relationship("Product", secondary=order_products, back_populates="orders")


# Define the Product model
class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)

# Define the many-to-many relationship between Order and Product
    orders: Mapped[List["Order"]] = relationship("Order", secondary=order_products, back_populates="products")


# Define schemas for serialization using Marshmallow
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        include_fk = True

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product

# Create schemas for serialization
User_Schema = UserSchema()
Users_Schema = UserSchema(many=True)
Order_Schema = OrderSchema()
Orders_Schema = OrderSchema(many=True)
Product_Schema = ProductSchema()
Products_Schema = ProductSchema(many=True)

# Create a user
@app.route("/users", methods = ["POST"])
def create_user():
    try:
        user_data = User_Schema.load(request.json)
    except ValidationError as e:
        return jsonify({"validation_errors": e.messages}), 400
    new_user = User(
        name=user_data['name'],
        email=user_data['email'],
        street_number=user_data['street_number'],
        street_name=user_data['street_name'],
            city=user_data['city'],
            state=user_data['state'],
            zip_code=user_data['zip_code']
        )
    db.session.add(new_user)
    db.session.commit()
    return User_Schema.jsonify(new_user), 201

#get all users
@app.route("/users", methods = ["GET"])
def get_users():
    users = db.session.execute(db.select(User)).scalars().all()
    return Users_Schema.jsonify(users)  


#get a single user
@app.route("/users/<int:id>", methods = ["GET"])
def get_user(id):
    user = db.session.get(User, id)
    if user:
        return User_Schema.jsonify(user)
    return {"message": "User not found"}, 404


#update user
@app.route("/users/<int:id>", methods=["PUT"])
def update_user(id): 
    user = db.session.get(User, id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    try:
        user_data = User_Schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify({"validation_errors": e.messages}), 400
    db.session.query(User).filter(User.id == id).update(user_data)
    db.session.commit()
    db.session.refresh(user)
    return User_Schema.jsonify(user), 200


#delete user
@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = db.session.get(User, id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200


#create product
@app.route("/products", methods=["POST"])
def create_product():
    try:
        product_data = Product_Schema.load(request.json)
        new_product = Product(
            name=product_data['name'],
            price=product_data['price']
        )
        db.session.add(new_product)
        db.session.commit()
        db.session.refresh(new_product)
        return Product_Schema.jsonify(new_product), 201
    except ValidationError as e:
        return jsonify({"validation_errors": e.messages}), 400
   


#get all products
@app.route("/products", methods=["GET"])
def get_products():
    products = db.session.execute(db.select(Product)).scalars().all()
    return Products_Schema.jsonify(products)


#get a single product
@app.route("/products/<int:id>", methods=["GET"])
def get_product(id):
    product = db.session.get(Product, id)
    if product:
        return Product_Schema.jsonify(product)
    return {"message": "Product not found"}, 404

#update product
@app.route("/products/<int:id>", methods=["PUT"])
def update_product(id):
    product = db.session.get(Product, id)
    if not product:
        return jsonify({"message": "Product not found"}), 400
    try:
        product_data = Product_Schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify({"validation_errors": e.messages}), 400
    db.session.query(Product).filter(Product.id == id).update(product_data)
    db.session.commit()
    db.session.refresh(product)
    return Product_Schema.jsonify(product), 200


#delete product
@app.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    product = db.session.get(Product, id)
    if not product:
        return jsonify({"message": "Product not found"}), 404
    try:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": f"Product {id} deleted successfully"}), 200
    except ValidationError as e:
        return jsonify({"validation_errors": e.messages}), 400

@app.route("/orders", methods=["POST"])
def create_order():
    try:
        order_data = Order_Schema.load(request.json)
        user = db.session.get(User, order_data['user_id'])
        if not user:
            return jsonify({"error": "User not found"}), 404
        new_order = Order(
            user_id=order_data['user_id'],
            order_date=order_data['order_date']
        )
        db.session.add(new_order)
        db.session.commit()
        return Order_Schema.jsonify(new_order), 201
    except ValidationError as e:
        return jsonify({"validation_errors": e.messages}), 400
   




#get all orders for a user
@app.route("/users/<int:user_id>/orders", methods=["GET"])
def get_user_orders(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    orders = db.session.execute(
        db.select(Order).where(Order.user_id == user_id)
    ).scalars().all()
    return Orders_Schema.jsonify(orders)

#get all products in an order
@app.route("/orders/<int:order_id>/products", methods=["GET"])
def get_order_products(order_id):
    order = db.session.get(Order, order_id)
    if not order:
        return jsonify({"message": "Order not found"}), 404
    products = order.products  
    return Products_Schema.jsonify(products)


#add product to order
@app.route("/orders/<int:order_id>/products", methods=["POST"])
def add_product_to_order(order_id):
    try:
        order = db.session.get(Order, order_id)
        if not order:
            return jsonify({"message": "Order not found"}), 404
        data = request.json
        if not data or 'product_id' not in data:
            return jsonify({"error": "product_id is required"}), 400
        product_id = data['product_id']
        product = db.session.get(Product, product_id)
        if not product:
            return jsonify({"message": "Product not found"}), 404
        if product in order.products:
            return jsonify({"message": "Product already in order"}), 400
        order.products.append(product)
        db.session.commit()
        return jsonify({"message": f"Product {product_id} added to order {order_id}"}), 200
    except ValidationError as e:
        return jsonify({"validation_errors": e.messages}), 400
    

#delete product from order
@app.route("/orders/<int:order_id>/products/<int:product_id>", methods=["DELETE"])
def remove_product_from_order(order_id, product_id):
    try:
        order = db.session.get(Order, order_id)
        if not order:
            return jsonify({"message": "Order not found"}), 404
        product = db.session.get(Product, product_id)
        if not product:
            return jsonify({"message": "Product not found"}), 404
        if product not in order.products:
            return jsonify({"message": "Product not in order"}), 400
        order.products.remove(product)
        db.session.commit()
        return jsonify({"message": f"Product {product_id} removed from order {order_id}"}), 200
    except ValidationError as e:
       return jsonify({"validation_errors": e.messages}), 400


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)