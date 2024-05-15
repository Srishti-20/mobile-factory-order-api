# Mobile Factory Order API

This project is a Flask-based API for processing orders of mobile electronic components. It validates component orders, calculates the total price, and generates a unique order ID. The application includes unit tests to ensure the functionality and reliability of the API.

## Problem Statement

At Mobile Factory Pvt Ltd., we offer configurable mobiles that customers can customize by selecting specific parts. Each mobile configuration must include exactly one part from each of the following categories:

- Screen (LED, OLED, or AMOLED)
- Camera (Wide-Angle or Ultra-Wide-Angle)
- Port (USB-C, Micro-USB, or Lightning)
- OS (Android or iOS)
- Body (Metal or Plastic)

If the order is valid, the total price is calculated and a unique order ID is generated.

## Objective

Implement an API to create the order of a phone given a list of component data.

### Component Data

The components and their respective details are stored in memory:

| Code | Price | Part                    |
| ---- | ----- | ----------------------- |
| A    | 10.28 | LED Screen              |
| B    | 24.07 | OLED Screen             |
| C    | 33.30 | AMOLED Screen           |
| D    | 25.94 | Wide-Angle Camera       |
| E    | 32.39 | Ultra-Wide-Angle Camera |
| F    | 18.77 | USB-C Port              |
| G    | 15.13 | Micro-USB Port          |
| H    | 20.00 | Lightning Port          |
| I    | 42.31 | Android OS              |
| J    | 45.00 | iOS OS                  |
| K    | 45.00 | Metallic Body           |
| L    | 30.00 | Plastic Body            |

## Getting Started

These instructions will guide you to set up and run the project on your local machine for development and testing purposes.

### Prerequisites

Make sure you have `python` or `python3` and `pip` or `pip3` installed on your machine.

### Installation and Running the Application

1. Download both the python code files: `app.py` and `test_app.py` from this repository.
2. Open both the files in an open-source text editor, example: `VS Code`.
3. Install the required packages:
   ```sh
   pip3 install flask
   ```
4. Run the application:
   ```sh
   python3 app.py
   ```

### API Reference

- Open Terminal or Command Prompt in your device.
- Navigate to the Project directory were you saved it.

### command to do the POST request:-

```http
  curl -X POST -H "Content-Type: application/json" -d '{"components": ["I","A","D","F","K"]}' http://127.0.0.1:5000/orders
```

#### Explanation of each components of this curl command line:-

- **curl** It is the command-line tool used to send the request.
- **-X POST** specifies that the request is a POST request.
- **-H "Content-Type: application/json"** sets the request header to indicate the data format is JSON.
- **-d '{"components": ["I","A","D","F","K"]}'** provides the JSON data being sent.
- **http://127.0.0.1:5000/orders:** is the server endpoint receiving the request. It consists of:

```
- http:// - the protocol to use.
- 127.0.0.1 - the IP address of the server. 127.0.0.1 is the loopback address, meaning it refers to the local machine.
- :5000 - the port number on the server. Port 5000 is commonly used by Flask, a Python web framework.
- /orders - the endpoint on the server that will handle the request.
```

### The Response from the above POST request

```json
{
  "1order_id": "1715751735ADFIK2301",
  "2total": 142.3,
  "3parts": [
    "LED Screen",
    "Wide-Angle Camera",
    "USB-C Port",
    "Android OS",
    "Metallic Body"
  ]
}
```
5. Run the UnitTests:
   ```
   python3 test_app.py
   ```


## Project Structure

1. **File `app.py`**

#### Explanation:-

1. Importing the required modules:
   ```
   import time
   import random
   from flask import Flask, request, jsonify
   ```

- importing time to get the current time of ordering, so that we can use it while generating our order ID.
- random is used to put random 4 digit number in our order ID, for it's uniquness.
- importing flask modules to run the application, make the api requests work and jsonify the output.

2. Creating the Flask application, defining the component data and required catagories:

   ```
   app = Flask(__name__)

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
   required_categories = ["Screen", "Camera", "Port", "OS", "Body"]
   ```

- creating the flask app.
- defining the component data provided in the problem statement.
- defining the required categories present in the given data.

3. Defining route for handling orders:
   ```
   @app.route('/orders', methods=['POST'])
   ```

- setting the endpoit to route the application by putting that it in the URL.

4. Defining function to handle orders:
   ```
   def create_order():
   request_data = request.json
   components = request_data.get('components', [])
   ```

-
- get JSON data from request and storing it in the variable request_data.
- .get function helps to find the key and give the values of it.If the key is not found then it puts the default value if provided like in this we gave an empty list as the default value, Storing the Value in the varibale names `components`.

5. Checking the validity of the input:

   ```
   if not isinstance(components, list):
       return jsonify({'error': 'Invalid request data. Please provide a list of components.'}), 400

   if not components or not isinstance(components, list):
       return jsonify({'error': 'Invalid request data. Please provide a list of components. Example: {"components": ["A", "D", "F", "I", "K"]}'}), 400

   components.sort()
   ```

- first condition is to check if components is a list datatype or not.
- second condition is to check if `components` has values in it or is it an empty list, and to verify it's datatype too.
- then we sort the `components`, so as to process the output in the right order of catagories for the required data.

6. Data processing and formating

   ```
   order_parts = []
   total_price = 0.0
   selected_categories = set()

   # Check if component code is valid
   for component_code in components:
       component_info = component_data.get(component_code)     # Get component information i.e dictionary as a value of that key
       if component_info:
           category = component_info['category']               # Get component category's value
           if category in selected_categories:
               return jsonify({'error': 'Invalid order. Only one part per category is allowed.'}), 400
           selected_categories.add(category)
           order_parts.append(component_info['part'])
           total_price += component_info['price']
       else:
           return jsonify({'error': 'Invalid component code: {}'.format(component_code)}), 400
   ```

- took a list() to store the parts ordered, a float() variable to store the calculated price of the items, a set() to store the catagory of the input data processed so that not more than 1 item from the same catagory can be stored in it, hence processing the valid input.
- function to check each value in the input data:
  component_code takes each input at each iteration and check.

component_info have the value searched by the .get() from the
component_data.

if component_info is not None, variable `catagory` will store the value of the key called catagory taken from the component_info. Then it is checked that if the catagory is already present in the selected_categories set() or not, if yes then shows an error, if not then add that catagory to the set().

if component_info is None then throws an error message.

7. Ensure all required categories are included
   ```
   if selected_categories != set(required_categories):
       return jsonify({'error': 'Invalid order. Please include one part from each category: Screen, Camera, Port, OS, Body.'}), 400
   ```

- if both the sets, selected_categories and required_categories and equale then condition is passed, otherwise error.

8. Generate and return the order_details/output

   ```
   def generate_order_id():
       timestamp = int(time.time())                            # Current time in seconds since epoch
       random_number = random.randint(1000, 9999)              # Random 4-digit number
       alphabets = ''.join(components)                         # Concatenate component codes
       order_id = f"{timestamp}{alphabets}{random_number}"     # Generate order ID
       return order_id

   # Return order details
   order_response = {
       'order_id': generate_order_id(),                       # Generate a unique order ID
       'total_price': total_price,                            # Total price of the order
       'ordered_parts': order_parts                           # List of parts included in the order
   }
   return jsonify(order_response), 201
   ```

- generating order ID using current time of out system, alphabets given in the input data and random number generated to make the order completely unique.
- made a dictionary to formate the order_respone so that it can in json format and then jsonified while returning too.

9. Run the application
   ```
   if __name__ == '__main__':
   app.run(debug=True)
   ```

- main function is called here, that means the code starts running from this line of code.
- `app.run()' is the code to start the Flask development server.
- (debug=True) is passed as an argument to enable functionalities like automatic reloading, error debugging information, etc.

2. **File `test_app.py`**

#### Explanation:-

This code file defines a set of unit tests for a Flask application that processes orders based on component selection.

1. Importing modules
   ```
   import unittest
   import json
   from app import app
   ```
2. Class Definition and setUp
   ```
   class FlaskTestCase(unittest.TestCase):
   # Set up the test client
   def setUp(self):
       self.app = app.test_client()
       self.app.testing = True
   ```

- defines a test case class named `FlaskTestCase` that inherits from `unittest.TestCase`. This class will contain the individual test methods for your application.
- `def setUp(self)` method is automatically called before each test case is run. It creates a `test_client` object using the app object which simulates a web browser making requests to the application. Then Sets the testing attribute of the `test_client` to True. This enables additional features for testing, like automatic context handling.

3. Different test cases

   ```
   # Test valid order
   def test_valid_order(self):
       # Post request with valid JSON data
       response = self.app.post('/orders', data=json.dumps({"components": ["A", "D", "F", "I", "K"]}), content_type='application/json')
       self.assertEqual(response.status_code, 201)  # 201 Created
       data = json.loads(response.data)             # Convert response to JSON
       self.assertIn('order_id', data)              # Check if 'order_id' key exists
       self.assertIn('total_price', data)           # Check if 'total_price' key exists
       self.assertIn('ordered_parts', data)         # Check if 'ordered_parts' key exists
       print("\nValid Order Response:", data)       # Print response for debugging

   # Test invalid order with duplicate category
   def test_invalid_order_duplicate_category(self):
       response = self.app.post('/orders', data=json.dumps({"components": ["A", "B", "F", "I", "K"]}), content_type='application/json')
       self.assertEqual(response.status_code, 400)     # 400 Bad Request
       data = json.loads(response.data)
       self.assertIn('error', data)                    # Check if 'error' key exists
       print("\nInvalid Order (Duplicate Category) Response:", data)

   # Test invalid order with missing components
   def test_invalid_order_missing_components(self):
       response = self.app.post('/orders', data=json.dumps({"components": ["A", "D", "F", "I"]}), content_type='application/json')
       self.assertEqual(response.status_code, 400)
       data = json.loads(response.data)
       self.assertIn('error', data)
       print("\nInvalid Order (Missing Components) Response:", data)

   # Test invalid order with invalid component code
   def test_invalid_order_invalid_component(self):
       response = self.app.post('/orders', data=json.dumps({"components": ["A", "D", "F", "I", "X"]}), content_type='application/json')
       self.assertEqual(response.status_code, 400)
       data = json.loads(response.data)
       self.assertIn('error', data)
       print("\nInvalid Order (Invalid Component Code) Response:", data)

   # Test invalid order with non-list components
   def test_invalid_order_non_list_components(self):
       response = self.app.post('/orders', data=json.dumps({"components": "A, D, F, I, K"}), content_type='application/json')
       self.assertEqual(response.status_code, 400)
       data = json.loads(response.data)
       self.assertIn('error', data)
       print("\nInvalid Order (Non-List Components) Response:", data)
   ```

- the code for each test cases is checking each type of error and it's working, the code is pretty much self explanatory.
- uses the test_client.post method to send a POST request to the /orders endpoint of the application. The request body contains JSON data with a key named "components" that holds a list of component codes.
- the content_type argument is set to "application/json" to indicate the format of the request body.
- response Assertions:
  It checks the response status code to ensure it matches the expected outcome (e.g., 201 for successful creation, 400 for errors).

It converts the JSON response to a Python dictionary using json.loads.

It uses assertions from the unittest module to verify the presence of specific keys in the response data (e.g., order_id, total, parts). These assertions are currently using placeholders like "1order_id", "2total", and "3parts". You'll likely need to update them based on the actual response structure from your create_order function.

Optionally, it may print the response data for debugging purposes.

## Hence here we come to an end of out project.
