from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models for Cupcake, CartItem, and Subscription
class Cupcake(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(300), nullable=False)

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cupcake_id = db.Column(db.Integer, db.ForeignKey('cupcake.id'), nullable=False)
    cupcake = db.relationship('Cupcake', backref=db.backref('cart_items', lazy=True))

class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), nullable=False)
    active = db.Column(db.Boolean, default=True)

# Route for the home page (root)
@app.route('/')
def home():
    return render_template('index.html')

# Endpoint to get the list of cupcakes (Menu)
@app.route('/cupcakes', methods=['GET'])
def get_cupcakes():
    cupcakes = Cupcake.query.all()
    return jsonify([
        {
            'id': cupcake.id,
            'name': cupcake.name,
            'price': cupcake.price,
            'description': cupcake.description
        }
        for cupcake in cupcakes
    ])

# Endpoint to add a cupcake to the cart
@app.route('/cart', methods=['POST'])
def add_to_cart():
    cupcake_id = request.json.get('cupcake_id')
    if not cupcake_id:
        return jsonify({'message': 'Cupcake ID is required'}), 400
    
    cupcake = Cupcake.query.get(cupcake_id)
    if not cupcake:
        return jsonify({'message': 'Cupcake not found'}), 404
    
    new_item = CartItem(cupcake_id=cupcake_id)
    db.session.add(new_item)
    db.session.commit()

    return jsonify({'message': f'Added {cupcake.name} to the cart'}), 201

# Endpoint to get all items in the cart
@app.route('/cart', methods=['GET'])
def get_cart():
    cart_items = CartItem.query.all()
    return jsonify([
        {
            'id': item.id,
            'cupcake_id': item.cupcake.id,
            'name': item.cupcake.name,
            'price': item.cupcake.price
        }
        for item in cart_items
    ])

# Endpoint to remove an item from the cart
@app.route('/cart/<int:cart_item_id>', methods=['DELETE'])
def remove_from_cart(cart_item_id):
    cart_item = CartItem.query.get(cart_item_id)
    if not cart_item:
        return jsonify({'message': 'Item not found'}), 404
    
    db.session.delete(cart_item)
    db.session.commit()

    return jsonify({'message': 'Item removed from cart'}), 200

# Endpoint to complete the order (clear the cart)
@app.route('/order/complete', methods=['POST'])
def complete_order():
    CartItem.query.delete()
    db.session.commit()

    return jsonify({'message': 'Order completed successfully!'}), 200

# Endpoint to cancel the order (clear the cart)
@app.route('/order/cancel', methods=['POST'])
def cancel_order():
    CartItem.query.delete()
    db.session.commit()

    return jsonify({'message': 'Order cancelled successfully!'}), 200

# Endpoint to subscribe for the cupcakes subscription
@app.route('/subscribe', methods=['POST'])
def subscribe():
    user_name = request.json.get('user_name')
    if not user_name:
        return jsonify({'message': 'Name is required'}), 400

    new_subscription = Subscription(user_name=user_name)
    db.session.add(new_subscription)
    db.session.commit()

    return jsonify({'message': f'{user_name}, you are subscribed! Enjoy 5 cupcakes every week!'}), 201

# Endpoint to get all subscriptions
@app.route('/subscriptions', methods=['GET'])
def get_subscriptions():
    subscriptions = Subscription.query.all()
    return jsonify([
        {
            'id': sub.id,
            'user_name': sub.user_name,
            'active': sub.active
        }
        for sub in subscriptions
    ])

# Manually push context to app to create the database before first request
with app.app_context():
    db.create_all()

# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
