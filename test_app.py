import unittest     
import json
from app import app

# Define Flask test case
class FlaskTestCase(unittest.TestCase):
    # Set up the test client
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # Test valid order
    def test_valid_order(self):
        # Post request with valid JSON data
        response = self.app.post('/orders', data=json.dumps({"components": ["A", "D", "F", "I", "K"]}), content_type='application/json')
        self.assertEqual(response.status_code, 201)  # 201 Created
        data = json.loads(response.data)             # Convert response to JSON
        self.assertIn('1order_id', data)             # Check if '1order_id' key exists
        self.assertIn('2total', data)                # Check if '2total' key exists
        self.assertIn('3parts', data)                # Check if '3parts' key exists
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


if __name__ == '__main__':
    unittest.main(verbosity=2) # Run all tests with proper details