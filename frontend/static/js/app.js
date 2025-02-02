// Function to open specific pop-ups
function openPopup(type) {
    const popup = document.getElementById('popup');
    const popupBody = document.getElementById('popup-body');

    popupBody.innerHTML = ""; // Clear previous content

    if (type === 'subscription') {
        popupBody.innerHTML = `
            <h2>Subscription</h2>
            <p>Receive 5 cupcakes weekly for only R$ 30/month!</p>
            <div class="subscription-form">
                <input type="text" placeholder="Enter your name" id="subscription-name" />
                <button onclick="subscribe()">Subscribe Now</button>
            </div>
        `;
    } else if (type === 'menu') {
        fetch('/api/cupcakes') // Updated endpoint
            .then(response => response.json())
            .then(cupcakes => {
                popupBody.innerHTML = `
                    <h2>Menu</h2>
                    <ul>
                        ${cupcakes.map(cupcake => `
                            <li class="menu-item">
                                <h3>${cupcake.nome} - R$ ${cupcake.preco}</h3>
                                <p>${cupcake.descricao}</p>
                                <button onclick="addToCart(${cupcake.id})">Add to Cart</button>
                            </li>
                        `).join('')}
                    </ul>
                `;
            });
    } else if (type === 'history') {
        popupBody.innerHTML = `
            <h2>Shop History</h2>
            <p>Our shop has been serving the community for over 40 years, providing delicious cupcakes to sweeten your day.</p>
        `;
    } else if (type === 'cart') {
        loadCartItems();
    }

    popup.style.display = 'flex'; // Show the popup
}

// Close the popup
function closePopup() {
    document.getElementById('popup').style.display = 'none';
}

// Add a cupcake to the cart
function addToCart(cupcakeId) {
    fetch('/api/cart', { // Updated endpoint
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ cupcake_id: cupcakeId }) // Sending JSON
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    });
}

// Load cart items
function loadCartItems() {
    fetch('/api/cart') // Updated endpoint
        .then(response => response.json())
        .then(cartItems => {
            const popupBody = document.getElementById('popup-body');
            popupBody.innerHTML = `
                <h2>Your Cart</h2>
                <ul>
                    ${cartItems.map(item => {
                        // Check if cupcake data exists
                        const cupcake = item.cupcake || {};
                        return `
                            <li class="cart-item">
                                <p>Cupcake: ${cupcake.nome || 'Unknown'} - R$ ${cupcake.preco || '0.00'}</p>
                                <button onclick="removeFromCart(${item.id})">Remove</button>
                            </li>
                        `;
                    }).join('')}
                </ul>
                <button onclick="completeOrder()">Complete Order</button>
                <button onclick="cancelOrder()">Cancel Order</button>
            `;
        });
}

// Remove an item from the cart
function removeFromCart(cartItemId) {
    fetch(`/api/cart/${cartItemId}`, { // Updated endpoint
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        loadCartItems();
        alert(data.message);
    });
}

// Complete the order
function completeOrder() {
    fetch('/api/orders', { // Updated endpoint
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        alert('Your order has been completed!');
        closePopup();
    });
}

// Cancel the order
function cancelOrder() {
    fetch('/api/orders/cancel', { // Updated endpoint
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        alert('Your order has been cancelled!');
        closePopup();
    });
}

// Subscription action
function subscribe() {
    const name = document.getElementById('subscription-name').value;
    if (name) {
        alert(`Thank you for subscribing, ${name}! You will start receiving cupcakes very soon! Just wait in the store for someone of our staff contact you.`);
        closePopup();
    } else {
        alert('Please enter your name to subscribe.');
    }
}
