import time 
import random
import collections

from flask import Flask, request, jsonify   # Import Flask modules

app = Flask(__name__)                       # Create Flask app

# Define component data
component_data = {
    "A": {"price": 10.28, "part": "LED Screen", "category": "Screen"},
    "B": {"price": 24.07, "part": "OLED Screen", "category": "Screen"},
    "C": {"price": 33.30, "part": "AMOLED Screen", "category": "Screen"},
    "D": {"price": 25.94, "part": "Wide-Angle Camera", "category": "Camera"},
    "E": {"price": 32.39, "part": "Ultra-Wide-Angle Camera", "category": "Camera"},
    "F": {"price": 18.77, "part": "USB-C Port", "category": "Port"},
    "G": {"price": 15.13, "part": "Micro-USB Port", "category": "Port"},
    "H": {"price": 20.00, "part": "Lightning Port", "category": "Port"},
    "I": {"price": 42.31, "part": "Android OS", "category": "OS"},
    "J": {"price": 45.00, "part": "iOS OS", "category": "OS"},
    "K": {"price": 45.00, "part": "Metallic Body", "category": "Body"},
    "L": {"price": 30.00, "part": "Plastic Body", "category": "Body"}
}

# Define required categories
required_categories = ["Screen", "Camera", "Port", "OS", "Body"] 

# Define route for handling orders
@app.route('/orders', methods=['POST'])

# Define function to handle orders
def create_order():
    request_data = request.json                         # Get JSON data from request
    components = request_data.get('components', [])     # Get list of components

    # Check if components is a list
    if not isinstance(components, list):
        return jsonify({'error': 'Invalid request data. Please provide a list of components.'}), 400

    # Validate input
    if not components or not isinstance(components, list): 
        return jsonify({'error': 'Invalid request data. Please provide a list of components. Example: {"components": ["A", "D", "F", "I", "K"]}'}), 400

    # Sort user-provided component list
    components.sort()

    # Process order
    order_parts = []
    total_price = 0.0
    selected_categories = set()
    
    # Check if component code is valid
    for component_code in components:
        component_info = component_data.get(component_code)     # Get component information i.e dictionary as a value of that key
        if component_info:
            category = component_info['category']               # Get component category's value
            if category in selected_categories:
                return jsonify({'error': 'Invalid order. Only one part per category is allowed.'}), 400     # Invalid order
            selected_categories.add(category)
            order_parts.append(component_info['part'])
            total_price += component_info['price']
        else:
            return jsonify({'error': 'Invalid component code: {}'.format(component_code)}), 400             # Invalid component code

    # Ensure all required categories are included
    if selected_categories != set(required_categories):
        return jsonify({'error': 'Invalid order. Please include one part from each category: Screen, Camera, Port, OS, Body.'}), 400    # Invalid order
    
    # Generate order ID
    def generate_order_id():
        timestamp = int(time.time())                            # Current time in seconds since epoch
        alphabets = ''.join(components)                         # Concatenate component codes
        random_number = random.randint(1000, 9999)              # Random 4-digit number
        order_id = f"{timestamp}{alphabets}{random_number}"     # Generate order ID
        return order_id

    # Return order details
    order_response = collections.OrderedDict([  
    ('order_id', generate_order_id()),  # Generate a unique order ID
    ('total_price', total_price),     # Total price of the order
    ('ordered_parts', order_parts),     # List of parts included in the order
    ])

    return jsonify(order_response), 201

if __name__ == '__main__':
    app.run(debug=True)                                         # Run the Flask app
