from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Frontend routes
@app.route('/')
def index():
    return render_template('index.html')

# Route to get cupcakes (calling FastAPI backend)
@app.route('/cupcakes')
def cupcakes():
    response = requests.get('http://localhost:8000/api/cupcakes')
    cupcakes = response.json()
    return jsonify(cupcakes)

# Route to add cupcake to cart (calling FastAPI backend)
@app.route('/cart', methods=['POST'])
def add_to_cart():
    cupcake_id = request.json['cupcake_id']
    response = requests.post(f'http://localhost:8000/api/cart', json={"cupcake_id": cupcake_id})
    return response.json()

# Route to get cart items (calling FastAPI backend)
@app.route('/cart')
def get_cart_items():
    response = requests.get('http://localhost:8000/api/cart')
    cart_items = response.json()
    return jsonify(cart_items)

if __name__ == "__main__":
    app.run(port=5000)
