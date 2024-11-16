from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__, static_folder='static', template_folder='templates')

# Base URL for the FastAPI backend
FASTAPI_BASE_URL = "http://127.0.0.1:8000/api"

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route to get cupcakes (calling FastAPI backend)
@app.route('/cupcakes', methods=['GET'])
def cupcakes():
    response = requests.get(f"{FASTAPI_BASE_URL}/cupcakes")
    if response.status_code == 200:
        return jsonify(response.json())
    return jsonify({"error": "Failed to fetch cupcakes"}), response.status_code

# Route to add cupcake to the cart
@app.route('/cart', methods=['POST'])
def add_to_cart():
    cupcake_id = request.json.get('cupcake_id')
    if not cupcake_id:
        return jsonify({"error": "Cupcake ID is required"}), 400
    
    response = requests.post(f"{FASTAPI_BASE_URL}/cart", json={"cupcake_id": cupcake_id})
    return jsonify(response.json()), response.status_code

# Route to get cart items (calling FastAPI backend)
@app.route('/cart', methods=['GET'])
def get_cart():
    response = requests.get(f"{FASTAPI_BASE_URL}/cart")
    if response.status_code == 200:
        return jsonify(response.json())
    return jsonify({"error": "Failed to fetch cart items"}), response.status_code

# Route to remove item from cart
@app.route('/cart/<int:item_id>', methods=['DELETE'])
def remove_from_cart(item_id):
    response = requests.delete(f"{FASTAPI_BASE_URL}/cart/{item_id}")
    return jsonify(response.json()), response.status_code

# Route to complete order
@app.route('/order/complete', methods=['POST'])
def complete_order():
    response = requests.post(f"{FASTAPI_BASE_URL}/orders")
    return jsonify(response.json()), response.status_code

# Route to cancel order
@app.route('/order/cancel', methods=['POST'])
def cancel_order():
    response = requests.post(f"{FASTAPI_BASE_URL}/orders/cancel")
    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(port=5000, debug=True)
